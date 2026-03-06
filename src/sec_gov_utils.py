import os
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from src.constants import Company_CIKs, HEADERS, SEC_SUBMISSIONS_URL, OUTPUT_PATH, SEC_ARCHIVE_URL
from src.pdf_utils import close_browser, convert_to_pdf_async, get_browser_async


def extract_10k_ix_url_from_index(index_url: str, headers: dict):
    """
    From an index URL like:
        https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm
    return the file-name and link like:
      ("aapl-20250927.htm",
       "https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/0000320193-25-000079-index.htm")
    """
    resp = requests.get(index_url, headers=headers)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # SEC index pages usually have the documents in table.tableFile
    table = soup.find("table", class_="tableFile")
    if not table:
        raise RuntimeError("Could not find documents table on index page")

    for row in table.find_all("tr")[1:]:  # skip header
        cells = row.find_all("td")
        if len(cells) < 4:
            continue

        # Column layout is: [Seq, Description, Document, Type, Size , ...]
        doc_cell = cells[2]
        type_cell = cells[3]

        doc_type = type_cell.get_text(strip=True)
        print(f"doc_type: {doc_type}")
        link_tag = doc_cell.find("a")
        print(f"link_tag: {link_tag}")
        if not link_tag:
            continue

        href = link_tag["href"]
        filename = link_tag.get_text(strip=True)

        # Pick the main 10‑K HTML document
        if doc_type.startswith("10-K") and filename.endswith(".htm"):
            doc_url = urljoin(index_url, href)  # absolute URL
            return filename, doc_url

    raise RuntimeError("Could not find 10-K HTML document on index page")


def get_latest_10k_index_url(company_name):
    """
    From Sec.gov submissions link, get the latest 10k report index link
    """
    cik = Company_CIKs[company_name]
    url = SEC_SUBMISSIONS_URL.format(cik=cik)
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    filings = data["filings"]["recent"]["form"]
    accession_numbers = data["filings"]["recent"]["accessionNumber"]

    for i, form_type in enumerate(filings):
        if form_type == "10-K":
            latest_10k_accession = accession_numbers[i]
            accession_formatted = latest_10k_accession.replace("-", "")
            latest_index_url = f"{SEC_ARCHIVE_URL}{cik}/{accession_formatted}/{latest_10k_accession}-index.htm"
            return latest_index_url

    return None


async def get_latest_10k_report_pdf():
    print("starting fetch and convert loop")

    os.makedirs(OUTPUT_PATH, exist_ok=True)

    # open a single browser instance to reuse across companies
    p, browser = await get_browser_async()

    try:
        for company in Company_CIKs.keys():
            print(f"=== processing {company} ===")
            latest_index_url = get_latest_10k_index_url(company)
            print(f"fetched index URL: {latest_index_url}")

            print(f"fetching 10K report file for {company}")
            filename, file_link = extract_10k_ix_url_from_index(latest_index_url, HEADERS)
            print(f"fetched filename: {filename}")
            print(f"fetched file link: {file_link}")

            file_link = file_link.replace("ix?doc=/", "")
            response = requests.get(file_link, headers=HEADERS)
            latest_10k_htm = response.text

            print(f"writing 10K report file to {OUTPUT_PATH}{os.sep}{company}_10K_report.pdf")
            await convert_to_pdf_async(
                html=latest_10k_htm,
                 output_path=f"{OUTPUT_PATH}{os.sep}{company}_10K_report.pdf"
                 )

            time.sleep(0.2)  # 200ms delay between requests
    finally:
        await close_browser(p, browser)
        print("done")


# This function was used to get CIK for the companies in constants.py for the first time
def get_cik(company_names):
    def find_cik(company_name, data):
        for item in data.values():
            if company_name.lower() in item["title"].lower():
                return f"{item['cik_str']:010d}"  # Format with leading zeros
        return None

    response = requests.get(SEC_CIK_REF_URL, headers=HEADERS)
    data = response.json()

    for company_name in company_names:
        cik = find_cik(company_name, data)
        if cik:
            print(f"\"{company_name}\": \"{cik}\"")
            return cik
        else:
            print(f"CIK for {company_name} not found.")
            return None

