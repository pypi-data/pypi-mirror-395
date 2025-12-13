from langgraph.graph import StateGraph as StateGraph

def create_edge(graph: StateGraph, sources: str | list[str], target: str) -> None:
    """Create edges from source nodes to target node in the graph.

    Special handling:
    - START cannot participate in a fan-in. If present, add a direct START -> target edge
      separately and only fan-in non-START sources.

    Args:
        graph (StateGraph): The graph to add edges to.
        sources (str | list[str]): The source nodes. If str or list of 1 element,
            connect directly. If list > 1 elements, use the list for fan-in. If empty list,
            do nothing.
        target (str): The target node.
    """
