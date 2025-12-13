def copy(variable, new_variable):
    """
    Copy the content of one variable file to another variable file.
    
    This function reads the content from a source variable file (with .var extension) 
    and writes it to a destination variable file. If the source file doesn't exist,
    it creates the destination file with a default value "$value.none". 
    
    Parameters:
    -----------
    variable : str 
        The name of the source variable (without .var extension). 
        The function will look for a file named "{variable}.var" in the current directory.
        
    new_variable : str 
        The name of the destination variable (without .var extension).
        The function will create or overwrite a file named "{new_variable}.var" 
        in the current directory.
    
    Process Flow:
    -------------
    1. Attempts to open and read the source variable file ({variable}.var)
    2. If successful, stores the file content in memory
    3. If the source file is not found, displays a warning message
    4. Opens the destination variable file ({new_variable}.var) for writing 
    5. Writes the content from source file to destination file
    6. If reading failed (source file not found), writes "$value.none"  as default content 
    
    Error Handling:
    ---------------
    - FileNotFoundError: Handles cases where the source variable file doesn't exist 
    - NameError: Handles cases where the 'output' variable wasn't defined due to read failure
    - The function ensures the destination file is always created, even if source reading fails
    
    File Format:
    ------------ 
    Variable files are simple text files with .var extension that contain string values.
    The format can include special value indicators like "$value.none"  for null/undefined values.
    
    Example Usage:
    --------------
    >>> copy("user_name", "backup_user_name")
    # Copies content from user_name.var  to backup_user_name.var  
    
    >>> copy("nonexistent_var", "new_var")  
    # Warning! File not found: nonexistent_var.var  , will be automatically entered as None
    # Creates new_var.var  with content "$value.none" 
    
    Notes:
    ------
    - Both parameters should be provided without the .var extension
    - The function uses UTF-8 encoding for file operations
    - Existing destination files will be overwritten 
    - The function always ensures a destination file is created 
    - Default value "$value.none"  indicates the absence of valid data
    
    Common Use Cases:
    -----------------
    - Creating backups of variable files 
    - Initializing new variables with existing values
    - Transferring configuration data between variable names 
    - Recovering from missing variable files with safe defaults 
    """
    try:
        # 尝试打开并读取源变量文件 
        with open("C:\\pvt_data\\" + variable + ".var", 'r', encoding='utf-8') as r:
            output = r.read()   # 读取文件内容 
        
    except FileNotFoundError as e:
        # 如果文件不存在或其他错误发生
        print(f"Warning! File not found: {variable}.var , will be automatically entered as None")
    
    finally:
        # 无论是否发生异常，都会执行以下代码 
        with open("C:\\pvt_data\\" + new_variable + ".var", 'w', encoding='utf-8') as w:
            try:
                # 尝试将读取的内容写入新文件 
                w.write(output) 
            except NameError:
                # 如果output变量不存在(即文件读取失败)
                w.write("$value.none")   # 写入默认值
