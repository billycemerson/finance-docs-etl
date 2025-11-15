import pandas as pd
from supabase_client import get_supabase_client

def load_to_supabase(csv_path="../data/transform_data.csv"):
    client = get_supabase_client()

    # Load CSV
    df = pd.read_csv(csv_path)

    # Ensure correct types
    df["report_date"] = pd.to_datetime(df["report_date"]).dt.strftime("%Y-%m-%d")

    int_columns = [
        "year",
        "month",
        "total_aset",
        "total_liabilitas",
        "total_ekuitas",
        "laba_rugi_bersih_periode_berjalan"
    ]

    for col in int_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # Insert each row
    for _, row in df.iterrows():
        payload = row.to_dict()

        # Check if record exists
        existing = (
            client.table("laporan_keuangan")
            .select("id")
            .eq("company", payload["company"])
            .eq("report_date", payload["report_date"])
            .execute()
        )

        if existing.data:
            print(f"Skipping (already exists): {payload['company']} - {payload['report_date']}")
            continue

        # Insert new row
        client.table("laporan_keuangan").insert(payload).execute()
        print(f"Inserted: {payload['company']} - {payload['report_date']}")

    print("\nLoading complete.")

if __name__ == "__main__":
    load_to_supabase()