# 5. Element Properties and Visibility

-   **Objective:** Give users more control over the appearance and behavior of elements in the construction.
-   **Features:**
    -   **Informative Hover Cards:** Rich informational hover cards for all elements, displaying properties like spread, coefficients, and center coordinates.
    -   **Dynamic Styling:** Add the ability to assign a CSS class to any element at any time, allowing for dynamic style changes.
    -   **Visibility Toggles:** Implement controls to toggle the visibility of individual elements and groups of elements (e.g., hide all points, lines, or circles).
    -   **Guide Elements (Implemented):** Introduce a "guide" property for lines and circles. Guide elements are visually distinct (orange, dashed style) and are excluded from intersection checks, preventing them from creating new points. This is useful for construction lines that are not part of the a final figure.
