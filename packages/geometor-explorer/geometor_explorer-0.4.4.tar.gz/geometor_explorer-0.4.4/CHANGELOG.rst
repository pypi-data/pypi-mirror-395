changelog
=========

0.4.4
-----
*2025-12-06*

**refactor**

.. + Renamed `logging.py` to `log.py` to avoid module name conflicts.
.. + Updated `app.py` to use the new `log` module.

**fix**

.. + Updated `serialize.py` to import `Polynomial` from `geometor.model.polynomials`.

**test**

.. + Added `tests/test_app.py` for application testing.

0.4.3
-----
*2025-12-06*

**docs**

.. + Updated author metadata in `pyproject.toml`.
.. + Cleaned up module docstrings.

**chore**

.. + Updated `.gitignore`.

0.4.2
-----

-   Refined docstrings and type hinting.
-   Fixed `from __future__ import annotations` placement.

0.4.1
-----
*2025-11-28*

**refactor**

.. + Updated model save method call in `app.py`.
.. + Cleaned up imports in `serialize.py`.

**docs**

.. + Updated module index include path.

0.4.0
-----
*2025-10-31*

**added**

.. + Added `Polynomial` element to the model.
.. + Added a "Polynomial" button to the UI to construct polynomials.
.. + Implemented SVG rendering for polynomials using dynamic polylines.
.. + Added `polynumbers.md` with background information.

0.3.17
------
*2025-10-30*

**fixed**

.. + Fixed an issue where constructing an angle bisector could cause a recursion error.

0.3.16
------
*2025-10-29*

**feat**

.. + Adds a button to the main toolbar to toggle the 'ancestors on hover' feature.

**fixed**

.. + Fixes an issue where lines and circles would not be visible during ancestor hover highlighting.
.. + Adds ancestor data to the model serialization to enable client-side ancestor highlighting.

0.3.15
------
*2025-10-29*

**feat**

.. + Adds ancestor highlighting on hover.

0.3.14
------
*2025-10-27*

**changed**

.. + Updates documentation.

0.3.13
------
*2025-10-27*

**feat**

.. + Flips the svg y-axis to conform to standard geometry coordinate systems.

**fixed**

.. + Adds error handling to construction endpoints.

0.3.12
------
*2025-10-27*

**refactor**

.. + Improves dependents retrieval and serialization.

0.3.11
------
*2025-10-25*

**changed**

.. + Rethinks the placement of the line hover cards when hovering on the table - it should be outside the bounding box of the defining points fo the line, as we are doing with sections and polygons.

0.3.10
------
*2025-10-25*

**fixed**

.. + Fixes polygon hover highlight color.

0.3.9
-----
*2025-10-25*

**added**

.. + Adds a settings modal with a theme toggle.

0.3.8
-----
*2025-10-25*

**fixed**

.. + Fixes analysis toggle button initial state.

0.3.7
-----
*2025-10-25*

**added**

.. + Adds a button to the UI to toggle divine analysis.

0.3.6
-----
*2025-10-25*

**changed**

.. + Improves visual feedback for enabled and disabled buttons.
.. + Enabled buttons now have a cyan border.
.. + All buttons have a cyan background on hover, except when disabled.

0.3.4
-----
*2025-10-24*

**added**

.. + Adds an angle bisector construction from three selected points.
.. + Adds a "bisector" class to perpendicular and angle bisector lines.
.. + Adds a dash-dot style for the "bisector" class.

**changed**

.. + Changes the guide element color to orange.

0.3.3
-----
*2025-10-24*

**added**

.. + Adds animation timeline controls: start, end, and step buttons.
.. + Adds keyboard shortcuts (arrow keys) for timeline controls.

0.3.2
------
*2025-10-24*

**added**

.. + Adds a perpendicular bisector construction from two selected points.

**changed**

.. + Updates the guide style to a smaller dot stroke.

0.3.0
------
*2025-10-24*

**added**

.. + Added an animation timeline to visualize the construction process step-by-step.
.. + Added a play/pause button and a scrubbable slider to control the animation.
.. + Added a checkbox to enable or disable the animation feature.

0.2.15
------
*2025-10-24*

**added**

.. + Added GSAP and `Animate.js` to prepare for construction animation.

0.2.14
------
*2025-10-24*

**added**

.. + Adds a keymap `f` to fit the construction in the available view.

0.2.13
------
*2025-10-24*

**added**

.. + Adds sorting functionality to the 'Sizes', 'Chains', and 'Points' tables in the 'Groups' view.

0.2.12
------
*2025-10-24*

**added**

.. + Added spread information to the polygon hover card.
.. + Added coefficients to the line hover card.
.. + Added center coordinates (h, k) and radius (r) to the circle hover card.

**changed**

.. + Improved the layout and styling of the hover card subtables for a more compact and readable display.

0.2.11
------
*2025-10-24*

**fixed**

.. + Fixed a race condition in the UI that could cause an error when hovering over elements before the model data was fully loaded.
.. + Fixed a bug in the serialization of segments that caused an error when creating new segments.

**changed**

.. + Refactored the serialization logic to be more efficient and maintainable.
.. + Segments are now rendered with markers and a light green stroke to distinguish them from other elements.

0.2.10
------
*2025-10-23*

**added**

.. + Adds keymaps for the following actions:
.. + `l`: construct line
.. + `c`: construct circle
.. + `p`: set point (opens dialog)
.. + `s`: set segment
.. + `S`: set section
.. + `y`: set polygon
.. + Adds a center panel in the status bar to show the ID of the currently selected points.

0.2.9
-----
*2025-10-23*

**added**

.. + Added a modal dialog for creating new models with options for different templates (blank, default, equidistant).
.. + Added logging for file save and load operations.

**fixed**

.. + Fixed an issue where the initial model was loaded twice on startup.

0.2.8
-----
*2025-10-23*

**fixed**

.. + Fixed an issue where segment constructions were not being properly loaded and displayed.

0.2.7
-----
*2025-10-23*

**removed**

.. + Removed old construction files to support the updated serialization format from the model library.

0.2.5
-----
*2025-10-22*

**changed**

.. + Refactored JavaScript codebase to a modular architecture to resolve dependency issues.
.. + Implemented a dark theme for all modal dialogs.
.. + Added robust error handling for algebraic expressions in point creation.

0.2.4
-----
*2025-10-22*

**changed**

.. + Made dark theme the default style.
.. + Theme toggle now only changes the theme for the svg.

0.2.3
-----
*2025-10-22*

**added**

.. + Added a `guide` property toggle in the UI for points, lines, and circles.
.. + Added styling for guide elements to distinguish them visually.

0.2.1
-----
*2025-10-20*

**changed**

.. + Implemented a centralized logging system to provide clear, sequential feedback on construction and analysis operations.
.. + Refactored the application to use the new synchronous analysis hook from the `geometor-model` library.
.. + Added a file logger (`explorer.log`) for detailed debugging.

0.1.0
-----
*2025-10-19*

**changed**

.. + Updated point hover card to use a multi-column layout for algebraic and decimal values.
.. + Updated line hover card to display segment length.