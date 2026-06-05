import os
import zipfile
import pandas as pd
from pathlib import Path
from pymongo import MongoClient

zip_file = "Viator_25_05_2026.zip"
mongo_uri = "mongodb://192.168.1.52:27017"
db_name = "xwiz_viator_project"

client = MongoClient(mongo_uri)
db = client[db_name]
extract_path = Path("Viator_Extracted")

# Extract ZIP
with zipfile.ZipFile(zip_file, "r") as zip_ref:
    zip_ref.extractall(extract_path)

excel_files = list(extract_path.rglob("*.xlsx"))
print("Files found:", excel_files)
for file in excel_files:
    day_name = file.stem.lower().replace("viator_input_file_", "")
    collection_name = f"inputs_for_{day_name}"

    print(f"\n📥 Processing {file.name} → Collection: {collection_name}")

    # ✅ Read Excel
    df = pd.read_excel(file)

    # 🔍 DEBUG: check rows
    print(f"👉 Rows found: {len(df)}")

    df.columns = [col.replace("Nº PAX", "pax") for col in df.columns]
    df["Status"] = "Pending"

    data = df.to_dict(orient="records")

    if data:
        db[collection_name].delete_many({})
        db[collection_name].insert_many(data)
        print(f"✅ Inserted {len(data)} records into {collection_name}")
    else:
        print(f"⚠️ No data found in {file.name}")

print("\n🎉 All files uploaded successfully into MongoDB!")
print(f"Database: {db_name}")