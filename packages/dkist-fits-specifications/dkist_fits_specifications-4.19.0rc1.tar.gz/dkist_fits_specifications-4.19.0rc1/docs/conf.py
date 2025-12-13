# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = "dkist-fits-specifications"

# The full version, including alpha/beta/rc tags
from dkist_fits_specifications import __version__

release = __version__

# -- General configuration ---------------------------------------------------

from dkist_sphinx_theme.conf.core import *

extensions += [
    "dkist_fits_specifications.utils.sphinx.spec_table",
    "sphinx_automodapi.automodapi",
    "sphinx_automodapi.smart_resolver",
]
extensions.remove("autoapi.extension")

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

from dkist_sphinx_theme.conf.theme import *
