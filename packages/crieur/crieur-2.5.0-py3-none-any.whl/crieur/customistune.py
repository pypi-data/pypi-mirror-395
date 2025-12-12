from typing import Optional

from citeproc import CitationStylesBibliography
from mistune.block_parser import BlockParser
from mistune.inline_parser import InlineParser
from mistune.markdown import Markdown
from mistune.plugins import import_plugin
from mistune.renderers.html import HTMLRenderer

"""
Custom Markdown class instanciation to be able to attach the
`bibliography` attribute to the class upon creation before plugins
are instanciated because we need that element for the bibliography
plugin which handle citations using citeproc-py.
"""


class CustomMarkdown(Markdown):
    """Markdown instance to convert markdown text into HTML or other formats.
    Here is an example with the HTMLRenderer::

        from mistune import HTMLRenderer

        md = Markdown(renderer=HTMLRenderer(escape=False))
        md('hello **world**')

    :param renderer: a renderer to convert parsed tokens
    :param block: block level syntax parser
    :param inline: inline level syntax parser
    :param plugins: mistune plugins to use
    :param bibliography: a bibliography object from citeproc-py
    """

    def __init__(
        self,
        renderer=None,
        block: Optional[BlockParser] = None,
        inline: Optional[InlineParser] = None,
        plugins=None,
        bibliography: Optional[CitationStylesBibliography] = None,
    ):
        if block is None:
            block = BlockParser()

        if inline is None:
            inline = InlineParser()

        self.renderer = renderer
        self.block: BlockParser = block
        self.inline: InlineParser = inline
        self.bibliography: CitationStylesBibliography = bibliography
        self.before_parse_hooks = []
        self.before_render_hooks = []
        self.after_render_hooks = []

        if plugins:
            for plugin in plugins:
                plugin(self)


def create_custom_markdown(
    escape: bool = True,
    hard_wrap: bool = False,
    renderer="html",
    plugins=None,
    bibliography: Optional[CitationStylesBibliography] = None,
) -> Markdown:
    """Create a Markdown instance based on the given condition.

    :param escape: Boolean. If using html renderer, escape html.
    :param hard_wrap: Boolean. Break every new line into ``<br>``.
    :param renderer: renderer instance, default is HTMLRenderer.
    :param plugins: List of plugins.
    :param bibliography: a bibliography object from citeproc-py

    This method is used when you want to re-use a Markdown instance::

        markdown = create_markdown(
            escape=False,
            hard_wrap=True,
        )
        # re-use markdown function
        markdown('.... your text ...')
    """
    if renderer == "ast":
        # explicit and more similar to 2.x's API
        renderer = None
    elif renderer == "html":
        renderer = HTMLRenderer(escape=escape)

    inline = InlineParser(hard_wrap=hard_wrap)
    if plugins is not None:
        plugins = [import_plugin(n) for n in plugins]
    return CustomMarkdown(
        renderer=renderer, inline=inline, plugins=plugins, bibliography=bibliography
    )
