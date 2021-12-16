from __future__ import annotations
from enum import Enum

class NodeType(Enum):
  STATELESS = "STATELESS"
  STATEFUL = "STATEFUL"
  DB = "DB"


class Node:
  def __eq__(self, __o: Node) -> bool:
      return __o and self._name == __o._name

  def __hash__(self) -> int:
      return hash(self._name)
  
  def __repr__(self) -> str:
      return f"{self._name} ~ {str(self._node_type.value)}"

  def __init__(self, name: str, node_type: NodeType) -> None:
      self._name = name
      self._node_type = node_type
