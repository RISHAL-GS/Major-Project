from neo4j import GraphDatabase

URI = "bolt://127.0.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "RishalRishal"
DATABASE = "kg12"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

def run_cypher(query, params=None):
    with driver.session(database=DATABASE) as session:
        result = session.run(query, params or {})
        return [record.data() for record in result]
