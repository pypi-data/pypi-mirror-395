"""
This file is part of pyFFEDITC.

Copyright (C) 2025 Peter Grønbæk Andersen <peter@grnbk.io>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import os
import subprocess


def compress(input_path: str, output_path: str, ffeditc_exe_path: str) -> bool:
    """
    Compresses a file using the ffeditc_unicode.exe utility.

    Args:
        input_path (str): Path to the uncompressed input file.
        output_path (str): Path where the compressed file will be saved.
        ffeditc_exe_path (str): Path to the ffeditc_unicode.exe executable.

    Raises:
        FileNotFoundError: If the input file or the specified ffeditc_unicode.exe is not found.
        OSError: If file operations fail.

    Returns:
        bool: True if compression succeeded, False otherwise.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"No such file or directory: '{input_path}")
    
    output_dir = os.path.dirname(output_path)

    if not os.path.isdir(output_dir):
        raise FileNotFoundError(f"No such file or directory: '{output_dir}")

    if not os.path.exists(ffeditc_exe_path):
        raise FileNotFoundError(f"No such file or directory: '{ffeditc_exe_path}")

    executable_dir = os.path.dirname(ffeditc_exe_path)

    try:
        result = subprocess.run(
            [ffeditc_exe_path, input_path, "/c", "/o:" + output_path],
            cwd=executable_dir,
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print("Error output:\n", e.stderr)
        return False


def decompress(input_path: str, output_path: str, ffeditc_exe_path: str) -> bool:
    """
    Decompresses a file using the ffeditc_unicode.exe utility.

    Args:
        input_path (str): Path to the compressed input file.
        output_path (str): Path where the decompressed file will be saved.
        ffeditc_exe_path (str): Path to the ffeditc_unicode.exe executable.

    Raises:
        FileNotFoundError: If the input file or the specified ffeditc_unicode.exe is not found.
        OSError: If file operations fail.

    Returns:
        bool: True if decompression succeeded, False otherwise.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"No such file or directory: '{input_path}")
    
    output_directory = os.path.dirname(output_path)

    if not os.path.isdir(output_directory):
        raise FileNotFoundError(f"No such file or directory: '{output_directory}")

    if not os.path.exists(ffeditc_exe_path):
        raise FileNotFoundError(f"No such file or directory: '{ffeditc_exe_path}")

    executable_dir = os.path.dirname(ffeditc_exe_path)

    try:
        result = subprocess.run(
            [ffeditc_exe_path, input_path, "/u", "/o:" + output_path],
            cwd=executable_dir,
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print("Error output:\n", e.stderr)
        return False

