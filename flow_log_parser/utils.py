import os

def file_exists(filepath):
    """
    Check if a file exists.
    
    :param filepath: Path to the file.
    :return: True if the file exists; False otherwise.
    """
    return os.path.exists(filepath)
