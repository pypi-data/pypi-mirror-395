import os 
 
def list():
    """
    Reads all ".var" files from the "C:\\pvt_data" directory and converts their contents to appropriate Python values.
    
    This function scans the specified directory for files with .var extension and interprets their contents
    according to predefined value mappings. Each file's content is converted to the corresponding Python
    data type or object based on specific string patterns.
    
    Args:
        None
        
    Returns:
        dict: A dictionary where keys are filenames (without .var extension) and values are the converted
              contents of those files. The conversion follows these rules:
              - "$value.false" -> False (boolean)
              - "$value.true" -> True (boolean)
              - "$value.ellipsis" -> ... (Ellipsis object)
              - "$value.none" -> None (NoneType)
              - "$value.notimplemented" -> NotImplemented (NotImplemented object)
              - Any other content -> string (original file content)
              
    Raises:
        FileNotFoundError: If the "C:\\pvt_data" directory does not exist 
        
    Example:
        If C:\pvt_data contains:
        - debug.var with content "$value.true"
        - max_retries.var with content "5"
        - placeholder.var with content "$value.ellipsis"
        
        The function returns:
        {
            'debug': True,
            'max_retries': '5',
            'placeholder': ...
        }
        
    Note:
        - Only files with .var extension are processed
        - Files are read with UTF-8 encoding 
        - If any error occurs while reading a file, that file's value is set to None and an error message is printed
        - The directory path is hardcoded to C:\pvt_data 
        - Empty files or files with unrecognized content are stored as strings
    """
    folder_path = "C:\\pvt_data"
    results = {}
    
    # 确保文件夹路径存在 
    if not os.path.exists(folder_path): 
        raise FileNotFoundError(f"Folder '{folder_path}' not found")
    
    # 遍历文件夹中的所有文件 
    for filename in os.listdir(folder_path): 
        if filename.endswith('.var'): 
            file_path = os.path.join(folder_path,  filename)
            key_name = filename[:-4]  # 移除 '.var' 扩展名 
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read() 
                    if content == "$value.false": 
                        results[key_name] = False 
                    elif content == "$value.true": 
                        results[key_name] = True 
                    elif content == "$value.ellipsis": 
                        results[key_name] = ...
                    elif content == "$value.none": 
                        results[key_name] = None 
                    elif content == "$value.notimplemented": 
                        results[key_name] = NotImplemented
                    else:
                        results[key_name] = content
            except Exception as e:
                print(f"Error reading file '{filename}': {e}")
                results[key_name] = None 
    
    return results 