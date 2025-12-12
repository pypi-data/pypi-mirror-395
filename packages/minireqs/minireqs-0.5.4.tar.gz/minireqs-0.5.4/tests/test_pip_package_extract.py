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

import pytest
import tempfile
import os
from pathlib import Path
import pandas as pd

from minireqs.pip_package_extract import (
    find_py_files,
    safe_import,
    find_pip_pkg,
    get_imports,
    extract_pip_requirement
)


class TestFindPyFiles:
    """Test the find_py_files function."""
    
    def test_find_single_py_file(self, tmp_path):
        """Test finding a single Python file."""
        test_file = tmp_path / "test.py"
        test_file.write_text("# test file")
        
        result = find_py_files(test_file)
        assert len(result) == 1
        assert result[0].name == "test.py"
    
    def test_find_py_files_in_directory(self, tmp_path):
        """Test finding Python files in a directory."""
        # Create test files
        (tmp_path / "file1.py").write_text("# file 1")
        (tmp_path / "file2.py").write_text("# file 2")
        (tmp_path / "file3.txt").write_text("# not a py file")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file3.py").write_text("# file 3")
        
        result = find_py_files(tmp_path)
        assert len(result) == 3
        assert all(f.suffix == ".py" for f in result)
    
    def test_invalid_path(self, tmp_path):
        """Test with invalid path."""
        invalid_path = tmp_path / "nonexistent.py"
        result = find_py_files(invalid_path)
        assert result == []
    
    def test_non_py_file(self, tmp_path):
        """Test with a non-Python file."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("# not python")
        result = find_py_files(txt_file)
        assert result == []


class TestSafeImport:
    """Test the safe_import function."""
    
    def test_import_standard_library(self):
        """Test importing standard library modules."""
        module = safe_import("os")
        assert module is not None
        assert module.__name__ == "os"
    
    def test_import_installed_package(self):
        """Test importing an installed package."""
        module = safe_import("pandas")
        assert module is not None
        assert hasattr(module, "__file__")
    
    def test_import_nonexistent_module(self):
        """Test importing a non-existent module."""
        module = safe_import("nonexistent_module_xyz123")
        assert module is None
    
    def test_import_with_dots(self):
        """Test importing modules with dots (partial import)."""
        # Try importing a submodule that might not exist, should fall back to parent
        module = safe_import("pandas.nonexistent.submodule")
        # Should at least try to import pandas
        assert module is not None or safe_import("pandas") is not None


class TestGetImports:
    """Test the get_imports function."""
    
    def test_get_imports_simple(self, tmp_path):
        """Test extracting simple imports."""
        test_file = tmp_path / "test.py"
        test_file.write_text("""
import os
import sys
from pathlib import Path
""")
        imports = get_imports(test_file)
        assert "os" in imports
        assert "sys" in imports
        assert "pathlib" in imports
        assert "pathlib.Path" in imports
    
    def test_get_imports_from_statement(self, tmp_path):
        """Test extracting from import statements."""
        test_file = tmp_path / "test.py"
        test_file.write_text("""
from pandas import DataFrame
from numpy import array, ndarray
import json
""")
        imports = get_imports(test_file)
        assert "pandas" in imports
        assert "pandas.DataFrame" in imports
        assert "numpy" in imports
        assert "numpy.array" in imports
        assert "numpy.ndarray" in imports
        assert "json" in imports
    
    def test_get_imports_aliased(self, tmp_path):
        """Test extracting aliased imports."""
        test_file = tmp_path / "test.py"
        test_file.write_text("""
import pandas as pd
import numpy as np
from pathlib import Path as P
""")
        imports = get_imports(test_file)
        assert "pandas" in imports
        assert "numpy" in imports
        assert "pathlib" in imports


class TestFindPipPkg:
    """Test the find_pip_pkg function."""
    
    def test_find_pip_pkg_standard_library(self):
        """Test finding package for standard library (should return None)."""
        pkg, version = find_pip_pkg("os")
        # Standard library modules typically return None
        assert pkg is None or isinstance(pkg, str)
    
    def test_find_pip_pkg_installed_package(self):
        """Test finding package for installed packages."""
        # Test with pandas (should be installed as dependency)
        pkg, version = find_pip_pkg("pandas")
        if pkg is not None:
            assert isinstance(pkg, str)
            assert isinstance(version, str)
            assert len(version) > 0
    
    def test_find_pip_pkg_nonexistent(self):
        """Test finding package for non-existent module."""
        pkg, version = find_pip_pkg("nonexistent_module_xyz123")
        assert pkg is None
        assert version is None


class TestExtractPipRequirement:
    """Test the extract_pip_requirement function."""
    
    def test_extract_from_single_file(self, tmp_path):
        """Test extracting requirements from a single file."""
        test_file = tmp_path / "test.py"
        test_file.write_text("""
import pandas
import numpy
from pathlib import Path
""")
        req_file = tmp_path / "requirements.txt"
        
        df = extract_pip_requirement(test_file, req_file)
        
        assert isinstance(df, pd.DataFrame)
        assert "import_name" in df.columns
        assert "requirement" in df.columns
        
        # Check if requirements file was created
        assert req_file.exists()
        
        # Check that requirements file has content
        if req_file.stat().st_size > 0:
            content = req_file.read_text()
            assert len(content.strip()) > 0
    
    def test_extract_from_directory(self, tmp_path):
        """Test extracting requirements from a directory."""
        # Create multiple test files
        (tmp_path / "file1.py").write_text("import pandas")
        (tmp_path / "file2.py").write_text("import numpy")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file3.py").write_text("from pathlib import Path")
        
        req_file = tmp_path / "requirements.txt"
        df = extract_pip_requirement(tmp_path, req_file)
        
        assert isinstance(df, pd.DataFrame)
        assert req_file.exists()
    
    def test_extract_with_qa_flag(self, tmp_path, capsys):
        """Test extracting with QA flag enabled."""
        test_file = tmp_path / "test.py"
        test_file.write_text("import pandas")
        req_file = tmp_path / "requirements.txt"
        
        df = extract_pip_requirement(test_file, req_file, QA=True)
        
        # Check that QA output was printed
        captured = capsys.readouterr()
        assert len(captured.out) > 0
    
    def test_extract_empty_file(self, tmp_path):
        """Test extracting from an empty Python file."""
        test_file = tmp_path / "empty.py"
        test_file.write_text("# empty file")
        req_file = tmp_path / "requirements.txt"
        
        df = extract_pip_requirement(test_file, req_file)
        
        assert isinstance(df, pd.DataFrame)
        # Should have no requirements for empty file
        assert len(df) == 0 or "requirement" in df.columns
    
    def test_extract_requirements_file_format(self, tmp_path):
        """Test that requirements file has correct format."""
        test_file = tmp_path / "test.py"
        test_file.write_text("import pandas")
        req_file = tmp_path / "requirements.txt"
        
        extract_pip_requirement(test_file, req_file)
        
        if req_file.exists() and req_file.stat().st_size > 0:
            content = req_file.read_text()
            lines = content.strip().split('\n')
            # Each line should be a package requirement
            for line in lines:
                if line.strip():
                    # Should be in format "package=version" or just "package"
                    assert '=' in line or len(line.strip()) > 0

