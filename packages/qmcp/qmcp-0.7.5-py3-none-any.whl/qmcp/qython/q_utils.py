import os

def get_q_qython_namespace_code() -> str:
    """
    Get the contents of the qython.q file containing Q runtime utilities.
    
    Returns:
        str: Contents of the qython.q file
        
    Raises:
        FileNotFoundError: If qython.q file is missing
        IOError: If file cannot be read
    """
    current_dir = os.path.dirname(__file__)
    qython_q_path = os.path.join(current_dir, 'qython.q')
    
    if not os.path.exists(qython_q_path):
        raise FileNotFoundError(f"Qython Q file not found: {qython_q_path}")
    
    try:
        with open(qython_q_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise IOError(f"Failed to read qython.q file from {qython_q_path}: {e}") from e