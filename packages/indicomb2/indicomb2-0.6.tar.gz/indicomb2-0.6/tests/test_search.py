from pathlib import Path

from indicomb2.search import main


def test_search():
    example_config = Path(__file__).parents[1] / "search.yaml"
    args = ["--config", str(example_config)]
    main(args)


if __name__ == "__main__":
    test_search()
