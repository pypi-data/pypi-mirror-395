import json
import os
from pathlib import Path
from typing import Dict, Any


def get_docs_path() -> Path:
    """Get the path to the qython documentation directory"""
    return Path(__file__).parent / "docs"


def get_documentation(topic: str = "home") -> str:
    """Get Qython documentation by topic
    
    Args:
        topic: Documentation topic filename (without extension)
        
    Returns:
        Markdown documentation content
        
    Raises:
        ValueError: If topic contains invalid characters or path traversal
        FileNotFoundError: If documentation file doesn't exist
    """
    # Security: prevent path traversal
    if ".." in topic or "/" in topic or "\\" in topic:
        raise ValueError(f"Invalid topic name: {topic}")
    
    # Only allow alphanumeric and basic characters
    if not topic.replace("_", "").replace("-", "").isalnum():
        raise ValueError(f"Invalid topic name: {topic}")
    
    docs_path = get_docs_path()
    
    # Special handling for "home" topic - combine multiple files
    if topic == "home":
        home_files = ["home.md", "home_numpy.md", "home_db.md"]
        contents = []
        
        for filename in home_files:
            file_path = docs_path / filename
            if file_path.exists():
                # Ensure the resolved path is still within the docs directory
                if not str(file_path.resolve()).startswith(str(docs_path.resolve())):
                    raise ValueError(f"Invalid file path: {filename}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        contents.append(f.read())
                except OSError as e:
                    raise ValueError(f"Could not read documentation file '{filename}': {e}")
        
        if not contents:
            raise FileNotFoundError(f"No home documentation files found")
        
        return '\n\n'.join(contents)
    
    # Regular handling for other topics
    md_file = docs_path / f"{topic}.md"
    
    if not md_file.exists():
        # List available topics
        available = [f.stem for f in docs_path.glob("*.md")]
        raise FileNotFoundError(f"Documentation topic '{topic}' not found. Available: {', '.join(available)}")
    
    # Ensure the resolved path is still within the docs directory (extra security)
    if not str(md_file.resolve()).startswith(str(docs_path.resolve())):
        raise ValueError(f"Invalid topic path: {topic}")
    
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            return f.read()
    except OSError as e:
        raise ValueError(f"Could not read documentation file '{topic}': {e}")

# def get_documentation_json(topic: str = "home") -> Dict[str, Any]:
#     """Get Qython documentation by topic (JSON format)
#     
#     Args:
#         topic: Documentation topic filename (without extension)
#         
#     Returns:
#         Dictionary containing the documentation content
#         
#     Raises:
#         ValueError: If topic contains invalid characters or path traversal
#         FileNotFoundError: If documentation file doesn't exist
#     """
#     # Security: prevent path traversal
#     if ".." in topic or "/" in topic or "\\" in topic:
#         raise ValueError(f"Invalid topic name: {topic}")
#     
#     # Only allow alphanumeric and basic characters
#     if not topic.replace("_", "").replace("-", "").isalnum():
#         raise ValueError(f"Invalid topic name: {topic}")
#     
#     docs_path = get_docs_path()
#     json_file = docs_path / f"{topic}.json"
#     
#     if not json_file.exists():
#         # List available topics
#         available = [f.stem for f in docs_path.glob("*.json")]
#         raise FileNotFoundError(f"Documentation topic '{topic}' not found. Available: {', '.join(available)}")
#     
#     # Ensure the resolved path is still within the docs directory (extra security)
#     if not str(json_file.resolve()).startswith(str(docs_path.resolve())):
#         raise ValueError(f"Invalid topic path: {topic}")
#     
#     try:
#         with open(json_file, 'r', encoding='utf-8') as f:
#             return json.load(f)
#     except json.JSONDecodeError as e:
#         raise ValueError(f"Invalid JSON in documentation file '{topic}': {e}")


def list_available_topics() -> Dict[str, str]:
    """List all available documentation topics
    
    Returns:
        Dictionary mapping topic names to their titles
    """
    docs_path = get_docs_path()
    topics = {}
    
    for json_file in docs_path.glob("*.json"):
        topic_name = json_file.stem
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                title = data.get('title', topic_name)
                topics[topic_name] = title
        except (json.JSONDecodeError, OSError):
            # Skip invalid files
            continue
    
    return topics