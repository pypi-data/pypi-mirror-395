GEOMETOR • explorer
===================

.. image:: https://img.shields.io/pypi/v/geometor-explorer.svg
   :target: https://pypi.python.org/pypi/geometor-explorer
.. image:: https://img.shields.io/github/license/geometor/explorer.svg
   :target: https://github.com/geometor/explorer/blob/main/LICENSE

An interactive interface for visualizing and analyzing geometric models.

Overview
--------

**geometor.explorer** is a web-based application for creating, visualizing, and analyzing geometric constructions. It serves as the primary interface to the GEOMETOR ecosystem, allowing users to visually build models and engage with the underlying symbolic algebra.

Key Features
------------

- **Interactive Visualization**: Render constructions as scalable SVG.
- **Real-time Analysis**: Integrates with `geometor.divine` to highlight golden sections and harmonic ranges.
- **Symbolic Feedback**: Displays exact algebraic coordinates and equations using LaTeX/KaTeX.
- **Python Backend**: Powered by Flask and `geometor.model`.

Usage
-----

Install and run the explorer:

.. code-block:: bash

    pip install geometor-explorer
    python -m geometor.explorer

    # or simply
    explorer

Open your browser to `http://127.0.0.1:4444`.

Resources
---------

- **Source Code**: https://github.com/geometor/explorer
- **Issues**: https://github.com/geometor/explorer/issues

Related Projects
----------------

- `GEOMETOR Model <https://github.com/geometor/model>`_: The core symbolic engine.
- `GEOMETOR Divine <https://github.com/geometor/divine>`_: Analysis tools.
