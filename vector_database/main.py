import argparse
from Vector_Database import add_dataset, search

def main():
    parser = argparse.ArgumentParser(
        description="Add Hugging‑Face datasets to Pinecone & run semantic searches"
    )
    parser.add_argument(
        "--add",
        help="Name of a Hugging‑Face dataset to load and index (e.g. 'gbharti/finance-alpaca')",
        type=str
    )
    parser.add_argument(
        "--query",
        help="A free‑form text query to search your Pinecone index",
        type=str
    )
    parser.add_argument(
        "--top_k",
        help="Number of results to return",
        type=int,
        default=5
    )
    args = parser.parse_args()

    if args.add:
        add_dataset(args.add)

    if args.query:
        search(args.query, top_k=args.top_k)

if __name__ == "__main__":
    main()