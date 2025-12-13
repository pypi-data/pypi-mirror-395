from .qython.docs_api import get_documentation, list_available_topics

def qython_help(topic: str = "home") -> str:
    """You MUST use this tool whenever the user asks you to do ANYTHING with Qython."""
    return get_documentation(topic)