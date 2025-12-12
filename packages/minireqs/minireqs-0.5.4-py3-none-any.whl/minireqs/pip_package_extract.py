# Copyright (C) 2025 Lei Liu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import pandas as pd
import ast
import importlib
import importlib.metadata as md # Python 3.8+ required
import random
import string
import os
import tempfile
from pathlib import Path

TEST_MODE = False

if TEST_MODE:
    from helpers import safe_import, find_py_files, \
        list_requirements, \
        compile_requirements, \
        check_installed_versions
else:
    from .helpers import safe_import, find_py_files, \
        list_requirements, \
        compile_requirements, \
        check_installed_versions
  

# Find the corresponding pip install package requirements 
# of a name in import statement.
# Core function
def find_pip_pkg(import_name):

    module = safe_import(import_name)
    if module is None:
        print(f"WARNING: Cannot import {import_name}")
        return None, None
    
    module_path = getattr(module, "__file__", None)
    if not module_path:
        return None, None

    module_path = module_path.replace("\\", "/")

    best_match = None
    best_len = 0
    version = None

    for dist in md.distributions():
        for file in dist.files or []:
            f = str(file).replace("\\", "/")
            if f in module_path:
                if len(f) > best_len:
                    best_match = dist.metadata["Name"]
                    best_len = len(f)
                    version = dist.version

    return best_match, version

# Get the possible names of imports that are needed from a script file 
# Core function   
def get_imports(script_path):

    if not os.path.isfile(script_path):
        return []

    with open(script_path, 'r') as file:
        content = file.read()
        if not content.strip():  # empty or whitespace-only file
            return []  
        tree = ast.parse(content, filename=script_path)
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_name = alias.name
                imports.add(imported_name)
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module
            imports.add(module_name)
            for alias in node.names:
                imported_name = alias.name
                imports.add(f"{module_name}.{imported_name}")
            
    list_imports = list(imports)
    additional_imports = [x.split('.')[0] for x in list_imports if '.' in x]
    
    return list(set( list_imports + additional_imports ))

# Find all pip install requirements from a py file or all py files in a folder
# Core function
def extract_pip_requirement(
    script_path = 'main.py', 
    req_path = 'req_main.txt', 
    QA=False):
    
    file_list = find_py_files(script_path)

    list_imports = []
    for i, file in enumerate(file_list):
        print(i, file)
        list_imports = list_imports + get_imports(file)

    if list_imports == []:
        print("List of imports is empty")
        return pd.DataFrame()

    list_imports = list(set(list_imports))    

    combine_pair = lambda pair: f"{pair[0]}=={pair[1]}" if pair[0] is not None and pair[1] is not None else None

    df_pip_pkg = pd.DataFrame({
        'import_name': list_imports,
        'requirement': [combine_pair(find_pip_pkg(x)) for x in list_imports] 
        }).dropna(subset=['requirement'])
    
    if QA:
        print(df_pip_pkg.sort_values('requirement').reset_index(drop=True))    

    df_pip_pkg['requirement'].dropna().drop_duplicates().to_csv(req_path, index=False, header=False)

    df_pip_pkg['len_import'] = df_pip_pkg['import_name'].str.len()
    df_pip_pkg_out = df_pip_pkg.sort_values(['requirement','len_import'])\
        [['import_name','requirement']]\
            .drop_duplicates(subset=['requirement'], keep='first').reset_index(drop=True)
    return df_pip_pkg_out

# Generate a full requirements file from a minimal requirements file 
# including transitive packages and their versions; then compare
# the versions of actually installed packages from the full requirements
# file; use the actually installed versions as the input, to generate the final
# compiled version, compare with the installed version; if they are the same,
# re-genrate the compiled version using the universal platform option.

# import random
# import string
# import os 
# import tempfile

def generate_full_requirements(min_req_file, full_universal_req_file):

    # Generate temporary req files
    rand_tempfile = lambda: os.path.join(
        tempfile.gettempdir(),
        ''.join(random.choice(string.ascii_lowercase) for _ in range(10)) + ".txt"
    )
    compiled_req_file1 = rand_tempfile()
    compiled_req_file2 = rand_tempfile()
    installed_req_file = rand_tempfile()

    # Step 1
    print(f'Step 1: find all packages required by {min_req_file}.')
    compile_requirements(min_req_file, compiled_req_file1)  
    print("\n")  

    # Step 2
    print(f"Step 2: compare the versions in compiled_req_file1 with those actaully installed")
    any_nomatch, df_comp = check_installed_versions(compiled_req_file1, installed_req_file)
    print(f"Is there any mismatched version: {any_nomatch}\n")

    # Step 3
    print("Step 3: compile again to double check the installed versions have no conflicts")
    compile_requirements(installed_req_file, compiled_req_file2)

    set_req1 = set(list_requirements(installed_req_file))
    set_req2 = set(list_requirements(compiled_req_file2))
    print(f"No conflicts: {set_req1 == set_req2}\n")

    # Step 4 (output)
    if set_req1 == set_req2:
        compile_requirements(installed_req_file, full_universal_req_file, sys_platform='universal')
        print(f"Full universal requirements file generated: {full_universal_req_file}")
    else:
        print("Error: manually check the requirments files!")

    # Delete the temporary files
    file_path = compiled_req_file1
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} deleted")
    else:
        print(f"{file_path} does not exist")

    file_path = compiled_req_file2
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} deleted")
    else:
        print(f"{file_path} does not exist")

    file_path = installed_req_file
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} deleted")
    else:
        print(f"{file_path} does not exist")

    return set_req1 == set_req2
    


if __name__ == '__main__':
    df_pip_package = extract_pip_requirement()
    print(df_pip_package)