# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# Adjust path to src directory
import os
import sys
import tomllib
from datetime import datetime

sys.path.insert(0, os.path.abspath('../src'))

# -- Read metadata from pyproject.toml ---------------------------------------
with open("../pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)

project = pyproject["project"]["name"]
author = "k4144" # pyproject.toml doesn't have author in standard format yet, keeping hardcoded or could parse if added
copyright = f"{datetime.now().year}, {author}"
version = pyproject["project"]["version"]
release = version

# -- Auto-run sphinx-apidoc --------------------------------------------------
def run_apidoc(_):
    from sphinx.ext.apidoc import main
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    module = os.path.join(cur_dir, "..", "src", "ghtest")
    output_path = cur_dir
    main(['-e', '-o', output_path, module, '--force'])

def setup(app):
    app.connect('builder-inited', run_apidoc)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',  # For Google/NumPy style docstrings
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

