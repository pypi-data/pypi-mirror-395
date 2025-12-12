import os 
import inspect
 
def new(variable, value=None):
    """
    Creates a new variable file with optional value in the 'data' subdirectory.
    
    Args:
        variable (str): Name of the variable file to create (without .var extension)
        value (any, optional): Value to store in the file. Converted to string.
                              Defaults to None (creates empty file).
    
    Behavior:
        - Converts any non-None value to string before writing
        - Overwrites existing files silently
    
    Example:
        new("username", "admin")  # Creates data/username.var  containing "admin"
        new("temp")  # Creates empty data/temp.var  file
    """
    
    # 自动检测变量名，如果未定义则当作字符串
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
    
    if value is True:
        value_str = '$value.true' 
    elif value is False:
        value_str = '$value.false' 
    elif value is Ellipsis:
        value_str = '$value.ellipsis' 
    elif value is None:
        value_str = '$value.none' 
    elif value is NotImplemented:
        value_str = '$value.notimplemented' 
    else:
        value_str = str(value)
    
    with open(path, 'w', encoding='utf-8') as w:
        w.write(value_str) 