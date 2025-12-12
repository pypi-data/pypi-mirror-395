import json
import locale
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

from feedgen.feed import FeedGenerator
from jinja2 import Environment as Env
from jinja2 import FileSystemLoader
from slugify import slugify

from . import VERSION
from .customistune import create_custom_markdown
from .typography import typographie
from .utils import neighborhood

# Only support locales compatible with citeproc-py available in:
# https://github.com/citation-style-language/locales/tree/master
for locale_ in ["fr_FR.UTF-8", "fr_CA.UTF-8", "fr_FR", "fr_CA"]:
    try:
        locale.setlocale(locale.LC_ALL, locale_)
        break
    except locale.Error:
        continue
    locale.setlocale(locale.LC_ALL, "")


mistune_plugins = [
    "footnotes",
    "superscript",
    "table",
    "crieur.plugins.inline_footnotes.inline_footnotes",
    "crieur.plugins.bibliography.bibliography",
]
md = create_custom_markdown(plugins=mistune_plugins, escape=False)


def slugify_(value):
    return slugify(value)


def markdown(value):
    return md(value) if value else ""


def typography(value):
    value = value.replace("\\ ", " ")
    value = value.replace("'", "’")
    return typographie(value) if value else ""


def pluralize(number, singular="", plural="s"):
    if number == 1:
        return singular
    else:
        return plural


def generate_html(numeros, keywords, authors, settings):
    environment = Env(
        loader=FileSystemLoader(
            [str(settings.templates_path), str(Path(__file__).parent / "templates")]
        )
    )
    environment.filters["slugify"] = slugify_
    environment.filters["markdown"] = markdown
    environment.filters["typography"] = typography
    environment.filters["pluralize"] = pluralize

    extra_vars = json.loads(settings.extra_vars) if settings.extra_vars else {}

    common_params = {
        "title": settings.title,
        "base_url": settings.base_url,
        "numeros": numeros,
        "articles": sorted(
            [article for numero in numeros for article in numero.articles], reverse=True
        ),
        "keywords": keywords,
        "authors": authors,
        "crieur_version": VERSION,
        "settings": settings,
        **extra_vars,
    }

    template_homepage = environment.get_template("homepage.html")
    content = template_homepage.render(is_homepage=True, **common_params)
    settings.target_path.mkdir(parents=True, exist_ok=True)
    (settings.target_path / "index.html").write_text(content)

    template_numeros = environment.get_template("numeros.html")
    content = template_numeros.render(is_numeros=True, **common_params)
    numeros_folder = settings.target_path / "numero"
    numeros_folder.mkdir(parents=True, exist_ok=True)
    (numeros_folder / "index.html").write_text(content)

    template_blog = environment.get_template("blog.html")
    content = template_blog.render(is_blog=True, **common_params)
    blog_folder = settings.target_path / "blog"
    blog_folder.mkdir(parents=True, exist_ok=True)
    (blog_folder / "index.html").write_text(content)

    for index, previous_numero, numero, next_numero in neighborhood(numeros):
        template_numero = environment.get_template("numero.html")
        content = template_numero.render(
            numero=numero,
            previous_numero=previous_numero,
            next_numero=next_numero,
            **common_params,
        )
        numero_folder = settings.target_path / "numero" / numero.slug
        numero_folder.mkdir(parents=True, exist_ok=True)
        (numero_folder / "index.html").write_text(content)

        template_article = environment.get_template("article.html")
        for index, previous_article, article, next_article in neighborhood(
            numero.articles
        ):
            # next and previous are reversed because articles are antechrono.
            content = template_article.render(
                article=article,
                previous_article=next_article,
                next_article=previous_article,
                **common_params,
            )
            root_folder = settings.target_path if settings.flat else numero_folder
            article_folder = root_folder / "article" / article.id
            article_folder.mkdir(parents=True, exist_ok=True)
            (article_folder / "index.html").write_text(content)
            if article.images_path:
                shutil.copytree(
                    article.images_path, article_folder / "images", dirs_exist_ok=True
                )

    template_keywords = environment.get_template("keywords.html")
    content = template_keywords.render(is_keywords=True, **common_params)
    keywords_folder = settings.target_path / "mot-clef"
    keywords_folder.mkdir(parents=True, exist_ok=True)
    (keywords_folder / "index.html").write_text(content)

    for slug, keyword in keywords.items():
        template_keyword = environment.get_template("keyword.html")
        content = template_keyword.render(keyword=keyword, **common_params)
        keyword_folder = settings.target_path / "mot-clef" / keyword.slug
        keyword_folder.mkdir(parents=True, exist_ok=True)
        (keyword_folder / "index.html").write_text(content)

    template_authors = environment.get_template("authors.html")
    content = template_authors.render(is_authors=True, **common_params)
    authors_folder = settings.target_path / "auteur"
    authors_folder.mkdir(parents=True, exist_ok=True)
    (authors_folder / "index.html").write_text(content)

    for slug, author in authors.items():
        template_author = environment.get_template("author.html")
        content = template_author.render(author=author, **common_params)
        author_folder = settings.target_path / "auteur" / author.slug
        author_folder.mkdir(parents=True, exist_ok=True)
        (author_folder / "index.html").write_text(content)

    if not settings.without_search:
        search_index = json.dumps(
            [article.search_data for numero in numeros for article in numero.articles],
            indent=2,
        )
        template_search = environment.get_template("search.html")
        content = template_search.render(
            is_search=True, search_index=search_index, **common_params
        )
        search_folder = settings.target_path / "recherche"
        search_folder.mkdir(parents=True, exist_ok=True)
        (search_folder / "index.html").write_text(content)


def generate_feed(numeros, settings, lang="fr"):
    feed = FeedGenerator()
    feed.id(settings.base_url)
    feed.title(settings.title)
    feed.link(href=settings.base_url, rel="alternate")
    feed.link(href=f"{settings.base_url}feed.xml", rel="self")
    feed.language(lang)

    articles = sorted(
        [article for numero in numeros for article in numero.articles], reverse=True
    )

    for article in articles[: settings.feed_limit]:
        feed_entry = feed.add_entry(order="append")
        feed_entry.id(f"{settings.base_url}{article.url}")
        feed_entry.title(article.title_f)
        feed_entry.link(href=f"{settings.base_url}{article.url}")
        feed_entry.updated(
            datetime.combine(
                article.date,
                datetime.min.time(),
                tzinfo=timezone(timedelta(hours=-4), "ET"),
            )
        )
        for author in article.authors:
            feed_entry.author(name=str(author))
        feed_entry.summary(summary=article.content_html, type="html")
        if article.keywords:
            for keyword in article.keywords:
                feed_entry.category(term=keyword.name)

    feed.atom_file(settings.target_path / "feed.xml", pretty=True)
    print(f"Generated meta-feed with {settings.feed_limit} items.")
