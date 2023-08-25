import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable


class App:

    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def add_tube_module(self, global_id, type_name='tube'):
        with self.driver.session() as session:
            session.execute_write(self.create_tube_node, global_id, type_name)

    @staticmethod
    # all the static methods are transaction functions
    def create_tube_node(tx, global_id, type_name):
        tx.run("CREATE (m:Tube_Module {global_id: $global_id, type_name: $type_name})",
               global_id=global_id, type_name=type_name)

    def add_basic_module(self, global_id, type_name='basic_module'):
        with self.driver.session() as session:
            session.execute_write(self.create_basic_node, global_id, type_name)

    @staticmethod
    # all the static methods are transaction functions
    def create_basic_node(tx, global_id, type_name):
        tx.run("CREATE (m:Basic_Module {global_id: $global_id, type_name: $type_name})",
               global_id=global_id, type_name=type_name)

    def add_corridor_module(self, global_id, type_name='corridor_module'):
        with self.driver.session() as session:
            session.execute_write(self.create_corridor_node, global_id, type_name)

    @staticmethod
    # all the static methods are transaction functions
    def create_corridor_node(tx, global_id, type_name):
        tx.run("CREATE (m:Corridor_Module {global_id: $global_id, type_name: $type_name})",
               global_id=global_id, type_name=type_name)

    def add_conjunctive_module(self, global_id, type_name='conjunctive_module'):
        with self.driver.session() as session:
            session.execute_write(self.create_conjunctive_node, global_id, type_name)

    @staticmethod
    # all the static methods are transaction functions
    def create_conjunctive_node(tx, global_id, type_name):
        tx.run("CREATE (m:Conjunctive_Module {global_id: $global_id, type_name: $type_name})",
               global_id=global_id, type_name=type_name)

    # add relationship between tube and basic modules
    def add_tube_basic_adjacency(self, global_id_a, global_id_b):
        with self.driver.session() as session:
            session.execute_write(self.tube_basic_relationship, global_id_a, global_id_b)

    @staticmethod
    def tube_basic_relationship(tx, global_id_a, global_id_b):
        tx.run("MATCH (a:Tube_Module {global_id: $global_id_a})"
               "MATCH (b:Basic_Module {global_id: $global_id_b})"
               "MERGE (a)-[:ADJOINS]-(b)",
               global_id_a=global_id_a, global_id_b=global_id_b)

    # add relationship between tube and conjunct modules
    def add_tube_conjunct_adjacency(self, global_id_a, global_id_b):
        with self.driver.session() as session:
            session.execute_write(self.tube_conjunct_relationship, global_id_a, global_id_b)

    @staticmethod
    def tube_conjunct_relationship(tx, global_id_a, global_id_b):
        tx.run("MATCH (a:Tube_Module {global_id: $global_id_a})"
               "MATCH (b:Conjunctive_Module {global_id: $global_id_b})"
               "MERGE (a)-[:ADJOINS]-(b)",
               global_id_a=global_id_a, global_id_b=global_id_b)

    # add relationship between tube and corridor modules
    def add_tube_corridor_adjacency(self, global_id_a, global_id_b):
        with self.driver.session() as session:
            session.execute_write(self.tube_corridor_relationship, global_id_a, global_id_b)

    @staticmethod
    def tube_corridor_relationship(tx, global_id_a, global_id_b):
        tx.run("MATCH (a:Tube_Module {global_id: $global_id_a})"
               "MATCH (b:Corridor_Module {global_id: $global_id_b})"
               "MERGE (a)-[:ADJOINS]-(b)",
               global_id_a=global_id_a, global_id_b=global_id_b)

    def add_basic_conjunct_adjacency(self, global_id_a, global_id_b):
        with self.driver.session() as session:
            session.execute_write(self.basic_conjunct_relationship, global_id_a, global_id_b)

    @staticmethod
    def basic_conjunct_relationship(tx, global_id_a, global_id_b):
        tx.run("MATCH (a:Basic_Module {global_id: $global_id_a})"
               "MATCH (b:Conjunctive_Module {global_id: $global_id_b})"
               "MERGE (a)-[:ADJOINS]-(b)",
               global_id_a=global_id_a, global_id_b=global_id_b)

    def add_corridor_basic_adjacency(self, global_id_a, global_id_b):
        with self.driver.session() as session:
            session.execute_write(self.corridor_basic_relationship, global_id_a, global_id_b)

    @staticmethod
    def corridor_basic_relationship(tx, global_id_a, global_id_b):
        tx.run("MATCH (a:Corridor_Module {global_id: $global_id_a})"
               "MATCH (b:Basic_Module {global_id: $global_id_b})"
               "MERGE (a)-[:ADJOINS]-(b)",
               global_id_a=global_id_a, global_id_b=global_id_b)

    def add_corridor_conjunct_adjacency(self, global_id_a, global_id_b):
        with self.driver.session() as session:
            session.execute_write(self.corridor_conjunct_relationship, global_id_a, global_id_b)

    @staticmethod
    def corridor_conjunct_relationship(tx, global_id_a, global_id_b):
        tx.run("MATCH (a:Corridor_Module {global_id: $global_id_a})"
               "MATCH (b:Conjunctive_Module {global_id: $global_id_b})"
               "MERGE (a)-[:ADJOINS]-(b)",
               global_id_a=global_id_a, global_id_b=global_id_b)

    def add_corridor_adjacency(self, global_id_a, global_id_b):
        with self.driver.session() as session:
            session.execute_write(self.corridor_relationship, global_id_a, global_id_b)

    @staticmethod
    def corridor_relationship(tx, global_id_a, global_id_b):
        tx.run("MATCH (a:Corridor_Module {global_id: $global_id_a})"
               "MATCH (b:Corridor_Module {global_id: $global_id_b})"
               "MERGE (a)-[:ADJOINS]-(b)",
               global_id_a=global_id_a, global_id_b=global_id_b)

    def add_basic_adjacency(self, global_id_a, global_id_b):
        with self.driver.session() as session:
            session.execute_write(self.basic_relationship, global_id_a, global_id_b)

    @staticmethod
    def basic_relationship(tx, global_id_a, global_id_b):
        tx.run("MATCH (a:Basic_Module {global_id: $global_id_a})"
               "MATCH (b:Basic_Module {global_id: $global_id_b})"
               "MERGE (a)-[:ADJOINS]-(b)",
               global_id_a=global_id_a, global_id_b=global_id_b)

    def add_conjunct_adjacency(self, global_id_a, global_id_b):
        with self.driver.session() as session:
            session.execute_write(self.conjunct_relationship, global_id_a, global_id_b)

    @staticmethod
    def conjunct_relationship(tx, global_id_a, global_id_b):
        tx.run("MATCH (a:Conjunctive_Module {global_id: $global_id_a})"
               "MATCH (b:Conjunctive_Module {global_id: $global_id_b})"
               "MERGE (a)-[:ADJOINS]-(b)",
               global_id_a=global_id_a, global_id_b=global_id_b)

    def add_tube_corridor_connectivity(self, global_id_a, global_id_b):
        with self.driver.session() as session:
            session.execute_write(self.tube_corridor_connectivity, global_id_a, global_id_b)

    @staticmethod
    def tube_corridor_connectivity(tx, global_id_a, global_id_b):
        tx.run("MATCH (a:Tube_Module {global_id: $global_id_a})"
               "MATCH (b:Corridor_Module {global_id: $global_id_b})"
               "MERGE (a)-[:CONNECTS]-(b)",
               global_id_a=global_id_a, global_id_b=global_id_b)

    def add_corridor_basic_connectivity(self, global_id_a, global_id_b):
        with self.driver.session() as session:
            session.execute_write(self.corridor_basic_connectivity, global_id_a, global_id_b)

    @staticmethod
    def corridor_basic_connectivity(tx, global_id_a, global_id_b):
        tx.run("MATCH (a:Corridor_Module {global_id: $global_id_a})"
               "MATCH (b:Basic_Module {global_id: $global_id_b})"
               "MERGE (a)-[:CONNECTS]-(b)",
               global_id_a=global_id_a, global_id_b=global_id_b)

    def add_corridor_conjunct_connectivity(self, global_id_a, global_id_b):
        with self.driver.session() as session:
            session.execute_write(self.corridor_conjunct_connectivity, global_id_a, global_id_b)

    @staticmethod
    def corridor_conjunct_connectivity(tx, global_id_a, global_id_b):
        tx.run("MATCH (a:Corridor_Module {global_id: $global_id_a})"
               "MATCH (b:Conjunctive_Module {global_id: $global_id_b})"
               "MERGE (a)-[:CONNECTS]-(b)",
               global_id_a=global_id_a, global_id_b=global_id_b)

    def add_basic_connectivity(self, global_id_a, global_id_b):
        with self.driver.session() as session:
            session.execute_write(self.basic_connectivity, global_id_a, global_id_b)

    @staticmethod
    def basic_connectivity(tx, global_id_a, global_id_b):
        tx.run("MATCH (a:Basic_Module {global_id: $global_id_a})"
               "MATCH (b:Basic_Module {global_id: $global_id_b})"
               "MERGE (a)-[:CONNECTS]-(b)",
               global_id_a=global_id_a, global_id_b=global_id_b)

    def add_basic_conjunct_connectivity(self, global_id_a, global_id_b):
        with self.driver.session() as session:
            session.execute_write(self.basic_conjunct_connectivity, global_id_a, global_id_b)

    @staticmethod
    def basic_conjunct_connectivity(tx, global_id_a, global_id_b):
        tx.run("MATCH (a:Basic_Module {global_id: $global_id_a})"
               "MATCH (b:Conjunctive_Module {global_id: $global_id_b})"
               "MERGE (a)-[:CONNECTS]-(b)",
               global_id_a=global_id_a, global_id_b=global_id_b)

    def add_conjunct_connectivity(self, global_id_a, global_id_b):
        with self.driver.session() as session:
            session.execute_write(self.conjunct_connectivity, global_id_a, global_id_b)

    @staticmethod
    def conjunct_connectivity(tx, global_id_a, global_id_b):
        tx.run("MATCH (a:Conjunctive_Module {global_id: $global_id_a})"
               "MATCH (b:Conjunctive_Module {global_id: $global_id_b})"
               "MERGE (a)-[:CONNECTS]-(b)",
               global_id_a=global_id_a, global_id_b=global_id_b)