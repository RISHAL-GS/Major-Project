# Personalized LLM with FAISS and Sentence Transformers

## 📌 Overview
This project demonstrates how to build a personalized semantic search engine using vector databases. It integrates multiple tools to allow fast and accurate retrieval of similar text prompts across multiple datasets. Ideal for building personalized LLM applications where efficient query-response mapping is essential.

### 🎯 Project Goals
- Load and manage multiple instruction-based datasets
- Convert text prompts into dense vector embeddings using Sentence Transformers
- Index and search efficiently using FAISS
- Maintain metadata to trace back search results to original datasets

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone <https://github.com/RISHAL-GS/Major-Project>
cd <your-repo-folder>
```

### 2. Python Environment
Make sure you are using Python 3.8+ and it's recommended to create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
Install required libraries:
```bash
pip install datasets
pip install sentence-transformers
pip install faiss-cpu   # Use faiss-gpu if you have a CUDA-enabled GPU
pip install numpy
```
Optionally, you can add them to a `requirements.txt` and install via:
```bash
pip install -r requirements.txt
```

---

## 🧠 Technologies Used
| Tool                  | Purpose                                       |
|-----------------------|-----------------------------------------------|
| Hugging Face Datasets | Load and manage datasets                      |
| Sentence Transformers | Convert text to embeddings                    |
| FAISS                 | Fast Approximate Nearest Neighbor Search      |
| NumPy                 | Array and matrix operations                   |

---

## 🗂️ File Structure
```
/your-repo-folder
├── main.py              # Main script to load datasets, encode, search
├── README.md            # Project documentation
└── requirements.txt     # Dependency list
```

---

## ➕ Adding Datasets
To add a dataset:
```python
add_dataset("gbharti/finance-alpaca")
```
> Once successfully added and indexed, **comment it out** to avoid duplicate entries:
```python
# add_dataset("gbharti/finance-alpaca")
```
Repeat this for each new dataset.

### Data Format Requirement
Each dataset should follow this schema:
```json
{
  "instruction": "",
  "input": "",
  "output": ""
}
```

---

## 🔍 Performing a Search
Use the following command to perform a semantic search:
```python
search("How do interest rates affect the stock market?")
```
- Results will include the most similar instructions from all indexed datasets.
- Top 5 results are shown by default (can be adjusted via `top_k`).

---

## 💾 How It Works
1. **Add Dataset**:
   - Loads dataset from Hugging Face.
   - Combines `instruction` and `input` into a single prompt.
   - Embeds all prompts using `all-MiniLM-L6-v2`.
   - Stores embeddings in FAISS index.
   - Saves metadata to map back to the original dataset.

2. **Query Search**:
   - Encodes the input query.
   - Searches FAISS index for top-k similar vectors.
   - Retrieves original instruction/output from matched dataset using metadata.

---

## 📈 Example Output
```
📚 From dataset: gbharti/finance-alpaca
🔎 Instruction: Explain the impact of interest rates on inflation.
💡 Answer: Higher interest rates generally reduce inflation by ...
--------------------------------------------------
```

---

## 🧑‍💻 Contribution Guidelines
- Fork the repo
- Create a new branch (`feature-xyz`)
- Commit changes with clear messages
- Submit a Pull Request for review

---

## 📜 License
This project is licensed under the MIT License. Feel free to use and adapt.

---

## 🙏 Acknowledgements
- [Hugging Face](https://huggingface.co/)
- [Sentence Transformers](https://www.sbert.net/)
- [FAISS by Facebook AI](https://github.com/facebookresearch/faiss)

---

## 📬 Contact
For queries or collaboration, contact [Your Name] at [your-email@example.com]

---

