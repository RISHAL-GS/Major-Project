from ollama import Client
from neo4j import GraphDatabase
import json

# -------------------------
# OLLAMA CLIENT
# -------------------------
client = Client()

# -------------------------
# NEO4J CONNECTION
# -------------------------
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "RishalRishal"
DATABASE = "kg12"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


# ---------------------------------------------------
# 1) EXTRACT LIVE DATABASE SCHEMA
# ---------------------------------------------------
def get_schema():
    with driver.session(database=DATABASE) as session:
        data = session.run("CALL db.schema.nodeTypeProperties()").data()
    return json.dumps(data, indent=2)


# ---------------------------------------------------
# 2) FEW-SHOT EXAMPLES (INCREASES ACCURACY)
# ---------------------------------------------------
FEW_SHOTS = [
    {
        "question": "What is the beaches rating of Milan?",
        "cypher": """MATCH (c:City {name: "Milan"})-[:HAS_ATTRIBUTE]->(a:Attribute)
WHERE a.type = "beaches"
RETURN a.value"""
    },
    {
        "question": "Show cities with nature score greater than 2",
        "cypher": """MATCH (c:City)-[:HAS_ATTRIBUTE]->(a:Attribute)
WHERE a.type = "nature" AND toInteger(a.value) > 2
RETURN c.name, a.value"""
    },
    {
        "question": "List all cities located in India",
        "cypher": """MATCH (c:City)-[:LOCATED_IN]->(co:Country {name: "India"})
RETURN c.name"""
    }
]


def format_few_shots():
    formatted = ""
    for ex in FEW_SHOTS:
        formatted += f"Q: {ex['question']}\nCypher: {ex['cypher']}\n\n"
    return formatted


# ---------------------------------------------------
# 3) MAIN NL → CYPHER CONVERSION FUNCTION
# ---------------------------------------------------
def nl_to_cypher(question):

    schema = get_schema()
    examples = format_few_shots()

    prompt = f"""
You are an expert Cypher-query generator. 
Your job is to convert natural language questions into VALID Neo4j Cypher queries.

Here is the LIVE Neo4j SCHEMA (DO NOT INVENT ANYTHING OUTSIDE THIS):
{schema}

Here are FEW-SHOT EXAMPLES to learn the format:
{examples}

RULES:
- Use EXACT node labels, properties, and relationship types from schema.
- Attribute values are strings → use toInteger(a.value) for numeric comparisons.
- Always return ONLY a Cypher query. No explanation.
- Never invent nodes or relationships.

USER QUESTION:
"{question}"

Generate the correct Cypher query:
"""

    response = client.generate(
        model="llama3.2:3b",
        prompt=prompt
    )

    return response["response"].strip()
