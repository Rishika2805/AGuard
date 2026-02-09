# graph/safe_node.py

from graph.logger import logger

def safe_node(fn):
    def wrapper(state):
        try:
            return fn(state)
        except Exception as e:
            logger.exception(f"Error in node {fn.__name__}: {e}")
            return {}
    return wrapper