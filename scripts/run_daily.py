from competition_intel.pipeline import run_once
from competition_intel.settings import CONFIG_PATH


def main() -> None:
    result = run_once(CONFIG_PATH)
    print(result)


if __name__ == "__main__":
    main()
