# Crieur — A Static Revue Generator.

With sources from Stylo corpora.

## Run

```
uv run --with crieur crieur stylo <stylo-corpus-id-1> <stylo-corpus-id-2> …
uv run --with crieur crieur generate serve --title PHLiT
```

## Help

### Commands

<!-- [[[cog
import subprocess
import cog
output = subprocess.check_output("crieur --help", shell=True)
help = output.decode()
cog.out(f"```\n{help}\n```")
]]] -->
```
usage: crieur [-h]  ...

options:
  -h, --help   Show this help message and exit

Available commands:
  
    version    Return the current version.
    generate   Generate a new revue website.
    stylo      Initialize a new revue to current directory from Stylo.
    templates  Fetch a theme from a git repository.
    serve      Serve an HTML book from `repository_path`/public or current
               directory/public.

```
<!-- [[[end]]] -->

### Command: `generate`

<!-- [[[cog
import subprocess
import cog
output = subprocess.check_output("crieur generate --help", shell=True)
help = output.decode()
cog.out(f"```\n{help}\n```")
]]] -->
```
usage: crieur generate [-h] [--title TITLE] [--base-url BASE_URL]
                       [--extra-vars EXTRA_VARS] [--target-path TARGET_PATH]
                       [--source-path SOURCE_PATH]
                       [--statics-path STATICS_PATH]
                       [--templates-path TEMPLATES_PATH] [--csl-path CSL_PATH]
                       [--without-statics] [--without-search] [--blog]
                       [--flat] [--feed-limit FEED_LIMIT]

options:
  -h, --help            show this help message and exit
  --title, -t TITLE     Title of the website (default: Crieur).
  --base-url BASE_URL   Base URL of the website, ending with / (default: /).
  --extra-vars EXTRA_VARS
                        stringified JSON extra vars passed to the templates.
  --target-path TARGET_PATH
                        Path where site is built (default: /public/).
  --source-path SOURCE_PATH
                        Path where stylo source were downloaded (default:
                        /sources/).
  --statics-path STATICS_PATH
                        Path where statics are located (default:
                        @crieur/statics/).
  --templates-path TEMPLATES_PATH
  --csl-path CSL_PATH   Path to the CSL applied for bibliography (default:
                        @crieur/styles/apa.csl).
  --without-statics     Do not copy statics if True (default: False).
  --without-search      Do not generate search page if True (default: False).
  --blog, -b            Use the built-in blog theme if True, overrides
                        statics/templates options (default: False).
  --flat, -f            Use a flat tree structure for Article URLs if True
                        (default: False, except for blog).
  --feed-limit FEED_LIMIT
                        Number of max items in the feed (default: 10).

```
<!-- [[[end]]] -->





### Command: `serve`

<!-- [[[cog
import subprocess
import cog
output = subprocess.check_output("crieur serve --help", shell=True)
help = output.decode()
cog.out(f"```\n{help}\n```")
]]] -->
```
usage: crieur serve [-h] [--repository-path REPOSITORY_PATH] [--port PORT]

options:
  -h, --help            show this help message and exit
  --repository-path REPOSITORY_PATH
                        Absolute or relative path to book’s sources (default:
                        current).
  --port, -p PORT       Port to serve the book from (default=8000)

```
<!-- [[[end]]] -->

### Command: `stylo`

<!-- [[[cog
import subprocess
import cog
output = subprocess.check_output("crieur stylo --help", shell=True)
help = output.decode()
cog.out(f"```\n{help}\n```")
]]] -->
```
usage: crieur stylo [-h] [--stylo-instance STYLO_INSTANCE]
                    [--stylo-export STYLO_EXPORT] [--force-download]
                    [stylo_ids ...]

positional arguments:
  stylo_ids             Corpus ids from Stylo, separated by commas.

options:
  -h, --help            show this help message and exit
  --stylo-instance STYLO_INSTANCE
                        Instance of Stylo (default: stylo.huma-num.fr).
  --stylo-export STYLO_EXPORT
                        Stylo export URL (default: https://export.stylo.huma-
                        num.fr).
  --force-download      Force download of sources from Stylo (default: False).

```
<!-- [[[end]]] -->

### Command: `templates`

<!-- [[[cog
import subprocess
import cog
output = subprocess.check_output("crieur templates --help", shell=True)
help = output.decode()
cog.out(f"```\n{help}\n```")
]]] -->
```
usage: crieur templates [-h] [--repo-url REPO_URL] [--source-path SOURCE_PATH]
                        [--quiet]

options:
  -h, --help            show this help message and exit
  --repo-url REPO_URL   Repository URL, ending with / (default:
                        https://gitlab.huma-num.fr/ecrinum/crieur-templates/).
  --source-path SOURCE_PATH
                        The path within the git repository to the theme files
                        (e.g.: blogs/blog-purple).
  --quiet, -q           Do not prompt for file overrides if True (default:
                        False).

```
<!-- [[[end]]] -->
