from neo4j import GraphDatabase
import json

# Neo4j credentials
URI = "bolt://127.0.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "RishalRishal"
DATABASE = "kg12"     # <-- Your actual DB name

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

def get_session():
    return driver.session(database=DATABASE)

def test_connection():
    with get_session() as session:
        result = session.run("RETURN 'Connected to Neo4j!' AS message;")
        print(result.single()["message"])

test_connection()

def load_data(tx, city, country, region, attributes):
    # Create city node
    tx.run(
        "MERGE (c:City {name: $city})",
        city=city
    )

    # Create country node
    tx.run(
        "MERGE (co:Country {name: $country})",
        country=country
    )

    # Create region node
    tx.run(
        "MERGE (r:Region {name: $region})",
        region=region
    )

    # Create relationships
    tx.run(
        """
        MATCH (c:City {name: $city}), (co:Country {name: $country})
        MERGE (c)-[:LOCATED_IN]->(co)
        """,
        city=city, country=country
    )

    tx.run(
        """
        MATCH (co:Country {name: $country}), (r:Region {name: $region})
        MERGE (co)-[:PART_OF]->(r)
        """,
        country=country, region=region
    )

    # Insert attributes
    for attr, value in attributes.items():
        attr_node = f"{attr}_{value}"

        tx.run(
            "MERGE (a:Attribute {name: $attr_node, type: $type, value: $value})",
            attr_node=attr_node, type=attr, value=value
        )

        tx.run(
            """
            MATCH (c:City {name: $city}), (a:Attribute {name: $attr_node})
            MERGE (c)-[:HAS_ATTRIBUTE]->(a)
            """,
            city=city, attr_node=attr_node
        )

def build_kg():
    # FIX: use get_session() so database=kg12 is used
    with get_session() as session:
        with open("clean_travel_dataset.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            city = item["city"]
            country = item["country"]
            region = item["region"]

            attributes = {
                k: v for k, v in item.items()
                if k not in ["city", "country", "region"]
            }

            session.execute_write(
                load_data, city, country, region, attributes
            )

        print("Knowledge graph inserted into Neo4j successfully!")

build_kg()
