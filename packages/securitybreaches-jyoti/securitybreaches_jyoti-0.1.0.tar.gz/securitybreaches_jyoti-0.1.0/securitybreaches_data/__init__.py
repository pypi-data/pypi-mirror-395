"""
Security Breaches Documentation Package
Author: Jyoti Rahate
"""

__version__ = "0.1.0"
__author__ = "Jyoti Rahate"

import os

# Get the directory where files are stored
PACKAGE_DIR = os.path.dirname(__file__)

def get_file_path(filename):
    """Get the full path to a file in the package"""
    return os.path.join(PACKAGE_DIR, filename)

def list_files():
    """List all available files in the package"""
    files = [f for f in os.listdir(PACKAGE_DIR) if not f.startswith('__')]
    return files

# Available files
DOCX_FILE = get_file_path('securitybreachesnotes.docx')
PDF_FILE = get_file_path('Security breaches .pdf')
