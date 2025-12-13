import os 
import inspect
 
def delete(variable):
    """
    Deletes a variable file with the given name from the 'data' subdirectory.
    
    Args:
        variable (str): The name of the variable file to be deleted (without .var extension)
        
    Raises:
        FileNotFoundError: If the specified variable file doesn't exist
        
    Note:
        - The file should be located in a 'data' subdirectory of the current script's directory
        - Files should have the '.var' extension 
    """

    try:
        if not isinstance(variable, str):
            frame = inspect.currentframe().f_back 
            try:
                for name, val in frame.f_locals.items(): 
                    if val is variable:
                        variable = name
                        break
                else:
                    variable = str(variable)
            finally:
                del frame 
    except:
        variable = str(variable)
    
    path = os.path.join(f"C:\\pvt_data\\{variable}.var") 
    
    try:
        os.remove(path)  
    except FileNotFoundError as e:
        print(e)
