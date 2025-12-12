import chromadb
import os

# --- CONFIGURATION ---
# Use the hardcoded path that worked for you previously
REAL_DB_PATH = r"E:\Lakshya\Columbia MSDS\Projects\AML\Financial-RAG-Chatbot\image\backend\data\indexes\chroma"
COLLECTION_NAME = "financial_docs"

print(f"🔍 Connecting to database at: {REAL_DB_PATH}")

# 1. Verify Path
if not os.path.exists(REAL_DB_PATH):
    print("❌ Error: The path does not exist!")
    exit(1)
    
print("✅ Path found.")

# 2. Initialize Client
try:
    client = chromadb.PersistentClient(path=REAL_DB_PATH)
    collection = client.get_collection(COLLECTION_NAME)
    print(f"✅ Connected to collection: '{COLLECTION_NAME}'")
    print(f"📊 Total Documents in DB: {collection.count()}")
except Exception as e:
    print(f"❌ Error connecting to ChromaDB: {e}")
    exit(1)

# 3. --- THE AMAZON TEST ---
print("\n--- 🕵️ TESTING FOR AMAZON DATA ---")

# Test A: Lowercase 'amzn'
print("👉 Querying for ticker='amzn' (lowercase)...")
results_lower = collection.get(where={"ticker": "amzn"}, limit=5)
count_lower = len(results_lower['ids'])
print(f"   Found: {count_lower} documents")

# Test B: Uppercase 'AMZN'
print("👉 Querying for ticker='AMZN' (uppercase)...")
results_upper = collection.get(where={"ticker": "AMZN"}, limit=5)
count_upper = len(results_upper['ids'])
print(f"   Found: {count_upper} documents")

# 4. --- REPORT & DIAGNOSIS ---
print("\n--- 📝 DIAGNOSIS REPORT ---")

if count_lower > 0:
    print("✅ SUCCESS: Amazon data exists as 'amzn' (lowercase).")
    print("   Sample Metadata:", results_lower['metadatas'][0])
elif count_upper > 0:
    print("✅ SUCCESS: Amazon data exists as 'AMZN' (uppercase).")
    print("   Sample Metadata:", results_upper['metadatas'][0])
    print("⚠️  WARNING: Your Lambda code might be using .lower(). Update it to use uppercase!")
else:
    print("❌ FAILURE: Zero documents found for Amazon.")
    print("   This confirms the data is physically missing from this specific folder.")
    print("   Action: You must run your ingestion script (build_index.py) for AMZN again.")