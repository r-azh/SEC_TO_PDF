## SEC 10‑K PDF downloader

This project fetches the latest **10‑K** filing for a predefined list of companies from **SEC EDGAR**, downloads the main HTML filing, and renders it to **PDF** using **Playwright/Chromium**.

### What it produces
- **Output**: PDF files named like `Apple_10K_report.pdf`, `Amazon_10K_report.pdf`, etc.
- **Output directory**: controlled by `OUTPUT_PATH` (defaults to `output/`)

### Configuration (environment variables)
- **`OUTPUT_PATH`**: directory where PDFs are written

## Run locally (Windows / sh)

### Using a virtual environment + pip

From the repo root:

```sh
uv sync
uv run python main.py
```

PDFs will be written under `output\`.

## Run with Docker (recommended for Playwright)

### Build

From the repo root:
```sh
docker build -t sec_gov_10k_pdf .

```

### Run (write PDFs to a mounted volume)

This writes PDFs into a local `output/` folder via a Docker volume mount.

```sh
mkdir output
docker run --rm \
  -v ${PWD}\output:/output \
  quartr-task
```

After it finishes, check `.\output\` for the generated PDFs.


