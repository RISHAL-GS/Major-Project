from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import pinecone 
import numpy as np
import uuid

# Initialize Pinecone
pinecone.init(api_key="pcsk_4Gqjyf_MpFsnmTaa7M9yNYPZnVoRYXPPmNev1mojR85EFt65UeASJ9BrXSrXrDGmDbegsi", environment="gcp-starter")  # or "us-west1-gcp" or check your Pinecone console
index = pinecone.Index("sacred-oak")

# Load the sentence transformer model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Local metadata store (optional, useful for display)
dataset_store = {}

def add_dataset(dataset_name):
    print(f"\n🔄 Adding dataset: {dataset_name}")
    
    # Load dataset (train split)
    ds = load_dataset(dataset_name, split='train')
    dataset_store[dataset_name] = ds

    # Build prompts
    texts = [(row['instruction'] + " " + row['input']).strip() for row in ds]
    vectors = model.encode(texts, show_progress_bar=True)

    # Prepare records for Pinecone upsert
    to_upsert = []
    for i, vec in enumerate(vectors):
        uid = f"{dataset_name}-{uuid.uuid4()}"
        metadata = {
            "dataset": dataset_name,
            "index": i,
            "instruction": ds[i]["instruction"],
            "output": ds[i]["output"]
        }
        to_upsert.append((uid, vec.tolist(), metadata))

    # Upsert to Pinecone
    index.upsert(vectors=to_upsert)
    print(f"✅ {len(to_upsert)} entries uploaded to Pinecone.")

def search(query, top_k=5):
    query_vector = model.encode([query])[0].tolist()
    results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)

    for match in results["matches"]:
        meta = match["metadata"]
        print(f"\n📚 From dataset: {meta.get('dataset', 'unknown')}")
        print("🔎 Instruction:", meta.get("instruction", ""))
        print("💡 Answer:", meta.get("output", ""))
        print("-" * 50)

# === Example Usage ===
add_dataset("gbharti/finance-alpaca")
search("How do interest rates affect the stock market?")
