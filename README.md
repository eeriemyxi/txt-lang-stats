# txt-lang-stats
This tool can generate language statistics automatically for a GitHub user:

The output looks like this:

```yaml
[+] Python: 45.8%
[-] Lua: 3.9%
[=] JavaScript: 2.7%
[~] C: 1.8%
[×] TypeScript: 1.5%
[&] Rust: 1.0%
[*] Nim: 0.8%
[.] Others: 42.0%

0% [+++++-=~×&*.....] 100%
```

_Last updated on **2025-04-09 21:03:47** with [`txt-lang-stats`](https://github.com/eeriemyxi/txt-lang-stats)_

See `README-TEMPLATE.md` for reference.

# Usage
```console
TXLST_GITHUB_USERNAME=eeriemyxi TXLST_INCLUDE_FORKS=True TXLST_BLACKLIST_LANGS='{"CSS", "Shell", "Emacs Lisp", "KakouneScript"}' TXLST_SYMBOLS='("+", "-", "=", "~", "×", "&", "*", ".")' TXLST_GITHUB_TOKEN="<GITHUB TOKEN HERE>" txt-lang-stats --insert-into README-TEMPLATE.md > README.md
```

Those long variables are just environment variables. You can export them
yourself anytime before running the command.

# Command-line Arguments
```
usage: txt-lang-stats [-h] [--insert-into INSERT_INTO]

options:
  -h, --help            show this help message and exit
  --insert-into INSERT_INTO
                        Looks for %STATS%, %BAR%, and %DATE% then replaces that line accordingly, finally writes the result to
                        stdin.
```

