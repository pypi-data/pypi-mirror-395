import argparse
import copy
import logging
import os
import urllib
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
import yaml

from indicomb2.markdown import Markdown
from indicomb2.requests import BearerAuth

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

BASE_URL = "/search/api/search"
SITE = "https://indico.cern.ch"
API_TOKEN = os.environ.get("INDICO_API_TOKEN", None)
DEFAULT_KWARGS = {"site": SITE, "api_token": API_TOKEN}
DEFAULT_PARAMS = {
    "category": "ATLAS Meetings",
    "sort": "mostrecent",
    "type": "contribution",
    "years": 1,
}


def request(site: str, url: str, params: dict, api_token: str):
    items = list(params.items()) if hasattr(params, "items") else list(params)
    items = sorted(items, key=lambda x: x[0].lower())
    url = f"{site}{url}?{urllib.parse.urlencode(items)}"
    logging.info(f"Requesting {url}")
    response = requests.get(url, auth=BearerAuth(api_token), timeout=30)
    response.encoding = response.apparent_encoding
    response.raise_for_status()
    return response.json()


def search(params, kwargs) -> list:
    params = copy.deepcopy(params)
    req = request(url=BASE_URL, params=params, **kwargs)
    pages = req["pages"]
    results = req["results"]
    for page in range(2, pages + 1):
        params["page"] = page
        req = request(url=BASE_URL, params=params, **kwargs)
        results += req["results"]
    return results


def make_table(results, target) -> None:
    # get data
    data = {"Date": [], "Title": [], "Speakers": []}
    for r in results:
        url = f"{SITE}{r['url']}"
        date = r["date"]
        data["Date"].append(f"[{date}]({url})")
        data["Title"].append(r["title"])
        data["Speakers"].append(", ".join(p["name"] for p in r["persons"]))

    # create table
    md = Markdown()
    md += "\n"
    md += md.header("Meeting Contributions", level=2)
    md += md.table(data)

    # write table
    target = Path(target)
    with target.open("a") as f:
        f.write(str(md))


def get_start_range(years: int = 1) -> str:
    end_date = (datetime.now(tz=timezone.utc).date() + timedelta(days=30)).isoformat()
    start_date = (datetime.now(tz=timezone.utc).date() - timedelta(days=365 * years)).isoformat()
    return f"[{start_date} TO {end_date}]"


def run_search(config) -> None:
    logging.info(f"Searching for target file {config['target']}")

    assert isinstance(config["params"], dict), "params must be a dictionary"
    queries = config["params"].pop("queries")
    assert isinstance(queries, list), "queries must be a list"

    results = []
    params = {**DEFAULT_PARAMS, **config["params"]}
    params["start_range"] = get_start_range(params.pop("years"))
    for query in queries:
        params["q"] = query
        logging.info(f"Searching for qeury {query}")
        this_results = search(params, DEFAULT_KWARGS)
        logging.info(f"Found {len(this_results)} results")
        results += this_results

    results = [r for r in results if r["start_dt"] is not None]
    for r in results:
        r["date"] = datetime.fromisoformat(r["start_dt"]).strftime("%Y-%m-%d")
    results.sort(key=lambda x: x["date"], reverse=True)  # noqa: FURB118

    logging.info(f"Number of total results: {len(results)}")
    exclude = config.get("exclude", [])
    if exclude:
        results = [
            r for r in results if not any(ex.lower() in r["title"].lower() for ex in exclude)
        ]
        logging.info(f"Number of results after excluding: {len(results)}")

    make_table(results, config["target"])


def main(args=None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        required=True,
        type=str,
        help="Path to the config file",
    )
    args = parser.parse_args(args)
    with Path(args.config).open() as f:
        config = yaml.safe_load(f)

    for cfg in config["search"]:
        run_search(cfg)


if __name__ == "__main__":
    main()
