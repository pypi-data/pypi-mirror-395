# GEOMETOR Explorer

A web-based UI for the GEOMETOR model.

## Overview

The `explorer` provides an interactive environment for creating, visualizing, and analyzing geometric constructions. It uses Flask for the backend and SVG for rendering. It integrates with `geometor.model` for core geometry and `geometor.divine` for analysis.

## Index

-   `app.py`: The main Flask application, handling routing and backend logic.
-   `static/`: Frontend assets, including JavaScript, CSS, and images.
-   `templates/`: HTML templates for the web interface.
-   `serialize.py`: Handles the serialization of construction data.
-   `logging.py`: Configures logging for the application.

## API Endpoints

The `app.py` file exposes the following API endpoints:

-   `GET /api/model`: Get the model data.
-   `POST /api/analysis/toggle`: Toggle the divine analysis.
-   `POST /api/model/save`: Save the model.
-   `POST /api/model/load`: Load a model.
-   `GET /api/constructions`: List available constructions.
-   `POST /api/model/new`: Create a new model.
-   `POST /api/construct/line`: Construct a line.
-   `POST /api/construct/circle`: Construct a circle.
-   `POST /api/construct/perpendicular_bisector`: Construct a perpendicular bisector.
-   `POST /api/construct/angle_bisector`: Construct an angle bisector.
-   `POST /api/construct/polynomial`: Construct a polynomial.
-   `POST /api/construct/point`: Construct a point.
-   `POST /api/model/delete`: Delete an element.
-   `GET /api/model/dependents`: Get dependents of an element.
-   `POST /api/model/edit`: Edit an element.
-   `POST /api/set/segment`: Set a segment.
-   `POST /api/set/section`: Set a section.
-   `POST /api/set/polygon`: Set a polygon.
-   `GET /api/groups/by_size`: Get golden sections grouped by size.
-   `GET /api/groups/by_point`: Get golden sections grouped by point.
-   `GET /api/groups/by_chain`: Get golden sections grouped by chain.
