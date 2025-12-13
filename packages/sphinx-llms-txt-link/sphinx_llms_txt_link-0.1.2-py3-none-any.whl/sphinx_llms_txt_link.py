import os
import posixpath

from docutils import nodes

__title__ = "sphinx-llms-txt-link"
__version__ = "0.1.2"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2025 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "add_llm_link_node",
    "setup",
    "add_static_path",
)


def add_llm_link_node(app, doctree, docname):
    if app.builder.format != "html":
        return

    # 1. Get the base filename (e.g., 'intro' from 'guide/intro')
    current_filename = posixpath.basename(docname)
    target_file = f"{current_filename}.txt"

    # 2. Retrieve user config for the prefix
    # Defaults to empty string (sibling directory)
    url_prefix = app.config.sphinx_llms_txt_link_url_prefix
    link_text = app.config.sphinx_llms_txt_link_text

    # 3. Construct the final link
    # If the user provided a prefix, we join it.
    # Note: We use posixpath.join to ensure forward slashes for URLs
    # regardless of the OS running the build.
    if url_prefix:
        # Check if it's an absolute URL (http) or a relative path
        if "://" in url_prefix or url_prefix.startswith("/"):
            relative_link = posixpath.join(url_prefix, target_file)
        else:
            # If it's a relative path structure (e.g. "../text_versions"),
            # it implies relative to the current page location.
            relative_link = posixpath.join(url_prefix, target_file)
    else:
        relative_link = target_file

    # Cleaner HTML without inline styles
    html_content = f"""
    <div class="sphinx-llms-txt-link-container">
        <a href="{relative_link}" class="sphinx-llms-txt-link">
            {link_text}
        </a>
    </div>
    """

    raw_node = nodes.raw("", html_content, format="html")
    doctree.append(raw_node)


def setup(app):
    app.connect("doctree-resolved", add_llm_link_node)

    # Inject the CSS file reference into the HTML <head>
    # Ship the CSS file alongside this extension
    app.add_css_file("sphinx_llms_txt_link.css")

    # Standard way for plugins:
    # Using app.connect('builder-inited', ...) to append to html_static_path
    app.connect("builder-inited", add_static_path)

    # format: name, default, rebuild-trigger
    # 'html' means rebuilding html is required if this changes
    app.add_config_value("sphinx_llms_txt_link_url_prefix", "", "html")
    # Config for the text displayed in the link
    app.add_config_value(
        "sphinx_llms_txt_link_text",
        "View llms.txt version",
        "html",
    )

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True
    }


def add_static_path(app):
    # This assumes 'assets' is a folder inside the python package
    # containing sphinx_llms_txt_link.css
    static_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "assets")
    )
    app.config.html_static_path.append(static_path)
