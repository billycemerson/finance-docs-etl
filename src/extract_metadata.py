import pdfplumber
import re

def extract_text_from_pdf(file_path: str) -> str:
    """Read the first page of a PDF file and return extracted text."""
    with pdfplumber.open(file_path) as pdf:
        first_page = pdf.pages[0]
        return first_page.extract_text()


def extract_company_name(text: str) -> str | None:
    """
    Extract company name using regex.
    Pattern example: 'PT ABC XYZ Tbk'
    """
    pattern = r"^(PT\s+.*?Tbk)"
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1) if match else None


def extract_report_date(text: str) -> dict | None:
    """
    Extract date information from text.
    Example matched pattern: 'Pada tanggal 31 Desember 2023'
    """
    pattern = r"Pada tanggal (\d{1,2}) (\w+) (\d{4})"
    match = re.search(pattern, text)

    if not match:
        return None

    # Extract components
    day = int(match.group(1))
    month_name = match.group(2)
    year = int(match.group(3))

    # Month mapping (Bahasa Indonesia → number)
    month_map = {
        "Januari": 1, "Februari": 2, "Maret": 3, "April": 4,
        "Mei": 5, "Juni": 6, "Juli": 7, "Agustus": 8,
        "September": 9, "Oktober": 10, "November": 11, "Desember": 12
    }

    month_number = month_map.get(month_name)

    return {
        "day": day,
        "month": month_number,
        "month_name": month_name,
        "year": year
    }


def extract_metadata(file_path: str) -> dict:
    """Main function to extract all metadata fields from the PDF."""
    text = extract_text_from_pdf(file_path)

    company = extract_company_name(text)
    date_info = extract_report_date(text)

    metadata = {
        "company": company,
        "year": date_info.get("year") if date_info else None,
        "month": date_info.get("month") if date_info else None,
        "month_name": date_info.get("month_name") if date_info else None,
    }

    return metadata


# Example Usage
# pdf_path = "../data/data-contoh.pdf"
# metadata = extract_metadata(pdf_path)
# print(metadata)