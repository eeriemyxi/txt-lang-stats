import argparse
import ast
import collections
import datetime
import functools
import hashlib
import http.client
import io
import json
import math
import os
import pathlib
import pickle
import sys
import time

CACHE_PATH = pathlib.Path(os.environ.get("TXLST_CACHE_PATH") or "/tmp/TXLST/")
CACHE_PATH.mkdir(exist_ok=True)

GITHUB_USERNAME = os.environ["TXLST_GITHUB_USERNAME"]
INCLUDE_FORKS = bool(ast.literal_eval(os.environ["TXLST_INCLUDE_FORKS"]))
BLACKLIST_LANGS = ast.literal_eval(os.environ["TXLST_BLACKLIST_LANGS"])
SYMBOLS = ast.literal_eval(os.environ["TXLST_SYMBOLS"])
GITHUB_TOKEN = os.environ["TXLST_GITHUB_TOKEN"]

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0"

HEADERS = {
    "User-Agent": USER_AGENT,
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

LangStat = collections.namedtuple("LangStat", ["name", "bytes"])


def sha256_hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def cache_call(path: pathlib.Path, expiry: int, args_to_cache: list):
    assert len(args_to_cache) > 0, "Can't make a cache file for that amount of args"

    def decorator(func):
        key_name = func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            assert len(kwargs) > 0, "Can't make a cache file for that amount of args"
            args_c = "+".join(str(kwargs[a]) for a in args_to_cache)
            args_hash = sha256_hash(args_c)
            result_file_path = CACHE_PATH / key_name / args_hash

            if result_file_path.is_file():
                with open(result_file_path, "rb") as file:
                    data = pickle.load(file)
                    if not time.time() > data["expiry"]:
                        return data["result"]

            result = func(*args, **kwargs)

            result_file_path.parent.mkdir(exist_ok=True)
            with open(result_file_path, "wb") as file:
                pickle.dump(dict(result=result, expiry=int(time.time()) + expiry), file)

            return result

        return wrapper

    return decorator


@cache_call(CACHE_PATH, 3600, ["username", "repo_name"])
def get_language_stats(client, *, username, repo_name: str):
    client.request("GET", f"/repos/{username}/{repo_name}/languages", None, HEADERS)
    response = client.getresponse()

    if response.status == 200:
        data = response.read()
        return json.loads(data)
    else:
        print(f"Response failed: {response.read()}", file=sys.stderr)


@cache_call(CACHE_PATH, 3600, ["inc_forks", "page"])
def get_repos(client, *, inc_forks: bool, page: int = 1):
    client.request("GET", f"/user/repos?type=sources&page={page}", None, HEADERS)
    response = client.getresponse()

    if response.status == 200:
        data = response.read()
        return json.loads(data)
    else:
        print(f"Response failed: {response.read()}", file=sys.stderr)


def iterate_repos(client, inc_forks: bool, page: int = 1):
    resjson = ["useless_element"]

    while resjson != []:
        resjson = get_repos(client, inc_forks=inc_forks, page=page)

        for repo in resjson:
            if repo["fork"] and not inc_forks:
                continue
            yield repo

        page += 1


def get_stats_for(username: str, include_forks: bool, symbols: tuple | list):
    client = http.client.HTTPSConnection("api.github.com")
    counter = collections.Counter()

    for index, repo in enumerate(iterate_repos(client, include_forks)):
        stats = get_language_stats(client, username=username, repo_name=repo["name"])
        if not stats:
            continue
        counter.update(stats)

    symbols = list(symbols)
    rest_symbol = symbols.pop()

    slangs = [LangStat(*it) for it in counter.most_common()]
    total = counter.total()

    stats = io.StringIO()
    bar = io.StringIO()
    mc_iter = iter(slangs)
    others = []

    for lang in mc_iter:
        if not symbols:
            break

        if lang.name in BLACKLIST_LANGS:
            others.append(lang)
            continue

        symbol = symbols.pop(0)
        percent = lang.bytes / total * 100
        n = math.ceil(percent / 10)

        stats.write(f"[{symbol}] {lang.name}: {percent:.1f}%\n")
        bar.write(symbol * n)

    others = [*others, *mc_iter]
    percent = 0

    for lang in others:
        percent += lang.bytes / total * 100

    n = math.ceil(percent / 10)

    stats.write(f"[{rest_symbol}] Others: {percent:.1f}%\n")
    bar.write(rest_symbol * n)

    return stats, bar


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--insert-into",
        type=argparse.FileType("r"),
        help="Looks for %%STATS%%, %%BAR%%, and %%DATE%% then replaces that line accordingly, finally writes the result to stdin.",
    )
    args = parser.parse_args()

    stats, bar = get_stats_for(GITHUB_USERNAME, INCLUDE_FORKS, SYMBOLS)

    stats = stats.getvalue()
    bar = f"0% [{bar.getvalue()}] 100%\n"

    if not args.insert_into:
        print(stats.strip())
        print(bar.strip())
        return

    final = io.StringIO()
    for line in args.insert_into.readlines():
        if "%%STATS%%" in line:
            final.write(stats)
            continue
        if "%%BAR%%" in line:
            final.write(bar)
            continue
        if "%%DATE%%" in line:
            final.write(
                line.replace(
                    "%%DATE%%", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            )
            continue

        final.write(line)

    print(final.getvalue())


if __name__ == "__main__":
    main()
