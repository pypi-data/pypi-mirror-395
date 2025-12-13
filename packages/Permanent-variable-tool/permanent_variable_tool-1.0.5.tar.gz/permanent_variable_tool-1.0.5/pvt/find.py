import os 

def find(variable):
    """ 
    Check if a variable data file exists in the specified directory.
    
    Args:
        variable: The name of the variable to look for (filename without extension)
    
    Returns:
        bool: True if the file exists and can be read, False if the file doesn't exist
        
    Note:
        The function constructs a file path in the format: C:\pvtData\{variable}.var 
        Only handles FileNotFoundError, other exceptions will propagate up 
    """
    try:
        path = os.path.join(f"C:\\pvt_data\\{variable}.var")
        with open(path, 'r', encoding='utf-8') as r:
            r.read()
            return True
    except FileNotFoundError:
        return False