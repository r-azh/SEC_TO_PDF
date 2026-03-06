
import os

HEADERS = {
    "User-Agent": "QuartrTask admin_quartr_task@gmail.com",
}


SEC_SUBMISSIONS_URL = f"https://data.sec.gov/submissions/CIK{{cik}}.json"
SEC_ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data/"
SEC_CIK_REF_URL = "https://www.sec.gov/files/company_tickers.json"

OUTPUT_PATH = os.getenv("OUTPUT_PATH", "output")

Company_CIKs = {
    "Amazon": "0001018724",
    "Apple": "0000320193",
    "Meta": "0001326801",
    "Alphabet": "0001652044",
    "Netflix": "0001065280",
    "Goldman Sachs": "0000886982",
}


