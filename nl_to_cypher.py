from ollama import Client

client = Client()

def nl_to_cypher(question):
    prompt = f"""
You are an expert Cypher generator.

Convert the user question into a Cypher query.

IMPORTANT RULES:
- OUTPUT ONLY THE CYPHER QUERY.
- NO explanations
- NO markdown
- NO formatting
- NO backticks

Dataset structure:
- (:City {{name}})
- (:Country {{name}})
- (:Region {{name}})
- (:Attribute {{type, value}})
- (City)-[:HAS_ATTRIBUTE]->(Attribute)
- (City)-[:LOCATED_IN]->(Country)
- (Country)-[:PART_OF]->(Region)

User question: "{question}"

Return ONLY Cypher query:
"""

    response = client.generate(
        model="llama3.2:3b",
        prompt=prompt
    )

    return response['response'].strip()
