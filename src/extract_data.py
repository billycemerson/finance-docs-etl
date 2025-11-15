import camelot
import pandas as pd

def read_tables(file_path: str):
    """Read PDF and return Camelot tables"""
    tables = camelot.read_pdf(file_path, flavor='stream', pages="all")
    # for t in tables:
    #     print(t.parsing_report) # Use if want logging the report
    return tables


def extract_values_from_tables(tables, target_fields):
    """Extract required fields from Camelot tables and return dict"""
    results = {field: None for field in target_fields}  # prefill keys

    for tbl in tables:
        df = tbl.df

        for field in target_fields:
            mask = df.isin([field])

            if mask.any().any():
                row_index = mask.any(axis=1).idxmax()
                col_index = mask.any(axis=0).idxmax()

                value_col = col_index + 1
                if value_col < df.shape[1]:
                    results[field] = df.iat[row_index, value_col]

    return results

def extract_data(file_path):
    target_fields = [
        "TOTAL ASET",
        "TOTAL LIABILITAS",
        "TOTAL EKUITAS",
        "LABA (RUGI) BERSIH PERIODE BERJALAN",
    ]

    tables = read_tables(file_path)
    results = extract_values_from_tables(tables, target_fields)
    return results

# Example Usage
# pdf_path = "../data/data-contoh.pdf"
# data = extract_data(pdf_path)
# print(data)