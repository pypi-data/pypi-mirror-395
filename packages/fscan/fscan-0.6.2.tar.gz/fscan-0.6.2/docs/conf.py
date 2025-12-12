# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from fscan import __version__


project = 'Fscan'
copyright = '2025, Evan Goetz, Ansel Neunzert'
author = 'Evan Goetz, Ansel Neunzert'
if "dev" in __version__:
    release = version = "dev"
else:
    release = version = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.napoleon',
    'sphinx_immaterial_igwn',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_immaterial_igwn'
html_static_path = ['_static']
html_theme_options = {
    # metadata
    "edit_uri": "blob/main/docs",
    "repo_name": "Fscan",
    "repo_type": "gitlab",
    "repo_url": "https://git.ligo.org/CW/instrumental/fscan",
    "icon": {
        "repo": "fontawesome/brands/gitlab",
        "edit": "material/file-edit-outline",
    },
    "features": [
        "navigation.sections",
    ],
    # colouring and light/dark mode
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "blue-grey",
            "accent": "deep-orange",
            "toggle": {
                "icon": "material/eye-outline",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "amber",
            "accent": "deep-orange",
            "toggle": {
                "icon": "material/eye",
                "name": "Switch to light mode",
            },
        },
    ],
    # table of contents
    "toc_title_is_page_title": True,
}

# -- autodoc

autoclass_content = 'class'
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

# -- autosummary

autosummary_generate = True

# -- napolean
napoleon_google_docstring = True
napoleon_numpy_docstring = True
