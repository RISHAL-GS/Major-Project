from neo4j import GraphDatabase
from nl_to_cypher import nl_to_cypher

URI = "bolt://127.0.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "RishalRishal"
DATABASE = "kg12"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

def query_kg(question):
    cypher = nl_to_cypher(question)
    print("\nGenerated Cypher:")
    print(cypher)

    with driver.session(database=DATABASE) as session:
        result = session.run(cypher)
        return [r for r in result]


if __name__ == "__main__":
    while True:
        q = input("\nAsk something about Mangalore tourism: ")
        ans = query_kg(q)
        print("Answer:", ans)
