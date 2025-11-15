import re

def clean_column_names(df):
    """Clean column names: remove metadata./data., lowercase, underscores."""
    cleaned = {}
    for col in df.columns:
        # Remove prefixes "data." and "metadata."
        new_col = col.replace("metadata.", "").replace("data.", "")

        # Lowercase
        new_col = new_col.lower()

        # Replace spaces and special characters with underscores
        new_col = re.sub(r'[^a-z0-9]+', '_', new_col)

        # Remove trailing underscore
        new_col = new_col.strip('_')

        cleaned[col] = new_col

    return df.rename(columns=cleaned)