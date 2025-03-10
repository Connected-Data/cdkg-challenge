"""
Graph RAG with BAML + Kuzu
"""

import os

import kuzu
from dotenv import load_dotenv

from baml_client import b, reset_baml_env_vars, types

load_dotenv()
os.environ["BAML_LOG"] = "WARN"
reset_baml_env_vars(dict(os.environ))


def get_schema_dict(conn: kuzu.Connection) -> dict[str, list[dict]]:
    # Get schema for LLM
    nodes = conn._get_node_table_names()
    relationships = conn._get_rel_table_names()

    schema = {"nodes": [], "edges": []}

    for node in nodes:
        node_schema = {"label": node, "properties": []}
        node_properties = conn.execute(f"CALL TABLE_INFO('{node}') RETURN *;")
        while node_properties.has_next():
            row = node_properties.get_next()
            node_schema["properties"].append({"name": row[1], "type": row[2]})
        schema["nodes"].append(node_schema)

    for rel in relationships:
        edge = {
            "label": rel["name"],
            "src": rel["src"],
            "dst": rel["dst"],
            "properties": [],
        }
        rel_properties = conn.execute(f"""CALL TABLE_INFO('{rel["name"]}') RETURN *;""")
        while rel_properties.has_next():
            row = rel_properties.get_next()
            edge["properties"].append({"name": row[1], "type": row[2]})
        schema["edges"].append(edge)

    return schema


def get_schema_baml(conn: kuzu.Connection) -> str:
    schema = get_schema_dict(conn)
    lines = []

    # ALWAYS RESPECT THE RELATIONSHIP DIRECTIONS section
    lines.append("ALWAYS RESPECT THE EDGE DIRECTIONS:\n---")
    for edge in schema.get("edges", []):
        lines.append(f"(:{edge['src']}) -[:{edge['label']}]-> (:{edge['dst']})")
    lines.append("---")

    # NODES section
    lines.append("\nNode properties:")
    for node in schema.get("nodes", []):
        lines.append(f"  - {node['label']}")
        for prop in node.get("properties", []):
            ptype = prop["type"].lower()
            lines.append(f"    - {prop['name']}: {ptype}")

    # EDGES section (only include edges with properties)
    lines.append("\nEdge properties:")
    for edge in schema.get("edges", []):
        if edge.get("properties"):
            lines.append(f"- {edge['label']}")
            for prop in edge.get("properties", []):
                ptype = prop["type"].lower()
                lines.append(f"    - {prop['name']}: {ptype}")
    return "\n".join(lines)


class GraphRAG:
    def __init__(self, db_path="cdl_db"):
        self.db_path = db_path
        self.db = kuzu.Database(db_path)
        self.conn = kuzu.Connection(self.db)
        self.baml_schema = get_schema_baml(self.conn)

    def execute_query(self, question: str, cypher: str) -> types.Answer:
        """Use the generated Cypher statement to query the graph database."""
        response = self.conn.execute(cypher)
        result = []
        while response.has_next():
            item = response.get_next()
            if item not in result:
                result.extend(item)

        # Create a context object that RAGAnswerQuestion can use
        result_list = [x for i, x in enumerate(result) if x not in result[:i]]
        result_str = ", ".join(result_list)
        # Return the result as an Answer object
        return types.Answer(question=question, answer=result_str)

    def run(self, question: str) -> dict[str, str]:
        cypher = b.RAGText2Cypher(self.baml_schema, question)

        result = {
            "question": question,
            "cypher": cypher.query if cypher else "N/A",
            "response": "N/A",
        }
        # Query the database
        if cypher:
            query_response = self.execute_query(question, cypher.query)
            r = b.RAGAnswerQuestion(question, query_response.answer)
            # Overwrite answer with the answer from the RAGAnswerQuestion function
            result["response"] = r.answer

        return result


if __name__ == "__main__":
    graph_rag = GraphRAG(db_path="cdl_db")

    question = "Who are the speakers whose talks have the tag 'rdf'? Return the speaker names as a numbered list."
    response = graph_rag.run(question)
    print(response)
    print("---")

    question = "Which speakers gave a talk whose title contains the term 'Knowledge Mesh'? Please give the talk's full title and the names of the speakers."
    response = graph_rag.run(question)
    print(response)
    print("---")

    question = "What was discussed in the talk by Paco Nathan?"
    response = graph_rag.run(question)
    print(response)
    print("---")

    question = "Can you tell me more about the event Connected Data World 2021?"
    response = graph_rag.run(question)
    print(response)
    print("---")
