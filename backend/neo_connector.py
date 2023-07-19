from neo4j import GraphDatabase
from faker import Faker
import random
from backend.custom_dataclasses import Definition, OrderedProperty, UnorderedProperty


class NeoConnector:
    def __init__(self) -> None:
        uri = "bolt://localhost:7687"
        username = ""
        password = ""
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def fill_defintions(self, definitions: list):
        with self.driver.session() as session:
            query = "MERGE (:Definition {name: $name, definition: $definition})"
            for definition in definitions:
                session.run(query, name=definition.value1, definition=definition.value2)

    def query_all_nodes_and_edges(self):
        with self.driver.session() as session:
            query = "MATCH (n)-[r]->(m) RETURN n, r, m"
            result = session.run(query)

            for record in result:
                node = record["n"]
                edge = record["r"]
                adjacent_node = record["m"]

                # Process the node, edge, and adjacent_node as desired
                # For example, print their properties
                print(f"Node: {node}")
                print(f"Edge: {edge}")
                print(f"Adjacent Node: {adjacent_node}")
                print("")

    def fill_neo4j_with_random_data(self, node_count, relationship_count):
        fake = Faker()

        with self.driver.session() as session:
            # Create nodes
            for _ in range(node_count):
                name = fake.name()
                age = random.randint(18, 65)
                session.run(
                    "CREATE (:Person {name: $name, age: $age})", name=name, age=age
                )

            # Create relationships
            for _ in range(relationship_count):
                session.run(
                    """
                    MATCH (a:Person), (b:Person)
                    WHERE a <> b
                    CREATE (a)-[:FRIEND]->(b)
                """
                )

        print("Data population complete.")
