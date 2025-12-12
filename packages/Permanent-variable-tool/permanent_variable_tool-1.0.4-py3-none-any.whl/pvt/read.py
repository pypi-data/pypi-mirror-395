import os 
import inspect
 
def read(variable):
    """
    Reads and returns the content of a variable file from the 'pvt_data' subdirectory.
    
    Args:
        variable (str): Name of the variable file to read (without .var extension)
        
    Returns:
        str: Content of the file as a string
        
    Raises:
        FileNotFoundError: If the specified variable file doesn't exist
        
    Note:
        - Files are expected to be UTF-8 encoded
        - File path format: C:/pvt_data/{variable}.var
        - Empty files return empty string 
    """ 
    
    try:
        if not isinstance(variable, str):
            frame = inspect.currentframe().f_back  
            try:
                # 在当前作用域查找变量名
                for name, val in frame.f_locals.items(): 
                    if val is variable:
                        variable = name  # 替换为变量名
                        break 
                else:
                    variable = str(variable)  # 找不到则转为字符串 
            finally:
                del frame
    except:
        # 如果出现任何异常（如变量未定义），直接当作字符串
        variable = str(variable)
    
    path = os.path.join(f"C:\\pvt_data\\{variable}.var") 
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            output = f.read() 
            if output == "$value.false": 
                return False
            elif output == "$value.true": 
                return True 
            elif output == "$value.ellipsis": 
                return ...
            elif output == "$value.none": 
                return None
            elif output == "$value.notimplemented": 
                return NotImplemented
            else:
                return output 
    except FileNotFoundError as e:
        print(e)