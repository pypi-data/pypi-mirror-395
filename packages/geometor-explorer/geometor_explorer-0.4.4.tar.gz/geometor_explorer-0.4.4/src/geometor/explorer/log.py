from __future__ import annotations
import logging
from logging import FileHandler
from rich.logging import RichHandler

def configure_logging(app):
    # Disable Werkzeug's default request logger to reduce noise
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.ERROR)

    # Clear existing handlers and prevent propagation to avoid duplicate logs
    app.logger.handlers.clear()
    app.logger.propagate = False

    # RichHandler for console (message only)
    rich_handler = RichHandler(
        rich_tracebacks=True, 
        markup=True, 
        show_path=False, 
        show_time=False, 
        show_level=False
    )
    rich_handler.setLevel(logging.INFO)
    
    # FileHandler for explorer.log (detailed)
    file_handler = FileHandler("explorer.log")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Add handlers to the app's logger
    app.logger.addHandler(rich_handler)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
