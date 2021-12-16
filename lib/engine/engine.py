from sqlalchemy import create_engine
from sqlalchemy.engine.reflection import Inspector

import networkx as nx
import matplotlib.pyplot as plt

from loguru import logger
import re
from .node import Node, NodeType

# global, dot matches new lines
regex = r"(.*?)CREATE VIEW(.*?)AS(.*?)SELECT(.*?)FROM(.*?)(WHERE (.*?))?(GROUP BY(.*?)$|$)"
prog = re.compile(regex, re.IGNORECASE|re.DOTALL)

class Engine:
  def __init__(self, db_connstring: str) -> None:
    self._engine = create_engine(db_connstring)
    self._engine.connect()
    self._dag = nx.DiGraph(name="Data DAG")



  def _add_edges(self, source_node_string: str, inserting_node: Node) -> None:
    for source in source_node_string.split(","):
      connected_node = None
      if not self._dag.has_node(source):
        inspector = Inspector.from_engine(self._engine)
        if source in inspector.get_table_names():
          connected_node = Node(source, NodeType.DB)
          self._dag.add_node(connected_node)
        else:
          raise ValueError("Node is not present in the database")
      else:
        connected_node = self._dag[Node(source)]
      self._dag.add_edge(connected_node, inserting_node)


  def print_dag(self):
    nx.draw_networkx(self._dag, None, True)
    plt.show()

  def update_dag(self, query: str) -> bool:
    match = prog.match(query)
    if not match:
      raise ValueError("Query is not valid")
    groups = match.groups()
    if (not groups[1] or not groups[4]) or (groups[1].strip() == "" or groups[4].strip() == ""):
      raise ValueError("Query is not valid")
    inserting_node = groups[1].strip()
    source_nodes = groups[4].strip()
    logger.info(f"Requesting to create node with name {inserting_node} taking as source {source_nodes}")
    if self._dag.has_node(inserting_node):
      raise NotImplementedError("Node already present, the query should be substituted")
    node = Node(inserting_node, NodeType.STATEFUL)
    self._dag.add_node(node)
    self._add_edges(source_nodes, node)


