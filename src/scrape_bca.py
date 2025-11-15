import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.bca.co.id"
PAGE_URL = "https://www.bca.co.id/id/tentang-bca/Hubungan-Investor/laporan-presentasi/Laporan-Keuangan"

# Common browser header to avoid 403
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_html(url: str) -> str:
    """Fetch page HTML with request headers."""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text


def parse_report_table(html: str) -> list:
    """
    Extract financial report rows and PDF URLs.
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("tbody.m-table.m-table--report tr")

    results = []
    for row in rows:
        title = row.select_one("p.a-text").get_text(strip=True)
        pdf_rel = row.select_one("input[data-file]")["data-file"]
        pdf_url = BASE_URL + pdf_rel

        results.append({"title": title, "url": pdf_url})

    return results


def download_pdf(url: str, save_path: str) -> None:
    """Download a PDF file with headers."""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    with open(save_path, "wb") as f:
        f.write(response.content)


def scrape_and_download() -> None:
    """Main execution: fetch page, extract PDFs, download them."""
    os.makedirs("../data/downloads", exist_ok=True)

    html = fetch_html(PAGE_URL)
    reports = parse_report_table(html)

    for rpt in reports:
        filename = rpt["url"].split("/")[-1]
        out_path = os.path.join("../data/downloads", filename)
        download_pdf(rpt["url"], out_path)


if __name__ == "__main__":
    scrape_and_download()