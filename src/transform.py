import json
import pandas as pd

from clean_columns import clean_column_names
from clean_numeric import clean_numeric_columns
from handling_date import create_report_date

import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")

def transform():
    with open("../data/extracted_data.json", "r") as f:
        df = pd.json_normalize(json.load(f))

    df = clean_column_names(df)
    df = clean_numeric_columns(df, exclude=("company", "file", "month_name"))
    df = create_report_date(df)

    df.drop(columns=["month_name", "file"], inplace=True)

    df.to_csv("../data/transform_data.csv", index=False)
    print("transformation complete.")

if __name__ == "__main__":
    transform()