# txt-lang-stats
This tool can generate language statistics automatically for a GitHub user:

This tool is designed to be served as auto-updated language statistics on your
GitHub profile README.md.

The output looks like this:

```yaml
[+] Python: 46.0%
[-] Lua: 3.9%
[=] JavaScript: 2.7%
[~] C: 1.8%
[×] TypeScript: 1.5%
[&] Rust: 1.0%
[*] Nim: 0.7%
[.] Others: 41.9%

0% [+++++-=~×&*.....] 100%
```

_Last updated on **2025-04-10 11:53:18** with [`txt-lang-stats`](https://github.com/eeriemyxi/txt-lang-stats)_

See `README-TEMPLATE.md` for reference on templating works.

See [this GitHub Actions
file](https://github.com/eeriemyxi/eeriemyxi/actions/workflows/update-lang-stats.yml)
for reference on how to use this project properly.

# Usage
```console
TXLST_GITHUB_USERNAME=eeriemyxi TXLST_INCLUDE_FORKS=True TXLST_BLACKLIST_LANGS='{"CSS", "Shell", "Emacs Lisp", "KakouneScript"}' TXLST_SYMBOLS='("+", "-", "=", "~", "×", "&", "*", ".")' TXLST_GITHUB_TOKEN="<GITHUB TOKEN HERE>" txt-lang-stats --insert-into README-TEMPLATE.md > README.md
```

Those long variables are just environment variables. You can export them
yourself anytime before running the command.

`TXLST_GITHUB_TOKEN` expects a classic access token with the `repo` section
checked. If you don't want the statistics to include private repositories, you
can get away with just the `repo.public_repo` permission.

# Command-line Arguments
```
usage: txt-lang-stats [-h] [--insert-into INSERT_INTO]

options:
  -h, --help            show this help message and exit
  --insert-into INSERT_INTO
                        Looks for %STATS%, %BAR%, and %DATE% then replaces that line accordingly, finally writes the result to
                        stdin.
```

