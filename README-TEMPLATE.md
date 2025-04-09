# txt-lang-stats
This tool can generate language statistics automatically for a GitHub user:

The output looks like this:

```yaml
%%STATS%%

%%BAR%%
```

_Last updated on **%%DATE%%** with [`txt-lang-stats`](https://github.com/eeriemyxi/txt-lang-stats)_

See `README-TEMPLATE.md` for reference.

# Usage
```console
TXLST_GITHUB_USERNAME=eeriemyxi TXLST_INCLUDE_FORKS=True TXLST_BLACKLIST_LANGS='{"CSS", "Shell", "Emacs Lisp", "KakouneScript"}' TXLST_SYMBOLS='("+", "-", "=", "~", "×", "&", "*", ".")' TXLST_GITHUB_TOKEN="<GITHUB TOKEN HERE>" txt-lang-stats --insert-into README-TEMPLATE.md > README.md
```

Those long variables are just environment variables. You can export them
yourself anytime before running the command.
