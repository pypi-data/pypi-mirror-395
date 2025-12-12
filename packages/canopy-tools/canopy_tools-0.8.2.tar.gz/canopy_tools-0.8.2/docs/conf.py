# Configuration file for the Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------

import os
import sys
import subprocess

sys.path.insert(0, os.path.abspath('../../canopy'))
                        
import sphinx_rtd_theme


# -- Project information -----------------------------------------------------

project = 'canopy'
copyright = '2025, David M. Belda & Adrien Damseaux'
author = 'David M. Belda & Adrien Damseaux'

def get_version_from_git():
    try:
        return subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            stderr=subprocess.STDOUT
        ).decode("utf-8").strip()
    except Exception:
        return "unknown"

release = get_version_from_git()


# -- General configuration ---------------------------------------------------

# Sphinx extension
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.githubpages'
]

templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

source_suffix = '.rst'
master_doc = 'index'

# Mock out any heavy or problematic modules that break imports
autodoc_mock_imports = [
    "canopy.sources.source_lpjguess",
    "canopy.sources.source_fluxnet2015",
    "canopy.source_data.registry"
]

# -- Options for HTML output -------------------------------------------------

# Set the theme to Read the Docs
html_theme = 'sphinx_rtd_theme'

# Theme options
html_static_path = ['_static']
html_css_files = ['custom.css']
# html_css_files = ['dark_mode.css'] # Need to improve

# Additional theme options
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': True,
    'prev_next_buttons_location': 'both',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': 'white',
    # Toc options
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

html_logo = "_static/canopylogo_small.png"
html_favicon = "_static/favicon.ico"