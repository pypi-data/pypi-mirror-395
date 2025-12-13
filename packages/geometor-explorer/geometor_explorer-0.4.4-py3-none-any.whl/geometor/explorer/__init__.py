"""
The :mod:`geometor.explorer` is a web-based interface for visualizing and interacting with
geometric models created using the :mod:`geometor.model` library.

Key Components:
---------------
- **App**: The main Flask application (:mod:`~geometor.explorer.app`) that handles API requests and serves the frontend.
- **Serialization**: Tools (:mod:`~geometor.explorer.serialize`) to convert model data into JSON format for the browser.
- **Logging**: Configuration (:mod:`~geometor.explorer.log`) for application logging.

Usage:
------
Run the application using the `run` function or by executing the module directly.
"""
from __future__ import annotations

__version__ = "0.4.4"
