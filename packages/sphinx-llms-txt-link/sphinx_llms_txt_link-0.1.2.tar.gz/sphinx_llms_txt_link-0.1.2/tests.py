import pickle
import shutil
import unittest
from pathlib import Path

from docutils import nodes
from sphinx.application import Sphinx

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("TestSphinxLlmLinkBuild",)

# --- Setup Boilerplate ---

# Define the source content required for the build test
# We use a unique class name to search the HTML reliably.
TEST_CSS_CLASS = "sphinx-llms-txt-link"

MINIMAL_CONF_PY = """
import os
import sys
# Ensure the extension under test is findable
sys.path.insert(0, os.path.abspath('.'))

# Assuming the extension file is named 'sphinx_llm_link.py'
# and is available in the Python path or a specified directory
extensions = [
    "sphinx_llms_txt_link",
]
html_static_path = ['_static']
master_doc = 'index'
project = 'LLM Test Docs'
copyright = '2025'
author = 'Test Author'
"""

MINIMAL_INDEX_RST = """
.. _index:

Welcome to the LLM Test Docs
===================================

This is a test page to verify the sphinx-llms-txt-link injection.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   guide/install

"""

NESTED_INSTALL_RST = """
.. _install:

Installation Guide
==================

This is a nested page. The link should point to `install.txt`.

"""


# --- Test Class ---

class TestSphinxLlmLinkBuild(unittest.TestCase):
    """
    Tests the sphinx-llms-txt-link extension by running a full Sphinx build
    and inspecting the resulting HTML, avoiding all internal mocks.
    """

    def setUp(self):
        # Determine paths relative to the test execution directory
        root_dir = Path(__file__).parent
        self.docs_dir = root_dir / "test_src"
        self.build_dir = root_dir / "test_build_docs"
        self.doc_tree_dir = self.build_dir / "doc_trees"

        # --- 1. Create the necessary source structure ---
        self.docs_dir.mkdir(exist_ok=True)
        (self.docs_dir / "guide").mkdir(exist_ok=True)

        # Write the minimal config
        (self.docs_dir / "conf.py").write_text(
            MINIMAL_CONF_PY,
            encoding="utf-8",
        )

        # Write the source documents
        (self.docs_dir / "index.rst").write_text(
            MINIMAL_INDEX_RST,
            encoding="utf-8",
        )
        (self.docs_dir / "guide/install.rst").write_text(
            NESTED_INSTALL_RST,
            encoding="utf-8",
        )

    def test_01_full_build_and_link_injection(self):
        """
        Runs a full HTML build and asserts that the link is correctly
        injected into both root and nested pages, with the correct relative
        path.
        """
        # Build the docs using the actual Sphinx application
        test_app = Sphinx(
            srcdir=self.docs_dir,
            confdir=self.docs_dir,
            outdir=self.build_dir,
            doctreedir=self.doc_tree_dir,
            buildername="html",
        )
        test_app.build()

        # --- 2. Check Root Document (index.html) ---
        index_html_path = self.build_dir / "index.html"
        self.assertTrue(index_html_path.exists())
        index_content = index_html_path.read_text(encoding="utf-8")

        # Assert the link is present and points to the sibling file
        expected_root_link = 'href="index.txt"'
        self.assertIn(
            expected_root_link, index_content,
            (
                f"Root link missing in index.html. "
                f"Expected: {expected_root_link}"
            ),
        )

        # Assert the CSS class is present
        self.assertIn(TEST_CSS_CLASS, index_content)

        # --- 3. Check Nested Document (guide/install.html) ---
        install_html_path = self.build_dir / "guide/install.html"
        self.assertTrue(install_html_path.exists())
        install_content = install_html_path.read_text(encoding="utf-8")

        # Assert the link is present and points to the sibling
        # file (install.txt)
        expected_nested_link = 'href="install.txt"'
        self.assertIn(
            expected_nested_link, install_content,
            (
                f"Nested link missing in install.html. "
                f"Expected: {expected_nested_link}"
            ),
        )

        # 4. Check CSS file inclusion (indirectly by conf.py extension loading)
        # The CSS file won't physically exist unless we add it, but the HTML
        # output should link to it via the <link> tag added
        # by app.add_css_file. However, checking the generated HTML for a
        # specific link tag is brittle. We trust the app.add_css_file
        # mechanism is working if setup() is correct. The true test is that
        # the link is present in the source, which we checked.

    def test_02_relative_prefix(self):
        """
        Tests link injection when a relative url_prefix is
        configured (e.g., 'text_versions').
        The link should be 'text_versions/index.txt'
        and 'text_versions/install.txt'.
        """
        # --- 1. Configure the relative prefix in conf.py ---
        # Note: We must re-create conf.py with the new setting
        conf_with_rel_prefix = (
                MINIMAL_CONF_PY
                + "\nsphinx_llms_txt_link_url_prefix = 'text_versions'"
        )
        (self.docs_dir / "conf.py").write_text(
            conf_with_rel_prefix,
            encoding="utf-8",
        )

        # --- 2. Build the docs ---
        test_app = Sphinx(
            srcdir=self.docs_dir,
            confdir=self.docs_dir,
            outdir=self.build_dir,
            doctreedir=self.doc_tree_dir,
            buildername="html",
        )
        test_app.build()

        # --- 3. Check Root Document (index.html) ---
        index_html_path = self.build_dir / "index.html"
        index_content = index_html_path.read_text(encoding="utf-8")
        # Expected: <a href="text_versions/index.txt" ...
        expected_root_link = 'href="text_versions/index.txt"'
        self.assertIn(
            expected_root_link, index_content,
            (
                f"Relative prefix link missing in index.html. "
                f"Expected: {expected_root_link}"
            ),
        )

        # --- 4. Check Nested Document (guide/install.html) ---
        install_html_path = self.build_dir / "guide/install.html"
        install_content = install_html_path.read_text(encoding="utf-8")
        # Expected: <a href="text_versions/install.txt" ...
        expected_nested_link = 'href="text_versions/install.txt"'
        self.assertIn(
            expected_nested_link, install_content,
            (
                f"Relative prefix link missing in install.html. "
                f"Expected: {expected_nested_link}"
            )
        )

    def test_03_absolute_path_prefix(self):
        """
        Tests link injection when an absolute path prefix is
        configured (e.g., '/text_versions').
        The link should be '/text_versions/index.txt'
        and '/text_versions/install.txt'.
        """
        # --- 1. Configure the absolute path prefix in conf.py ---
        abs_path_prefix = "/llm-txt-files"
        conf_with_abs_prefix = (
                MINIMAL_CONF_PY
                + f"\nsphinx_llms_txt_link_url_prefix = '{abs_path_prefix}'"
        )
        (self.docs_dir / "conf.py").write_text(
            conf_with_abs_prefix,
            encoding="utf-8",
        )

        # --- 2. Build the docs ---
        test_app = Sphinx(
            srcdir=self.docs_dir,
            confdir=self.docs_dir,
            outdir=self.build_dir,
            doctreedir=self.doc_tree_dir,
            buildername="html",
        )
        test_app.build()

        # --- 3. Check Root Document (index.html) ---
        index_html_path = self.build_dir / "index.html"
        index_content = index_html_path.read_text(encoding="utf-8")
        # Expected: <a href="/llm-txt-files/index.txt" ...
        expected_root_link = f'href="{abs_path_prefix}/index.txt"'
        self.assertIn(
            expected_root_link, index_content,
            (
                f"Absolute path link missing in index.html. "
                f"Expected: {expected_root_link}"
            ),
        )

        # --- 4. Check Nested Document (guide/install.html) ---
        install_html_path = self.build_dir / "guide/install.html"
        install_content = install_html_path.read_text(encoding="utf-8")
        # Expected: <a href="/llm-txt-files/install.txt" ...
        expected_nested_link = f'href="{abs_path_prefix}/install.txt"'
        self.assertIn(
            expected_nested_link, install_content,
            (
                f"Absolute path link missing in install.html. "
                f"Expected: {expected_nested_link}"
            ),
        )

    def test_04_absolute_url_prefix(self):
        """
        Tests link injection when an absolute URL prefix is
        configured (e.g., 'https://...').
        The link should be 'https://example.com/llm/index.txt'
        and 'https://example.com/llm/install.txt'.
        """
        # --- 1. Configure the absolute URL prefix in conf.py ---
        abs_url_prefix = "https://example.com/llm"
        conf_with_abs_url = (
                MINIMAL_CONF_PY
                + f"\nsphinx_llms_txt_link_url_prefix = '{abs_url_prefix}'"
        )
        (self.docs_dir / "conf.py").write_text(
            conf_with_abs_url,
            encoding="utf-8",
        )

        # --- 2. Build the docs ---
        test_app = Sphinx(
            srcdir=self.docs_dir,
            confdir=self.docs_dir,
            outdir=self.build_dir,
            doctreedir=self.doc_tree_dir,
            buildername="html",
        )
        test_app.build()

        # --- 3. Check Root Document (index.html) ---
        index_html_path = self.build_dir / "index.html"
        index_content = index_html_path.read_text(encoding="utf-8")
        # Expected: <a href="https://example.com/llm/index.txt" ...
        expected_root_link = f'href="{abs_url_prefix}/index.txt"'
        self.assertIn(
            expected_root_link, index_content,
            (
                f"Absolute URL link missing in index.html. "
                f"Expected: {expected_root_link}"
            ),
        )

        # --- 4. Check Nested Document (guide/install.html) ---
        install_html_path = self.build_dir / "guide/install.html"
        install_content = install_html_path.read_text(encoding="utf-8")
        # Expected: <a href="https://example.com/llm/install.txt" ...
        expected_nested_link = f'href="{abs_url_prefix}/install.txt"'
        self.assertIn(
            expected_nested_link, install_content,
            (
                f"Absolute URL link missing in install.html. "
                f"Expected: {expected_nested_link}"
            ),
        )

    def test_05_non_html_build_no_injection(self):
        """
        Tests that the extension gracefully handles non-HTML
        builds (e.g., LaTeX) by checking that the raw HTML node is NOT
        injected into the doctree.
        """
        # --- 1. Build the docs using the 'latex' builder ---
        # The key is to check the *doctree*, not the final output, as the
        # final output is not HTML.
        test_app = Sphinx(
            srcdir=self.docs_dir,
            confdir=self.docs_dir,
            outdir=self.build_dir,
            doctreedir=self.doc_tree_dir,
            buildername="latex",  # Use a non-html builder
        )
        test_app.build()

        # --- 2. Load the index doctree to inspect nodes ---
        # The doctrees are stored as pickle files in the doctreedir
        index_doctree_path = self.doc_tree_dir / "index.doctree"
        self.assertTrue(index_doctree_path.exists())

        # Sphinx uses pickle to store doctrees
        with open(index_doctree_path, "rb") as f:
            index_doctree = pickle.load(f)

        # --- 3. Assert the custom raw HTML node is NOT present ---
        # Search the doctree for the `nodes.raw` element that contains our
        # class name.
        has_custom_node = False
        for node in index_doctree.traverse(nodes.raw):
            # Check if the raw node has the class name we inject
            if TEST_CSS_CLASS in node.astext():
                has_custom_node = True
                break

        self.assertFalse(
            has_custom_node,
            (
                "Custom LLM link node was unexpectedly injected into the "
                "doctree during a non-HTML (latex) build."
            ),
        )

    def tearDown(self):
        # Clean up the build directory and source directory
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        if self.docs_dir.exists():
            shutil.rmtree(self.docs_dir)
