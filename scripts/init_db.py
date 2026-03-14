from competition_intel.pipeline import bootstrap_sources
from competition_intel.settings import CONFIG_PATH


def main() -> None:
    bootstrap_sources(CONFIG_PATH)
    print("database initialized and sources synced")


if __name__ == "__main__":
    main()
