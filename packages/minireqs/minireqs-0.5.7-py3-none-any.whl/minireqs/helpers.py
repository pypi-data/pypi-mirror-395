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
from importlib.metadata import version, PackageNotFoundError
from packaging.requirements import Requirement
import subprocess
import sys, os
import tempfile, random, string
from pathlib import Path


# Utility function
def find_py_files(script_path):
    """
    Return a list of .py file paths from a file or a folder.
    
    Args:
        script_path (str or Path): path to a python file or folder
    
    Returns:
        List[Path]: list of .py file paths
    """
    script_path = Path(script_path)

    if script_path.is_file() and script_path.suffix == ".py":
        # Single file
        return [script_path.resolve()]
    
    elif script_path.is_dir():
        # Folder: recursively find all .py files
        py_files = list(script_path.rglob("*.py"))
        return [p.resolve() for p in py_files]
    
    else:
        # Not a valid file or folder
        print(f"Error: {script_path} is neither a .py file nor a directory.")
        return []

# Safely import a possibly valid import_name
# Unility function
def safe_import(name):
    """
    Import a module safely by progressively stripping attributes.
    Example:
        'google.cloud.storage' → try full, then try 'google.cloud', then 'google'
    """
    parts = name.split(".")
    for i in range(len(parts), 0, -1):
        module_name = ".".join(parts[:i])
        try:
            return importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue
    return None

# Remove Comment Lines (leading whitespace allowed)
def remove_hash_comment_lines(infile, outfile=None):
    cleaned = []

    with open(infile) as f:
        for line in f:
            stripped = line.lstrip()     # remove leading spaces/tabs
            if stripped.startswith("#"): # comment line → skip
                continue
            cleaned.append(line.rstrip("\n"))

    if outfile is None:
        outfile = infile + ".cleaned"

    with open(outfile, "w") as f:
        f.write("\n".join(cleaned) + "\n")

    return outfile


# Use python -m uv pip compile to generate a full list 
# of transitive packages including the original packages 
# from a requirements file.
# Running the command line scripts from python

def compile_requirements(input_file, output_file, sys_platform=None):
    """
    Compile requirements file using uv pip compile.

    Popular sys_platform values: 'universal', 'win32', 'linux', 'darwin' 
    
    """

    rand_tempfile = lambda: os.path.join(
        tempfile.gettempdir(),
        ''.join(random.choice(string.ascii_lowercase) for _ in range(10)) + ".txt"
    )
    compiled_req_file1 = rand_tempfile()

    cmd = [sys.executable, '-m', 'uv', 'pip', 'compile', '--quiet', input_file]

    if sys_platform == 'universal':
        cmd.extend(['--universal'])
    elif sys_platform is not None:
        cmd.extend(['--python-platform', sys_platform])
    
    cmd.extend(['-o', compiled_req_file1])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=False, #True,
            text=True,
            check=True  # Raises exception if return code is non-zero
        )
        remove_hash_comment_lines(compiled_req_file1, output_file)
        print(f"Successfully compiled {input_file}")
        if result.stdout:
            print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error compiling requirements: {e}")
        print(f"Error output: {e.stderr}")
        return None
    except FileNotFoundError:
        print("Error: 'uv' command not found. Make sure uv is installed.")
        return None

 
# Check if the required packages in the requirements_file are installed in the current environment
# and their installed version, compare with the requirements_file to see if they are the same 

def check_installed_versions(requirements_file, req_installed_file = '_req_installed.txt'):

    req_infile = []
    req_installed = []
    nomatch_ind = []

    with open(requirements_file) as f:
        for line in f:
            line = line.strip()
            if "==" not in line or line.startswith("#"):
                continue
            
            req_infile += [line]

            pkg, required = line.split("==")
            try:
                installed = version(pkg)
                req_installed += [f"{pkg}=={installed}"]
                if installed == required:                    
                    nomatch_ind += [0]
                else:
                    print(f"{pkg}: MISMATCH installed={installed}, required={required}")
                    nomatch_ind += [1]

            except PackageNotFoundError:
                print(f"{pkg}: NOT INSTALLED (required={required})")
                req_installed += [None]
                nomatch_ind += [1]

    any_nomatch = sum(nomatch_ind) > 0
    df_comp = pd.DataFrame({'req_resolved':req_infile,
        'req_installed': req_installed,
        'nomatch_ind': nomatch_ind})
    if any_nomatch:
        print(df_comp[df_comp['nomatch_ind']==1])

    df_comp['req_installed'].to_csv(req_installed_file, index=False, header=False)

    return any_nomatch, df_comp

# Find the requirements (package==version) and return them as a list 
def list_requirements(path):
    reqs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            reqs.append(line)
    return reqs


# # Find packages that are platform dependent
# # from packaging.requirements import Requirement
# def find_platform_specific(req_file):
#     out = []
#     with open(req_file) as f:
#         for line in f:
#             line = line.strip()
#             if not line or line.startswith("#"):
#                 continue
#             req = Requirement(line)
#             if req.marker is not None:  # platform-specific or conditional
#                 out.append(line)
#     return out

# # Remove platform-specific requirements from a requirements file
# def remove_platform_specific(req_file, output_file=None):
#     platform_specific = []
#     cleaned_lines = []

#     with open(req_file) as f:
#         for line in f:
#             raw = line.rstrip("\n")
#             stripped = raw.strip()

#             # Keep comments and empty lines
#             if not stripped or stripped.startswith("#"):
#                 cleaned_lines.append(raw)
#                 continue

#             req = Requirement(stripped)

#             # If there is a marker → it's platform-specific
#             if req.marker is not None:
#                 platform_specific.append(raw)
#                 # Skip (delete) this line
#                 continue

#             # Keep non-platform-specific requirements
#             cleaned_lines.append(raw)

#     # Output file defaults to <original>.cleaned
#     if output_file is None:
#         output_file = req_file + ".cleaned"

#     # Write cleaned requirements
#     with open(output_file, "w") as f:
#         f.write("\n".join(cleaned_lines) + "\n")

#     return platform_specific
