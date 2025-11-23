# Mangalore Tourism Knowledge Graph (Neo4j + Python)

This repository contains a complete pipeline for building and querying a **Knowledge Graph (KG)** for Mangalore tourism using **Neo4j** and **Python**.

It covers:

* Cleaning structured data (cities, attributes, etc.)
* Loading the knowledge graph into Neo4j
* Converting natural language questions into Cypher queries
* Running queries and retrieving results

---

## 1. Project Structure

```
.
├── load_kg_to_neo4j.py     # Builds and inserts the KG into Neo4j
├── kg_query.py             # Helper to run Cypher queries
├── ask_kg.py               # Natural-language querying interface
├── clean_travel_dataset.json  # Clean structured tourism dataset
├── nl_to_cypher.py         # NL → Cypher converter
└── README.md
```

---

## 2. Requirements

### Dependencies

Install using pip:

```
pip install neo4j
```

If you use embeddings/LLMs later:

```
pip install sentence-transformers langchain
```

---

## 3. Neo4j Setup Guide

### Step 1 — Install Neo4j

Download from: [https://neo4j.com/download/](https://neo4j.com/download/)

### Step 2 — Create a database

* Database name: **kg12**
* Bolt URL: **bolt://127.0.0.1:7687**
* Username: **neo4j**
* Password: **RishalRishal**

> If you change username/password, update it in all Python files.

### Step 3 — Install APOC (optional)

Useful for advanced graph operations.

---

## 4. Load Knowledge Graph into Neo4j

Ensure the dataset exists:

```
clean_travel_dataset.json
```

Run:

```
python load_kg_to_neo4j.py
```

This script:

* Connects to Neo4j
* Creates City, Country, Region, and Attribute nodes
* Creates relationships
* Inserts all entries from the JSON

---

## 5. Query the Knowledge Graph (Direct Cypher)

Run:

```
python kg_query.py
```

What it does:

* Provides `run_cypher(query)`
* Connects to Neo4j
* Returns matching records

---

## 6. Ask Questions in Natural Language

Run:

```
python ask_kg.py
```

Example question:

```
show me cities with good nightlife
```

Pipeline:

1. Question →
2. Converted to Cypher by `nl_to_cypher()` →
3. Query executed →
4. Results printed

---

## 7. Expected Dataset Structure

Your `clean_travel_dataset.json` should follow:

```
[
  {
    "city": "Mangalore",
    "country": "India",
    "region": "Karnataka",
    "budget_level": "medium",
    "culture": "high",
    "nature": "high",
    "adventure": "medium",
    "nightlife": "low"
  }
]
```

---

## 8. Knowledge Graph Structure

### Node Types

| Label     | Example        |
| --------- | -------------- |
| City      | Mangalore      |
| Country   | India          |
| Region    | Karnataka      |
| Attribute | nightlife_high |

### Relationships

| Relationship                             | Meaning                       |
| ---------------------------------------- | ----------------------------- |
| `(:City)-[:LOCATED_IN]->(:Country)`      | City is in a country          |
| `(:Country)-[:PART_OF]->(:Region)`       | Country is part of region     |
| `(:City)-[:HAS_ATTRIBUTE]->(:Attribute)` | Attribute describing the city |

---

## 9. Natural Language Workflow

Example:

```
What cities have high nature score?
```

Becomes Cypher:

```
MATCH (c:City)-[:HAS_ATTRIBUTE]->(a:Attribute {type: "nature", value: "high"})
RETURN c.name;
```

---

## 10. Troubleshooting

### Neo4j connection error

Check:

```
neo4j status
```

Ensure:

* DB name = kg12
* Bolt URL active
* Password correct

### No results returned

Run:

```
MATCH (n) RETURN count(n);
```

Should be > 0.

### nl_to_cypher missing

Ensure:

```
nl_to_cypher.py
```

exists.

---
