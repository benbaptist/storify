import os
import sys
sys.path.insert(0, os.path.abspath('../')) # Add project root to path

project = 'storify'
copyright = '2025, Ben Baptist'
author = 'Ben Baptist'
release = '0.0.11'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon', # For Google and NumPy style docstrings
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'myst_parser', # For Markdown support
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme' # A popular theme

# For intersphinx linking
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

# MyST Parser settings (if you use .md files for documentation)
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown', # if you use .txt for markdown
    '.md': 'markdown',
}

# Autodoc settings
autodoc_member_order = 'bysource' 