# process_data.py
import pandas as pd
import sqlite3

# -----------------------------
# 1️⃣ Load the scraped data
# -----------------------------
try:
    df = pd.read_csv("quotes.csv")  # Change file name if your CSV has a different name
    print("✅ Loaded quotes.csv successfully.")
except FileNotFoundError:
    print("❌ quotes.csv not found! Please make sure the scraped file exists.")
    exit()

# -----------------------------
# 2️⃣ Basic data cleaning
# -----------------------------
# Remove leading/trailing spaces
if "author" in df.columns:
    df["author"] = df["author"].astype(str).str.strip()

# Fill missing tag values
if "tags" in df.columns:
    df["tags"] = df["tags"].fillna("").astype(str)

# -----------------------------
# 3️⃣ Handle list columns
# -----------------------------
# Convert any list-type columns (e.g., ['life', 'humor']) into semicolon-separated strings
for col in df.columns:
    df[col] = df[col].apply(lambda x: ";".join(x) if isinstance(x, list) else x)

# -----------------------------
# 4️⃣ Simple analysis examples
# -----------------------------
print("\n📊 Top 10 Authors:")
if "author" in df.columns:
    print(df["author"].value_counts().head(10))

print("\n🏷️ Top 20 Tags:")
if "tags" in df.columns:
    # Split tags (semicolon-separated) and count frequencies
    df["tag_list"] = df["tags"].astype(str).str.split(";")
    tags_exploded = df.explode("tag_list")
    tag_counts = tags_exploded["tag_list"].value_counts().head(20)
    print(tag_counts)

# -----------------------------
# 5️⃣ Save cleaned data
# -----------------------------
# Save cleaned CSV
df.to_csv("quotes_clean.csv", index=False, encoding="utf-8")
print("\n💾 Saved cleaned data to quotes_clean.csv")

# -----------------------------
# 6️⃣ Save to SQLite database
# -----------------------------
try:
    conn = sqlite3.connect("quotes.db")
    df.to_sql("quotes", conn, if_exists="replace", index=False)
    conn.close()
    print("💾 Saved cleaned data to quotes.db (SQLite database)")
except Exception as e:
    print("❌ Error saving to SQLite:", e)

print(f"\n✅ Data cleaning and saving complete. Total rows: {len(df)}")
