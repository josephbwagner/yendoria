import os
import subprocess  # nosec B404 # Safe use for git version detection in docs
import sys

# Add the project directory to the sys.path
sys.path.insert(0, os.path.abspath("../src"))


def get_version_from_git():
    """Get version from git tags, fallback to static version."""
    try:
        # Try to get version from git describe
        result = subprocess.run(  # nosec B603 B607 # Safe hardcoded git command for docs
            ["git", "describe", "--tags", "--dirty", "--always"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__)),
            check=False,  # Don't raise exception on non-zero exit
        )
        if result.returncode == 0:
            version_str = result.stdout.strip()
            # Remove 'v' prefix if present
            if version_str.startswith("v"):
                version_str = version_str[1:]
            return version_str
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    # Fallback to static version
    return "0.3.0"


# Project information
project = "Yendoria"
author = "Joseph Wagner"
release = get_version_from_git()
version = release.split("-")[0]  # Remove commit info for short version
copyright = "2025, Joseph Wagner"

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.githubpages",  # Helps with GitHub Pages deployment
]

# Try to add sphinx_autodoc_typehints if available
try:
    import sphinx_autodoc_typehints  # noqa: F401

    extensions.append("sphinx_autodoc_typehints")
except ImportError:
    pass

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Options for HTML output
html_theme = "furo"
html_title = f"{project} {version}"
html_static_path = ["_static"]

# Furo theme options
# Furo theme options
html_theme_options = {
    "source_repository": "https://github.com/josephbwagner/yendoria/",
    "source_branch": "master",
    "source_directory": "docs/",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/josephbwagner/yendoria",
            "html": (
                '<svg stroke="currentColor" fill="currentColor" '
                'stroke-width="0" viewBox="0 0 16 16">'
                '<path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 '
                "2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49"
                "-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15"
                "-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 "
                "2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 "
                "0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 "
                "2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 "
                "2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 "
                "2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 "
                "1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 "
                '16 8c0-4.42-3.58-8-8-8z"></path>'
                "</svg>"
            ),
            "class": "",
        },
    ],
}

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# Intersphinx settings for external library references
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "tcod": ("https://python-tcod.readthedocs.io/en/latest/", None),
}

# Autodoc settings to reduce warnings
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"

# Suppress warnings for missing references in external libraries
nitpicky = False  # Turn off nitpicky mode for external refs
nitpick_ignore = [
    ("py:class", "tcod.context.Context"),
    ("py:class", "tcod.Console"),
    ("py:class", "tcod.event.Event"),
    ("py:class", "tcod.event.KeyDown"),
    ("py:class", "tcod.event.Quit"),
    ("py:class", "np.ndarray"),
    ("py:class", "TileGraphic"),
    ("py:class", "collections.abc.Iterator"),
    ("py:class", "collections.abc.Callable"),
    ("py:data", "typing.Any"),
    ("py:class", "enum.Enum"),
]
