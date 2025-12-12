Release history and notes
=========================

`Sequence based identifiers
<http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
are used for versioning (schema follows below):

.. code-block:: text

    major.minor[.revision]

- It's always safe to upgrade within the same minor version (for example, from
  0.3 to 0.3.4).
- Minor version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  0.3.4 to 0.4).
- All backwards incompatible changes are mentioned in this document.

0.1.2
-----
2025-04-10

- Extend ``ignore_comments_endings`` with other most common pragma options.
- Add ``user_ignore_comments_endings`` configuration options for user-defined
  additional comments endings to ignore.
- Document configuration options.
- Start testing against Python 3.12 and 3.13.
- Stop testing against Python 3.8.

0.1.1
-----
2024-07-03

- Minor improvement of packaging and docs.

0.1
---
2023-12-18

- Initial beta release.
