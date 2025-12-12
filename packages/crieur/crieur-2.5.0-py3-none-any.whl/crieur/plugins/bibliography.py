from typing import TYPE_CHECKING, Any, Dict, List, Match, Union

from citeproc import Citation, CitationItem, CitationStylesBibliography
from mistune.core import BlockState

if TYPE_CHECKING:
    from citeproc import CitationStylesBibliography
    from mistune.core import BaseRenderer, InlineState
    from mistune.inline_parser import InlineParser

    from ..customistune import CustomMarkdown


CITATIONS_REFS = r"\[(?P<suppress>\-?)@(?P<ref>.*?)\]"


def clean_ref(citation_ref):
    # TODO: deal with page references (for instance `[@goody_raison_1979, pp.115]`).
    return citation_ref.split(",")[0]


def warn(citation_item):
    print(f"Reference with key '{citation_item.key}' not found in the bibliography.")


def parse_bibliography_wrapper(bibliography: "CitationStylesBibliography"):
    def parse_bibliography(
        inline: "InlineParser", m: Match[str], state: "InlineState"
    ) -> int:
        author_suppressed = clean_ref(m.group("suppress"))  # TODO
        citation_ref = clean_ref(m.group("ref"))
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
        state.append_token(
            {
                "type": "bibliography_ref",
                "raw": citation_ref,
                "attrs": {"citation": citation},
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
        renderer: "BaseRenderer", citation_ref: str, citation: Citation
    ) -> str:
        return "".join(
            f"""\
<a href="#ref_{citation_ref}" id="anchor_{citation_ref}">\
{bibliography.cite(citation, warn)}\
</a>""".split("\n")
        )

    return render_bibliography_ref


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
        CITATIONS_REFS,
        parse_bibliography_wrapper(md.bibliography),
        before="link",
    )
    md.after_render_hooks.append(md_bibliography_hook)

    if md.renderer and md.renderer.NAME == "html":
        md.renderer.register(
            "bibliography_ref", render_bibliography_ref_wrapper(md.bibliography)
        )
        md.renderer.register(
            "bibliography", render_bibliography_wrapper(md.bibliography)
        )
