import os
import re
import ast

def extract_docstrings(py_file_path):
    """
    从Python文件中提取各个函数的Docstring内容
    """
    with open(py_file_path, 'r', encoding='utf-8') as file:
        source_code = file.read()
    
    try:
        parsed_code = ast.parse(source_code)
    except SyntaxError as e:
        print(f"SyntaxError while parsing {py_file_path}: {e}")
        return {}
    
    docstrings = {}
    
    for node in ast.walk(parsed_code):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            docstring = ast.get_docstring(node)
            if docstring:
                docstrings[func_name] = docstring
    
    return docstrings

def convert_docstring_to_md(docstring, func_name):
    """
    将Docstring内容转换为Markdown格式
    """
    lines = docstring.strip().split('\n')
    md_content = ""
    in_code_block = False
    in_params_section = False
    for line in lines:
        if line.strip() == func_name:
            md_content += f"# {line.strip()}\n\n"
        elif line.startswith('    >>>'):
            if not in_code_block:
                md_content += '```\n'
                in_code_block = True
            md_content += line[8:] + '\n'   # 代码块不额外换行
        else:
            if in_code_block:
                md_content += '```\n\n'  # 每行额外空一行
                in_code_block = False
            if line.startswith('    '):
                if in_params_section:
                    if line.strip().startswith('数据类型'):
                        md_content += '  ' + line[4:] + '\n\n'  # 添加换行符
                    else:
                        md_content += '- ' + line[4:] + '\n\n'  # 添加换行符
                elif line.startswith('    |'):  # 表格不额外换行
                    md_content += line[4:] + '\n'
                else:
                    md_content += line[4:] + '\n\n'
            else:
                if line.strip() == "输入参数":
                    in_params_section = True
                elif line.strip() == "返回值":
                    in_params_section = False
                md_content += f"## {line}\n\n"
    if in_code_block:
        md_content += '```\n\n'  # 关闭代码块
    
    # 处理结果部分的'> '去掉
    md_content = md_content.replace('> ', '')
    md_content = md_content.replace('>', '')

    return md_content

def write_md_file(md_dir, relative_path, md_content):
    """
    将Markdown内容写入文件
    """
    md_file_path = os.path.join(md_dir, relative_path)
    os.makedirs(os.path.dirname(md_file_path), exist_ok=True)
    with open(md_file_path, 'w', encoding='utf-8') as file:
        file.write(md_content)

def process_py_file(py_file_path, ini_file_path, md_dir):
    """
    处理Python文件，提取各个函数的Docstring内容，并根据ini文件在对应的文件夹下存放对应的md文件
    """
    docstrings = extract_docstrings(py_file_path)
    
    with open(ini_file_path, 'r', encoding='utf-8') as ini_file:
        lines = ini_file.readlines()
    
    for line in lines:
        line = line.strip()
        if line.endswith('.md'):
            func_name = os.path.splitext(os.path.basename(line))[0]
            if func_name in docstrings:
                docstring = docstrings[func_name]
                md_content = convert_docstring_to_md(docstring, func_name)
                write_md_file(md_dir, line, md_content)

# 示例Python文件路径和Markdown文件目录
py_file_path = r'D:\Projects\SysplorerDoc\sysplorer_api.py'
ini_file_path = r'D:\Projects\SysplorerDoc\init.ini'
md_dir = r'D:\Projects\SysplorerDoc\Doc2MD'

# 创建Markdown文件目录（如果不存在）
os.makedirs(md_dir, exist_ok=True)

# 处理Python文件并导出Docstring为Markdown文件
process_py_file(py_file_path, ini_file_path, md_dir)