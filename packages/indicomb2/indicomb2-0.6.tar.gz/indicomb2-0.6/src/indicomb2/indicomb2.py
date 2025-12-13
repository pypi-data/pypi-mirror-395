import argparse
import datetime
import json
import logging
import multiprocessing as mp
import os
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml

import indicomb2.requests as ireq
from indicomb2.event import Event
from indicomb2.meetings import Meetings

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


@dataclass
class Indico:
    category_id: int
    api_token: str = None
    site: str = "https://indico.cern.ch"
    years: int = 1

    def __post_init__(self):
        if self.api_token is None:
            self.api_token = os.environ.get("INDICO_API_TOKEN", None)
        if self.api_token is None:
            msg = "Please provide an API token or set INDICO_API_TOKEN in your env"
            raise ValueError(msg)

        self.url = f"{self.site}/category/{self.category_id}/"
        today = datetime.datetime.now(tz=datetime.timezone.utc).date()
        start_date = today - datetime.timedelta(days=365 * self.years)
        self.start_date = start_date.strftime("%Y-%m-%d")
        logging.info(
            f"Fetching meetings for {self.category_id} from {self.start_date}",
        )
        self.req_kwargs = {"site": self.site, "api_token": self.api_token}
        self.events = ireq.request_category(
            category_id=self.category_id, start_date=self.start_date, **self.req_kwargs
        )

    @staticmethod
    def filter_events(
        results: dict, include: list[str] | None = None, exclude: list[str] | None = None
    ):
        if include is None:
            include = []
        if exclude is None:
            exclude = []
        include = [x.lower() for x in include]
        exclude = [x.lower() for x in exclude]

        # if no include, return all
        if not include:
            return results

        return [
            r
            for r in results
            if any(x in r["title"].lower() for x in include)
            and not any(x in r["title"].lower() for x in exclude)
            and not (
                "label" in r
                and r["label"] is not None
                and r["label"].get("title").lower() == "cancelled"
            )
        ]

    def get_contributions(self, event: dict):
        event = ireq.request_event(event["id"], **self.req_kwargs)
        assert len(event) == 1
        event = event[0]
        return Event.from_indico(
            url=event["url"],
            date=event["startDate"]["date"],
            title=event["title"],
            contributions=event["contributions"],
        )

    def get_meetings(
        self,
        include: list[str] | None = None,
        exclude: list[str] | None = None,
    ) -> Meetings:
        if exclude is None:
            exclude = []
        exclude += ["cancelled"]
        events = self.filter_events(self.events, include=include, exclude=exclude)
        results = []
        status = []
        pool = mp.Pool(processes=mp.cpu_count())
        for event in events:
            kwargs = {"event": event}
            status.append(
                pool.apply_async(self.get_contributions, kwds=kwargs, callback=results.append)
            )
        pool.close()
        pool.join()
        # check for errors
        for x in status:
            x.get()
        logging.info(f"Fetched contributions for {len(results)} events")
        return Meetings(sorted(results), self.url, self.start_date)


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        required=True,
        type=str,
        help="Path to the config file",
    )
    args = parser.parse_args(args)

    # load config
    with Path(args.config).open() as f:
        config = yaml.safe_load(f)

    # get sub configs
    summary_config = config.get("meeting_summaries", {})
    topical_config = config.get("topical_contributions", {})
    minutes_config = config.get("minutes_summary", {})

    # dump meetings to json
    all_meetings = {}
    for entry in config["scrape"]:
        ind = Indico(category_id=entry["category"], years=entry["years"])
        for name, kwargs in entry["groups"].items():
            logging.info(f"Fetching contributions for {name}")
            meetings = ind.get_meetings(**kwargs)
            all_meetings[name] = meetings
            Path("json").mkdir(exist_ok=True)
            fpath = Path(f"json/{name}.json")
            with fpath.open("w") as f:
                meetings_dict = [asdict(m) for m in meetings.meetings]
                json.dump(meetings_dict, f, indent=4, default=str)
            logging.info(f"Saved to {fpath}")

    # meeting summaries
    for name, kwargs in summary_config.items():
        logging.info(f"Creating {name} summary")
        meetings = all_meetings[name]
        meetings.meeting_list_md(name=name, **kwargs)

    # add contribution tables
    logging.info("Adding topical contributions")
    for config in topical_config:
        cats = config.get("categories", list(all_meetings.keys()))
        meetings = sum((all_meetings[cat] for cat in cats[1:]), all_meetings[cats[0]])
        meetings.add_topic(
            target=config["target"],
            include=config["include"],
            exclude=config.get("exclude"),
        )

    # add minutes tables
    for name, config in minutes_config.items():
        logging.info(f"Adding minutes to {config['target']}")
        all_meetings[name].minutes_md(name=name, target=config["target"])


if __name__ == "__main__":
    main()
