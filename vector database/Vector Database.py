from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load the sentence transformer model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create FAISS index (L2 distance)
dimension = 384  # for MiniLM
index = faiss.IndexFlatL2(dimension)

# Keep metadata for mapping search results
metadata = []
dataset_store = {}  # To access original data by dataset name


def add_dataset(dataset_name):
    print(f"\n🔄 Adding dataset: {dataset_name}")
    
    # Load the dataset (train split)
    ds = load_dataset(dataset_name, split='train')
    dataset_store[dataset_name] = ds  # Save for lookup later

    # Build text prompts
    texts = [
        (row['instruction'] + " " + row['input']).strip()
        for row in ds
    ]

    # Generate embeddings
    vectors = model.encode(texts, show_progress_bar=True)

    # Add to FAISS index
    index.add(np.array(vectors))

    # Save metadata to map vector positions
    meta = [{"dataset": dataset_name, "index": i} for i in range(len(ds))]
    metadata.extend(meta)

    print(f"✅ {len(texts)} entries added from {dataset_name}.")



#add_dataset("gbharti/finance-alpaca")
# add_dataset("your/second-dataset")  ← Just do this for more datasets

# === Search Example ===
def search(query, top_k=5):
    query_vec = model.encode([query])
    distances, indices = index.search(np.array(query_vec), k=top_k)

    for idx in indices[0]:
        meta = metadata[idx]
        ds_name = meta['dataset']
        row_index = meta['index']
        row = dataset_store[ds_name][row_index]

        print(f"\n📚 From dataset: {ds_name}")
        print("🔎 Instruction:", row["instruction"])
        print("💡 Answer:", row["output"])
        print("-" * 50)


# === Example Query ===
search("How do interest rates affect the stock market?")
