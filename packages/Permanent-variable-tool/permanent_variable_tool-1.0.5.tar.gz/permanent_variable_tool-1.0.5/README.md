# Permanent Variable Tool
### 中文文档请往下查看
---
## `pvt.new(variable:str, value:Any=None) -> None`
Functionality

Creates/updates variable files in `./data/` directory 
### Usage Example 
```python
pvt.new("user_profile", {"name": "John", "age": 28})  # Serializes to string 
pvt.new("system_flag")   # Creates empty file 
```
---
## `pvt.read(variable:str) -> str`
### Critical Notes
- Always wrap in try-except:
```python 
try:
    config = pvt.read("app_config")
except FileNotFoundError:
    initialize_defaults()
```
---
## `pvt.delete(variable:str) -> None`
### Security Notice 
- Deletion is permanent. Recommended safety check:
```python 
if os.path.exists(pvt.data_dir + "/" + variable + ".var"):
    pvt.delete("temp_data") 
```
---
## `pvt.find (variable name: str) -> Bool`
### Use examples
```python
Bool = pvt.find(str)
print(Bool) # True / False
```
---
## `pvt.list() -> dict`
Functionality  
Reads all `.var` files from `C:\pvt_data` and converts contents to Python values  
Value Mapping Rules  
- `$value.false` → `False`  
- `$value.true` → `True`  
- `$value.ellipsis` → `...`  
- Other content remains as string  
### Usage Example  
```python
variables = pvt.list()  # Returns {'debug': True, 'max_retries': '5'}
```
---
## `pvt.copy(variable name 1:str, variable name 2:str) -> None`  
function  
Find `variable name 1.var` from `C:\pvt_data` and copy its value to `variable name 2.var`. If `variable name 1.var` is not available, write `None` in `variable name 2.var` after prompt.
###Examples of use  
```python
pvt.copy("str1","str2") #copies the value in str1 to str2, creates if str2 does not exist, sets str2 to None if str1 does not exist and prompts an error.
```
---
---

# 永久变量工具 (Permanent Variable Tool)
### Please check the English documents up.
---
## `pvt.new(变量名:str, 值:Any=None) -> None`
功能 
在`./data/`目录中创建/更新变量文件
### 使用示例 
```python
pvt.new("user_profile", {"name": "张三", "age": 28})  # 序列化为字符串 
pvt.new("system_flag")   # 创建空文件
```
--- 
## `pvt.read(变量名:str) -> str`
### 重要说明 
- 必须使用try-except包裹:
```python 
try:
    config = pvt.read("app_config")
except FileNotFoundError:
    initialize_defaults()
```
---
## `pvt.delete(变量名:str) -> None`
### 安全提示 
- 删除操作不可逆。建议进行安全检查:
```python 
if os.path.exists(pvt.data_dir + "/" + variable + ".var"):
    pvt.delete("temp_data")
```
---
## `pvt.find(变量名:str) -> Bool`
### 使用示例 
```python 
Bool = pvt.find(str)
print(Bool) # True / False
```
---
## `pvt.list() -> dict`  
功能  
从`C:\pvt_data`读取所有`.var`文件并转换内容为Python值  
### 值转换规则  
- `$value.false` → 布尔值`False`  
- `$value.true` → 布尔值`True`  
- `$value.ellipsis` → 省略号对象`...`  
- 其他内容保留原始字符串格式  
### 使用示例  
```python
variables = pvt.list()  # 返回如 {'debug': True, 'max_retries': '5'}
```
---
## `pvt.copy(变量名1:str, 变量名2:str) -> None`  
功能  
从`C:\pvt_data`寻找`变量名1.var`，并复制其值写入`变量名2.var`，若`str2`不存在则创建，若`str1`不存在则将`str2`设为`None`并提示错误。
### 使用示例  
```python
pvt.copy("str1","str2")  # 复制str1里的值到str2
```