====================
sphinx-llms-txt-link
====================
.. External references

.. _Sphinx: https://github.com/sphinx-doc/sphinx
.. _Read the Docs: http://readthedocs.org/
.. _LLMOps: https://en.wikipedia.org/wiki/LLMOps
.. _AI Safety: https://en.wikipedia.org/wiki/AI_safety

.. Internal references

.. _sphinx-llms-txt-link: https://github.com/barseghyanartur/sphinx-llms-txt-link/
.. _Read the Docs project: http://sphinx-llms-txt-link.readthedocs.io/
.. _Contributor guidelines: https://sphinx-llms-txt-link.readthedocs.io/en/latest/contributor_guidelines.html
.. _llms.txt: https://barseghyanartur.github.io/sphinx-llms-txt-link/llms.txt

Automatically add a static link to the raw rendered text
version (reStructuredText or Markdown format) of every HTML
documentation page.

**Optimize for LLM Consumption**:

- Provides a direct link to the **raw, rendered text markup** for the current
  page.
- Enables developers to quickly copy clean, structured context for feeding
  into an LLM prompt.

.. image:: https://img.shields.io/pypi/v/sphinx-llms-txt-link.svg
   :target: https://pypi.python.org/pypi/sphinx-llms-txt-link
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/sphinx-llms-txt-link.svg
    :target: https://pypi.python.org/pypi/sphinx-llms-txt-link/
    :alt: Supported Python versions

.. image:: https://github.com/barseghyanartur/sphinx-llms-txt-link/actions/workflows/test.yml/badge.svg?branch=main
   :target: https://github.com/barseghyanartur/sphinx-llms-txt-link/actions
   :alt: Build Status

.. image:: https://readthedocs.org/projects/sphinx-llms-txt-link/badge/?version=latest
    :target: http://sphinx-llms-txt-link.readthedocs.io
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/docs-llms.txt-blue
    :target: https://sphinx-llms-txt-link.readthedocs.io/en/latest/llms.txt
    :alt: llms.txt - documentation for LLMs

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/barseghyanartur/sphinx-llms-txt-link/#License
   :alt: MIT

.. image:: https://coveralls.io/repos/github/barseghyanartur/sphinx-llms-txt-link/badge.svg?branch=main&service=github
    :target: https://coveralls.io/github/barseghyanartur/sphinx-llms-txt-link?branch=main
    :alt: Coverage

**TL;DR**

`sphinx-llms-txt-link`_ is a `Sphinx`_ extension that injects
a **server-side rendered** link to the `.txt` version of each HTML page,
specifically optimized for `LLMOps`_ and training consumption.

Features
========
- **Server-Side Injection:** Uses the `doctree-resolved` hook to insert
  a `docutils.nodes.raw` element, ensuring the link is in the static HTML
  source.
- **100% Indexable:** Guarantees visibility for all crawlers (Google,
  specialized LLM scrapers, RAG indexers).
- **Theme Agnostic:** Works reliably across themes (Read the Docs, Alabaster,
  Furo, etc.) without requiring template overrides.
- **Auto-Calculated Relative Path:** Correctly calculates the relative path
  to the sibling `.txt` file, avoiding common issues with Sphinx's internal
  link resolution.
- **Simple Styling Integration:** Injects a standard CSS
  class (`sphinx-llms-txt-link`) for easy styling and theme-specific
  overrides.

Prerequisites
=============
- Python 3.10+
- Sphinx 6.0+

Your Sphinx documentation must be configured to output `.txt` files (e.g.,
using `sphinx_markdown_builder` or ensuring the `text` builder runs).

Installation
============
.. code-block:: sh

    pip install sphinx-llms-txt-link

Documentation
=============
- Documentation is available on the `Read the Docs project`_.
- For guidelines on contributing check the `Contributor guidelines`_.

Usage example
=============
Sphinx configuration
--------------------

Essential configuration
~~~~~~~~~~~~~~~~~~~~~~~
Add the extension to your `conf.py`. No other configuration is required.

*Filename: docs/conf.py*

.. code-block:: python
    :name: test_docs_conf_extensions

    extensions = [
        # ... other extensions
        "sphinx_llms_txt_link",
        # ... other extensions
    ]

Custom styling (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~

The extension injects the following minimal HTML structure at the end of the
document body:

.. code-block:: html

    <div class="llm-link-container">
        <a href="current_page_name.txt" class="llm-link">
            View llms.txt version
        </a>
    </div>

If you wish to style the link to match your theme (e.g., `Alabaster` or
`Read the Docs`), you can create a CSS file (e.g.,
`_static/custom_sphinx_llms_txt_link.css`) and include it in
your `conf.py` settings:

*Filename: docs/conf.py*

.. code-block:: python
    :name: test_docs_conf_add_css

    html_css_files = [
        "custom_sphinx_llms_txt_link.css",
    ]

Build process
~~~~~~~~~~~~~
Ensure you run the standard HTML build command. If you use a tool
like `sphinx-markdown-builder` or a custom extension to generate the `.txt`
artifacts, ensure those artifacts exist in the build directory.

.. code-block:: sh

    # Build the .txt files
    sphinx-build -n -b text docs builddocs

    # Build the HTML output and inject the link
    sphinx-build -n -a -b html docs builddocs

The link will now appear at the bottom of every generated HTML page, pointing
correctly to its `.txt` counterpart.

Tests
=====
Run the tests with pytest:

.. code-block:: sh

    pytest

License
=======
MIT

Support
=======
For security issues contact me at the e-mail given in the `Author`_ section.

For overall issues, go to
`GitHub <https://github.com/barseghyanartur/sphinx-llms-txt-link/issues>`_.

Author
======
Artur Barseghyan <artur.barseghyan@gmail.com>
