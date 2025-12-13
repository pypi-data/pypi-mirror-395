import re
from typing import TYPE_CHECKING, Any, Dict, List, Match, Union

from citeproc import Citation, CitationItem, CitationStylesBibliography
from mistune.core import BlockState
from slugify.slugify import slugify

if TYPE_CHECKING:
    from citeproc import CitationStylesBibliography
    from mistune.core import BaseRenderer, InlineState
    from mistune.inline_parser import InlineParser

    from ..customistune import CustomMarkdown

# There is no verbose option for that one as citeproc-py is compiling it.
CITATIONS_PATTERN = r"""(?:\[(?P<bracketed_refs>[^\]]*?@[-\w:]+[^\]]*?)\]|(?P<standalone_ref>(?:-@|@)[-\w:]+)(?=[.,;:]|\s|$))"""  # noqa: E501

CITATION_PATTERN = r"""
    (?:^|(?P<prefix>[^@]+?)\s*)                   # Optional prefix before @
    (?P<suppress_author>-)?                       # Optional - sign to suppress author
    @(?P<citation_ref>[-\w:.]+)                   # Capture citation_ref without @
    (?:,\s*(?P<locator>[a-zA-Z.]*\s*[\w-]+))?     # Optional locator
    (?:\s*(?P<suffix>[^@\[\]]+);?)?               # Optional suffix before ;
"""
CITATION_PATTERN_COMPILED = re.compile(CITATION_PATTERN, re.VERBOSE)


def warn(citation_item):
    print(f"Reference with key '{citation_item.key}' not found in the bibliography.")


def parse_bibliography_wrapper(bibliography: "CitationStylesBibliography"):
    def parse_reference(reference: str, state: "InlineState") -> dict:
        match = CITATION_PATTERN_COMPILED.fullmatch(reference)
        if not match:
            return {}

        prefix = match.group("prefix").strip() if match.group("prefix") else ""
        suppress_author = match.group("suppress_author") is not None
        citation_ref = match.group("citation_ref")  # Already includes '@'
        locator = match.group("locator").strip() if match.group("locator") else ""
        suffix = match.group("suffix").strip() if match.group("suffix") else ""
        citations = state.env.get("citations")
        if not citations:
            citations = {}
        if citation_ref not in citations:
            citation = Citation([CitationItem(citation_ref)])
            citations[citation_ref] = citation
            state.env["citations"] = citations
            bibliography.register(citation)
        else:
            citation = citations[citation_ref]
        return {
            "type": "bibliography_ref",
            "raw": citation_ref,
            "attrs": {
                "citation": citation,
                "prefix": prefix,
                "locator": locator,
                "suppress_author": suppress_author,
                "suffix": suffix,
            },
        }

    def parse_bibliography(
        inline: "InlineParser", m: Match[str], state: "InlineState"
    ) -> int:
        standalone_ref = m.group("standalone_ref")
        bracketed_refs = m.group("bracketed_refs")

        if standalone_ref:
            token = parse_reference(standalone_ref, state)
            state.append_token(token)
            return m.end()

        else:  # We have bracketed_refs, let's deal with a dedicated group.
            group = slugify(bracketed_refs)
            tokens = []
            for bracketed_ref in bracketed_refs.split(";"):
                token = parse_reference(bracketed_ref.strip(), state)
                tokens.append(token)
            state.append_token(
                {
                    "type": "bibliography_refs",
                    "raw": group,
                    "attrs": {"citations_tokens": tokens},
                }
            )
            return m.end()

    return parse_bibliography


def md_bibliography_hook(
    md: "CustomMarkdown",
    result: Union[str, List[Dict[str, Any]]],
    state: BlockState,
) -> Union[str, List[Dict[str, Any]]]:
    citations = state.env.get("citations")
    if not citations:
        return result

    state = BlockState()
    state.tokens = [{"type": "bibliography"}]
    output = md.render_state(state)
    return result + output  # type: ignore[operator]


def render_bibliography_ref_wrapper(bibliography: "CitationStylesBibliography"):
    def render_bibliography_ref(
        renderer: "BaseRenderer",
        citation_ref: str,
        citation: Citation,
        prefix: str,
        locator: str,
        suppress_author: bool,
        suffix: str,
    ) -> str:
        citation_content = bibliography.cite(citation, warn)
        if locator:
            locator = f", {locator}"

        # FIXME: remove parenthesis, probably fragile and CSL dependent.
        citation_content = citation_content[1:-1]
        if suppress_author and "," in citation_content:
            # FIXME: remove authors, probably fragile and CSL dependent.
            citation_content = citation_content.split(",", 1)[1].strip()
        return "".join(
            f"""\
<a href="#ref_{citation_ref}" id="anchor_{citation_ref}">\
{prefix}{citation_content}{locator}{suffix}\
</a>""".split("\n")
        )

    return render_bibliography_ref


def render_bibliography_refs_wrapper(bibliography: "CitationStylesBibliography"):
    def render_bibliography_refs(
        renderer: "BaseRenderer", group_ref: str, citations_tokens: list
    ) -> str:
        citations_html = []
        previous_authors = ""
        for citation_token in citations_tokens:
            attrs = citation_token["attrs"]
            citation_content = bibliography.cite(attrs["citation"], warn)
            citation_content = citation_content[1:-1]  # Fragile: remove parenthesis.
            if locator := attrs["locator"]:
                locator = f", {locator}"

            if "," not in citation_content:
                citation_html = "".join(
                    f"""\
{attrs["prefix"]} \
<a href="#ref_{citation_token["raw"]}" id="anchor_{citation_token["raw"]}">\
{citation_content}{locator}\
</a> {attrs["suffix"]}""".strip().split("\n")
                )
                citations_html.append(citation_html)
                continue

            # FIXME: we are making the assumption that authors are separated from date
            # by a comma which is really optimistic and probably only works for the
            # default CSL.
            authors, remaining = citation_content.split(",", 1)
            are_same_authors = authors == previous_authors
            if attrs["suppress_author"] or are_same_authors:
                citation_content = remaining.strip()
            citation_html = "".join(
                f"""\
{attrs["prefix"]} \
<a href="#ref_{citation_token["raw"]}" id="anchor_{citation_token["raw"]}">\
{citation_content}{locator}\
</a> {attrs["suffix"]}""".strip().split("\n")
            )
            if are_same_authors:
                citations_html[-1] += f", {citation_html}"
            else:
                citations_html.append(citation_html)
            previous_authors = authors
        return f"({'; '.join(citations_html)})"

    return render_bibliography_refs


def render_bibliography_wrapper(bibliography: "CitationStylesBibliography"):
    def render_bibliography(renderer: "BaseRenderer") -> str:
        html_bibliography = ""

        def clean_item(item):
            # As of 2025, citeproc-py does not support repeated punctuation.
            return str(item).replace("..", ".").replace(".</i>.", ".</i>")

        for citation, item in zip(bibliography.items, bibliography.bibliography()):
            citation_ref = citation.reference.get("key")
            cleaned_item = clean_item(item)
            html_bibliography += f"""
    <li>
        <span id="ref_{citation_ref}">
            {cleaned_item}
            <a href="#anchor_{citation_ref}">↩</a>
        </span>
    </li>
    """.strip()
        return f"""\
<section id="bibliography">
<ol>
    {html_bibliography}
</ol>
</section>
"""

    return render_bibliography


def bibliography(md: "CustomMarkdown") -> None:
    """A mistune plugin to support bibliography with Bibtex.

    :param md: CustomMarkdown instance
    """
    if md.bibliography is None:
        return
    md.inline.register(
        "bibliography",
        CITATIONS_PATTERN,
        parse_bibliography_wrapper(md.bibliography),
        before="link",
    )
    md.after_render_hooks.append(md_bibliography_hook)

    if md.renderer and md.renderer.NAME == "html":
        md.renderer.register(
            "bibliography_ref", render_bibliography_ref_wrapper(md.bibliography)
        )
        md.renderer.register(
            "bibliography_refs", render_bibliography_refs_wrapper(md.bibliography)
        )
        md.renderer.register(
            "bibliography", render_bibliography_wrapper(md.bibliography)
        )
