import locale
import traceback
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from textwrap import dedent
from typing import Optional, cast

import mistune
from citeproc import CitationStylesBibliography, CitationStylesStyle, formatter
from citeproc.source.bibtex import BibTeX
from dataclass_wizard import DatePattern, DumpMeta, YAMLWizard
from dataclass_wizard import errors as dw_errors
from jinja2.filters import do_striptags
from PIL import Image, UnidentifiedImageError
from slugify import slugify
from yaml.composer import ComposerError

from .customistune import create_custom_markdown
from .generator import mistune_plugins
from .typography import typographie


@dataclass
class Settings:
    title: str
    base_url: str
    extra_vars: str
    target_path: Path
    source_path: Path
    statics_path: Path
    templates_path: Path
    csl_path: Path
    without_statics: bool
    without_search: bool
    flat: bool
    feed_limit: int


class FrenchTypographyRenderer(mistune.HTMLRenderer):
    """Apply French typographic rules to text."""

    def text(self, text):
        text = text.replace("\\ ", " ")
        return typographie(super().text(text), html=True)

    def block_html(self, html):
        html = html.replace("\\ ", " ")
        return typographie(super().block_html(html), html=True)


class ImgsWithSizesRenderer(FrenchTypographyRenderer):
    """Renders images as <figure>s and add sizes."""

    def __init__(self, escape=True, allow_harmful_protocols=None, article=None):
        super().__init__(escape, allow_harmful_protocols)
        self._article = article

    def paragraph(self, text):
        # In case of a figure, we do not want the (non-standard) paragraph.
        if text.strip().startswith("<figure>"):
            return text
        return super().paragraph(text)

    def image(self, text, url, title=None):
        if self._article.images_path is None:
            print(f"Image with URL `{url}` is discarded.")
            return ""
        full_path = self._article.images_path.resolve().parent / url
        try:
            image = Image.open(full_path)
        except (IsADirectoryError, FileNotFoundError, UnidentifiedImageError):
            print(f"`{full_path}` is not a valid image.")
            return ""
        width, height = image.size
        caption = f"<figcaption>{text}</figcaption>" if text else ""
        full_url = f"{self._article.settings.base_url}{self._article.url}{url}"
        return dedent(
            f"""\
            <figure>
                <a href="{full_url}"
                    title="Cliquer pour une version haute résolution">
                    <img
                        src="{full_url}"
                        width="{width}" height="{height}"
                        loading="lazy"
                        decoding="async"
                        alt="{text}">
                </a>
                {caption}
            </figure>
            """
        )


@dataclass
class Numero(YAMLWizard):
    _id: str
    name: str
    description: str
    metadata: str
    articles: list
    title: str = ""
    title_f: str = ""

    @property
    def date(self):
        articles_dates = []
        for article in self.articles:
            if article.date:
                articles_dates.append(article.date)
            else:
                print(f"Metadata error in article {article.title}: missing date")
        if articles_dates:
            return max(articles_dates)
        else:
            print("Metadata error no article found with a date")
            return date.today()

    def __lt__(self, other: "Numero"):
        if not isinstance(other, Numero):
            return NotImplemented
        return self.date < other.date

    def __post_init__(self):
        self.slug = slugify(self.name)

    @property
    def url(self):
        return f"numero/{self.slug}/"

    def configure_articles(self, yaml_path, settings):
        # Preserves abstract_fr key (vs. abstract-fr) when converting to_yaml()
        DumpMeta(key_transform="SNAKE").bind_to(Article)

        loaded_articles = []
        for article in self.articles:
            article_slug = slugify(article["article"]["title"])
            article_folder = (
                yaml_path.parent / f"{article_slug}-{article['article']['_id']}"
            )
            article_yaml_path = article_folder / f"{article_slug}.yaml"
            try:
                try:
                    loaded_article = cast(
                        Article, Article.from_yaml_file(article_yaml_path)
                    )
                except ComposerError:
                    loaded_article = cast(
                        Article,
                        Article.from_yaml(
                            article_yaml_path.read_text().split("---")[1]
                        ),
                    )
            except dw_errors.ParseError as e:
                print(f"Metadata error in `{article['article']['title']}`:")
                print(e)
                exit(1)
            if not loaded_article.date:
                print(f"Article `{loaded_article.title}` skipped (no date).")
                continue
            if loaded_article.date > datetime.today().date():
                print(
                    f"Article `{loaded_article.title}` skipped "
                    f"(future date: {loaded_article.date})."
                )
                continue

            print(f"Parsing article `{loaded_article.title}`")

            if not loaded_article.id:
                loaded_article.id = article_slug
            loaded_article.content_md = (
                article_folder / f"{article_slug}.md"
            ).read_text()
            loaded_article.content_bib_path = article_folder / f"{article_slug}.bib"
            loaded_article.images_path = (
                article_folder / "images"
                if (article_folder / "images").exists()
                else None
            )
            title = loaded_article.dossier[0].get("title")
            title_f = loaded_article.dossier[0].get("title_f")
            if title and title_f:
                self.title = title
                self.title_f = title_f
            else:
                print(f"Article {loaded_article.title} is missing `Issue` metadata")
            loaded_article.numero = self
            loaded_article.settings = settings
            loaded_articles.append(loaded_article)

        self.articles = sorted(loaded_articles, reverse=True)

        for article in self.articles:
            article.init_bibliography()
            article.init_search()


@dataclass
class Article(YAMLWizard):
    title: str
    title_f: str
    id: str = ""
    subtitle: str = ""
    subtitle_f: str = ""
    content_md: str = ""
    content_bib_path: Path = ""
    settings: Settings | None = None
    dossier: list | None = None
    date: Optional[DatePattern["%Y/%m/%d"]] = None  # noqa: F722
    authors: list = None
    abstract: list = None
    keywords: list = None
    numero: Numero | None = None

    def __post_init__(self):
        self.slug = slugify(self.title)
        md = mistune.create_markdown(escape=False)
        self.title_f = md(self.title_f).strip()[len("<p>") : -len("</p>")]
        self.subtitle_f = md(self.subtitle_f).strip()[len("<p>") : -len("</p>")]

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other: "Article"):
        if not isinstance(other, Article):
            return NotImplemented
        return self.date < other.date

    @property
    def abstract_fr(self):
        for abstract in self.abstract:
            if abstract.get("text_f") and (
                abstract.get("lang") == "fr" or abstract.get("lang") is None
            ):
                return abstract["text_f"]

    @property
    def abstract_en(self):
        for abstract in self.abstract:
            if abstract.get("text_f") and abstract.get("lang") == "en":
                return abstract["text_f"]

    @property
    def url(self):
        root = "" if self.settings.flat else f"numero/{self.numero.slug}/"
        return f"{root}article/{self.id}/"

    @property
    def content_html(self):
        md = create_custom_markdown(
            renderer=ImgsWithSizesRenderer(escape=False, article=self),
            plugins=mistune_plugins,
            escape=False,
            bibliography=self.bibliography,
        )
        html_content = md(self.content_md)

        return html_content

    def init_bibliography(self):
        try:
            bib_source = BibTeX(self.content_bib_path, encoding="utf-8")
        except (AttributeError, RuntimeError) as e:
            print(f"Error parsing bibtex {self.content_bib_path}: {e}")
            print(traceback.format_exc())
            self.bibliography = None
            return
        locale_iso, _ = locale.getlocale()
        if locale_iso is None:
            locale_iso = "fr_FR"
        bib_style = CitationStylesStyle(
            self.settings.csl_path, locale=locale_iso.replace("_", "-"), validate=False
        )
        self.bibliography = CitationStylesBibliography(
            bib_style, bib_source, formatter.html
        )

    def init_search(self):
        self.search_data = {
            "title": self.title,
            "url": f"{self.settings.base_url}{self.url}",
            "date": self.date.strftime("%d %B %Y"),
            "content": do_striptags(
                f"{self.content_html} {self.abstract_fr or self.abstract_en or ''}"
            )
            .replace("'", " ")
            .replace("<", "&lt;")
            .replace(">", "&gt;"),
            "numero_url": f"{self.settings.base_url}{self.numero.url}",
            "numero_title_f": self.numero.title_f,
            "numero_date": self.numero.date.strftime("%d %B %Y"),
        }


def configure_numero(yaml_path, settings):
    # Preserves abstract_fr key (vs. abstract-fr) when converting to_yaml()
    DumpMeta(key_transform="SNAKE").bind_to(Numero)

    try:
        numero = Numero.from_yaml_file(yaml_path)
    except ComposerError:
        numero = Numero.from_yaml(yaml_path.read_text().split("---")[1])

    print(f"Parsing numero `{numero.name}`")
    numero.configure_articles(yaml_path, settings)
    return numero


@dataclass
class Keyword:
    slug: str
    name: str
    articles: list

    def __eq__(self, other):
        return self.slug == other.slug

    def __lt__(self, other: "Keyword"):
        if not isinstance(other, Keyword):
            return NotImplemented
        len_self = len(self.articles)
        len_other = len(other.articles)
        if len_self == len_other:
            return self.slug > other.slug
        return len_self < len_other

    @property
    def url(self):
        return f"mot-clef/{self.slug}/"


@dataclass
class Author:
    slug: str
    forname: str
    surname: str
    articles: list
    biography: str = ""

    def __str__(self):
        return f"{self.forname} {self.surname}"

    def __eq__(self, other):
        return self.slug == other.slug

    def __lt__(self, other: "Author"):
        if not isinstance(other, Author):
            return NotImplemented
        len_self = len(self.articles)
        len_other = len(other.articles)
        if len_self == len_other:
            return self.slug > other.slug
        return len_self < len_other

    @property
    def url(self):
        return f"auteur/{self.slug}/"


def collect_keywords(numeros):
    keywords = {}
    for numero in numeros:
        for article in numero.articles:
            article_keywords = []
            for kwds in article.keywords:
                if kwds.get("list") and kwds.get("lang") == "fr":  # TODO: en?
                    for keyword in kwds.get("list", "").split(", "):
                        keyword_slug = slugify(keyword)
                        if keyword_slug in keywords:
                            keywords[keyword_slug].articles.append(article)
                            kw = keywords[keyword_slug]
                        else:
                            kw = Keyword(
                                slug=keyword_slug, name=keyword, articles=[article]
                            )
                            keywords[keyword_slug] = kw
                        article_keywords.append(kw)
            article.keywords = article_keywords
    return dict(sorted(keywords.items(), key=lambda item: item[1], reverse=True))


def collect_authors(numeros):
    authors = {}
    for numero in numeros:
        for article in numero.articles:
            article_authors = []
            if not article.authors:
                continue
            for athr in article.authors:
                author_forname = athr.get("forname", "")
                author_surname = athr.get("surname", "")
                author_biography = athr.get("biography", "")
                author_name = f"{author_forname} {author_surname}".strip()
                if not author_name:
                    continue
                author_slug = slugify(author_name)
                if author_slug in authors:
                    authors[author_slug].articles.append(article)
                    kw = authors[author_slug]
                else:
                    kw = Author(
                        slug=author_slug,
                        forname=author_forname,
                        surname=author_surname,
                        articles=[article],
                        biography=author_biography,
                    )
                    authors[author_slug] = kw
                article_authors.append(kw)
            article.authors = article_authors
    return dict(sorted(authors.items(), key=lambda item: item[1], reverse=True))
