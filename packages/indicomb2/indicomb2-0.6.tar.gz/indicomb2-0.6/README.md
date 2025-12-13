# indicomb2

Faster indicomb with MkDocs markdown support.
An alternative to the original [indicomb](https://gitlab.cern.ch/indicomb/indicomb).

This tool is fast enough to run in CI as your docs get built (say goodbye to your cron jobs!), and comes with MkDocs markdown support.

## Quick Start

Install the package:

```bash
pip install indicomb2
```

Set up a configuration file (see the [example](https://gitlab.cern.ch/indicomb/indicomb2/-/blob/main/example.yaml)):

```bash
indicomb2 -c my_config.yaml
```

## Features

You can configure `indicomb2` to perform several tasks:

1. **Scrape**: The `scrape` section grabs events from an Indico category and dumps them to JSON. This step is essential for all the other steps.

2. **Meeting Summaries**: The `meeting_summaries` section creates a dedicated page listing all selected meetings in the category. [View example](https://ftag.docs.cern.ch/meetings/algorithms/)

3. **Minutes Summary**: The `minutes_summary` section creates a dedicated page listing all minutes for selected meetings in the category. [View example](https://ftag.docs.cern.ch/meetings/algorithms-minutes/)

4. **Topical Contributions**: The `topical_contributions` section appends a table to an existing page with contributions matching specified keywords. [View example](https://ftag.docs.cern.ch/algorithms/taggers/GN2/#meeting-contributions)

## Setup Guide

1. Set up a CERN docs site: https://how-to.docs.cern.ch/
2. Add an environment variable `INDICO_API_TOKEN` with your token from https://indico.cern.ch/user/tokens/
3. Create a configuration file (see the [example](https://gitlab.cern.ch/indicomb/indicomb2/-/blob/main/example.yaml))
4. Run `indicomb2 -c my_config.yaml`

## Search (Work in Progress)

Instead of looking through events in a specified category, you can also search all of indico with

```bash
indisearch --config search.yaml 
```

see [search.yaml](search.yaml) and [search.py](src/indicomb2/search.py).
This needs a bit of improvement (figuring out a way to OR queries), but can be useful to highlight topical talks from accross many categories.
Forr example a list of talks about GPUs can be found [here](https://atlasml.web.cern.ch/atlasml/resources/hardware/#meeting-contributions).
