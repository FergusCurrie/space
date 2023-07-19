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

    def fill_ordered_properties(self, ordered_properties: list[OrderedProperty]):
        with self.driver.session() as session:
            query = "MERGE (n:Concept {name: $name})"
            # cypher query to create two nodes and a relationship between them

            query_add_relationship = "MATCH(n:Concept) WHERE n.name = $ordered_name  MERGE (n)-[:property]->(p:OrderedProperty {name: $prop_name, number: $number})"
            for i, ordered_property in enumerate(ordered_properties):
                session.run(query, name=ordered_property.name)
                for prop in ordered_property.value:
                    # create relationship
                    session.run(
                        query_add_relationship,
                        prop_name=prop,
                        ordered_name=ordered_property.name,
                        number=i + 1,
                    )

    def fill_unordered_properties(self, unordered_properties: list[UnorderedProperty]):
        with self.driver.session() as session:
            query = "MERGE (n:Concept {name: $name})"
            # cypher query to create two nodes and a relationship between them

            query_add_relationship = "MATCH(n:Concept) WHERE n.name = $unordered_name  MERGE (n)-[:property]->(p:UnOrderedProperty {name: $prop_name})"
            for unordered_property in unordered_properties:
                session.run(query, name=unordered_property.name)
                for i, prop in enumerate(unordered_property.value):
                    # create relationship
                    session.run(
                        query_add_relationship,
                        prop_name=prop,
                        unordered_name=unordered_property.name,
                    )

    def query_all_nodes(self):
        with self.driver.session() as session:
            query = "MATCH (n) RETURN n"
            result = session.run(query)

            for record in result:
                node = record["n"]

                # Process the node, edge, and adjacent_node as desired
                # For example, print their properties
                print(f"Node: {node}")

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
