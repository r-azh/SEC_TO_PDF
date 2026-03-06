import asyncio

from src.sec_gov_utils import get_latest_10k_report_pdf


def main():
    asyncio.run(get_latest_10k_report_pdf())


if __name__ == "__main__":
    main()
