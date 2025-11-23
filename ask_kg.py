from neo4j import GraphDatabase
from nl_to_cypher import nl_to_cypher
from ollama import Client

client = Client()

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "RishalRishal"
DATABASE = "kg12"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


# ----------------------------------------------------
# Run Cypher Safely
# ----------------------------------------------------
def run_cypher(query):
    try:
        with driver.session(database=DATABASE) as session:
            result = session.run(query)
            return result.data()
    except Exception as e:
        return {"error": str(e)}


# ----------------------------------------------------
# Convert KG raw output into natural language
# ----------------------------------------------------
def format_answer(question, cypher, kg_output):
    prompt = f"""
You are an AI that converts Neo4j knowledge graph results into friendly natural-language answers.

RULES:
- Be short, clear, factual.
- If KG output is empty -> say: "No information found in the knowledge graph."
- DO NOT mention Cypher.
- DO NOT mention Neo4j.
- Use the context from the question.

User question:
{question}

Cypher query:
{cypher}

Knowledge graph result:
{kg_output}

Write the best possible answer:
"""

    response = client.generate(
        model="llama3.2:3b",
        prompt=prompt
    )

    return response["response"].strip()


# ----------------------------------------------------
# Full Query Pipeline
# ----------------------------------------------------
def query_kg(user_query):

    print("\n----------- Generating Cypher -----------")
    cypher = nl_to_cypher(user_query)
    print(cypher)
    print("-----------------------------------------\n")

    kg_output = run_cypher(cypher)

    if isinstance(kg_output, dict) and "error" in kg_output:
        print("❌ Neo4j Error:", kg_output["error"])
        return

    final_answer = format_answer(user_query, cypher, kg_output)

    print("\nAnswer:", final_answer)
    return final_answer


# ----------------------------------------------------
# CLI Interface
# ----------------------------------------------------
if __name__ == "__main__":
    print("Ask something about your Travel Knowledge Graph:")

    while True:
        q = input("\n> ")

        if q.lower() in ["exit", "quit", "bye"]:
            print("\nGoodbye!")
            break

        query_kg(q)
