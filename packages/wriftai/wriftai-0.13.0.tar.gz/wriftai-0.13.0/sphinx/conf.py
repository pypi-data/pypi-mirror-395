"""conf.py."""

import os
import sys
from enum import EnumMeta, StrEnum
from typing import Any

from sphinx.application import Sphinx

sys.path.insert(0, os.path.abspath("../wriftai"))

# Sphinx extensions to enable
extensions = [
    "sphinx.ext.autodoc",  # Automatically generate docs from docstrings
    "sphinx.ext.napoleon",  # Support Google- and NumPy-style docstrings
    "sphinx_markdown_builder",  # Enable Markdown output instead of HTML
]

# Napoleon settings for docstring parsing
napoleon_google_docstring = True  # Parse Google-style docstrings
napoleon_use_ivar = (
    True  # Treat class docstring attributes as instance variables in docs
)

# Autodoc settings
autodoc_typehints = "description"  # Render type hints in the description section

autodoc_member_order = (
    "bysource"  # Document members in the order they appear in the source code
)
autodoc_show_inheritance = True  # Show base classes for inherited classes
# General formatting
add_module_names = (
    False  # Don't prepend module names to class/function references in docs
)

autoclass_content = "init"  # Render class description from init

# Custom type aliases for autodoc
autodoc_type_aliases = {"JsonValue": "JsonValue"}
markdown_anchor_signatures = True


def shorten_titles(app: Sphinx, *args: Any) -> None:
    """Remove wriftai. from ALL titles in docs/."""
    srcdir = app.srcdir

    for filename in os.listdir(srcdir):
        if not filename.endswith(".rst"):
            continue

        path = os.path.join(srcdir, filename)

        with open(path) as f:
            lines = f.readlines()

        if not lines or "wriftai." not in lines[0]:
            continue

        short = lines[0].strip().replace("wriftai.", "")
        lines[0] = short + "\n"
        lines[1] = "=" * len(short) + "\n"

        with open(path, "w") as f:
            f.writelines(lines)


def fix_enum_signatures(app, what, name, obj, options, signature, return_annotation):
    """Fixes the signatures of StrEnum and Enum classes in Sphinx autodoc.

    Sphinx normally expands StrEnum/Enum classes into their internal `EnumMeta`
    constructor signature, showing parameters like
    `(new_class_name, names, module, ...)`. This clutters the documentation
    for end users. This hook replaces the noisy internal signature with a
    clean, user-friendly one.
    """
    if isinstance(obj, EnumMeta):
        if obj is StrEnum:
            return "(str, Enum)", return_annotation
        if issubclass(obj, StrEnum):
            return "(StrEnum)", return_annotation
        return "(Enum)", return_annotation
    return signature, return_annotation


def setup(app: Sphinx) -> None:
    """Connect custom Sphinx hooks to modify documentation during the build."""
    app.connect("env-before-read-docs", shorten_titles)
    app.connect("autodoc-process-signature", fix_enum_signatures)
