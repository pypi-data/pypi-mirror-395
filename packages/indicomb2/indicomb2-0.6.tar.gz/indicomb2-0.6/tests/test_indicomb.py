from pathlib import Path

from indicomb2.indicomb2 import main


def test_indicomb():
    example_config = Path(__file__).parents[1] / "example.yaml"
    args = ["--config", str(example_config)]
    main(args)


if __name__ == "__main__":
    test_indicomb()
