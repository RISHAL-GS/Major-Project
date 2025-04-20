# Import the dataset loading utility from the Hugging Face Datasets library
from datasets import load_dataset

# Load the "finance-alpaca" dataset (from Hugging Face) and use only the 'train' split
dataset = load_dataset("gbharti/finance-alpaca", split='train')  # Use split here

# Create a list of text prompts by combining the 'instruction' and 'input' fields for each item in the dataset
corpus = [
    (row['instruction'] + " " + row['input']).strip()
    for row in dataset
]

# Import the sentence transformer model
from sentence_transformers import SentenceTransformer

# Load a pre-trained sentence embedding model (compact and efficient)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Encode the corpus (list of combined instruction-input prompts) into vector embeddings
# This will show a progress bar as it processes the data
embeddings = model.encode(corpus, show_progress_bar=True)

# Import FAISS (Facebook AI Similarity Search) and NumPy for similarity search and array handling
import faiss
import numpy as np

# Get the dimensionality of the embedding vectors
dimension = embeddings.shape[1]

# Create a FAISS index for fast L2 (Euclidean) similarity search over the embeddings
index = faiss.IndexFlatL2(dimension)

# Add the encoded corpus embeddings to the FAISS index
index.add(np.array(embeddings))

# Define a query string that we want to search similar instructions for
query = "How do interest rates affect the stock market?"

# Encode the query into a vector using the same model
query_vector = model.encode([query])

# Search the FAISS index for the top 5 most similar vectors to the query vector
# Returns the distances and indices of the closest matches
distances, indices = index.search(np.array(query_vector), k=5)

# Loop through the top 5 matching indices and print the corresponding instruction and output (answer)
for i in indices[0]:
    print("Instruction:", dataset[i]['instruction'])  # Print the instruction part of the matched item
    print("Answer:", dataset[i]['output'])            # Print the output (answer) part
    print("-" * 50)                                   # Print a separator line for readability
