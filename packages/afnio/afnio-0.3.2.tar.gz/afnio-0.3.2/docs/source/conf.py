import datetime

# source code directory, relative to this file, for sphinx-autobuild
# sys.path.insert(0, os.path.abspath("../.."))
import afnio

# General information about the project
project = "Afnio"
author = "Tellurio Inc. and Afnio contributors"
year = str(datetime.datetime.now().year)
copyright = (
    f"{year}, {author}. "
    f"Licensed under the GNU Affero General Public License v3 (AGPLv3)"
)
afnio_version = str(afnio.__version__)

extensions = [
    "myst_nb",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_design",
]

# API autogen
autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "inherited-members": True,
    "show-inheritance": False,
}
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# Type hints
typehints_fully_qualified = False
typehints_document_rtype = False

# MyST / notebook execution (speed tune as needed)
nb_execution_mode = "off"  # or "cache" for faster rebuilds
nb_execution_timeout = 60

# Tell Sphinx to look for our template overrides
templates_path = ["_templates"]

# HTML
html_theme = "pydata_sphinx_theme"
html_title = "Afnio"
html_static_path = ["_static"]
html_logo = "_static/img/afnio-logo-1024x1024.png"
html_theme_options = {
    "logo": {
        "image_light": html_logo,  # For light mode
        "image_dark": html_logo,  # For dark mode (can be different)
    },
    "canonical_url": "https://docs.afnio.ai/docs/stable/",
    "switcher": {
        "json_url": "_static/afnio-versions.json",  # TODO: update with deployed URL
        "version_match": afnio_version,
    },
    "show_toc_level": 2,
    "show_version_warning_banner": True,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/Tellurio-AI/afnio",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "PyPi",
            "url": "https://pypi.org/project/afnio/",
            "icon": "fa-brands fa-python",
        },
    ],
    "navbar_align": "left",
    "navbar_start": ["navbar-logo", "version-switcher"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "header_links_before_dropdown": 6,
    "navbar_persistent": [],
    "footer_start": ["copyright"],  # drop "sphinx-version"
    "footer_end": [],  # drop "theme-version"
    "use_edit_page_button": True,
}
html_context = {
    "github_user": "Tellurio-AI",
    "github_repo": "afnio",
    "github_version": "main",
    "doc_path": "docs",
}

# Cross-refs
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "torch": ("https://pytorch.org/docs/stable", None),
}
