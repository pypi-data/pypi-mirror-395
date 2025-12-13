# UI/UX Improvement Plan for GEOMETOR Explorer

## 1. Objective

To enhance the user interface and experience of the GEOMETOR Explorer to handle complex models with a large number of elements. The focus is on improving information density, providing real-time feedback on backend processes, and making the data tables more powerful and usable.

## 2. Key Initiatives

### A. Log & Status Panel

This new UI component will provide a real-time feed of events from the backend, giving the user visibility into the construction and analysis process.

-   **Purpose:**
    -   Display the status of ongoing calculations (e.g., "Calculating intersections for Line(A,B)...").
    -   Show a history of events for the current session (e.g., "Point 'E' discovered," "Golden section found: A-E-B").
    -   Provide immediate, textual feedback that complements the visual SVG updates.
-   **Location:** A collapsible panel at the bottom or side of the screen.
-   **Integration:** This panel will be the primary consumer of the new SSE stream. Each message pushed from the server (e.g., `point_added`, `analysis_updated`) will be formatted and appended to this log.
-   **Message Types:** The log should use different prefixes or colors for different message sources (e.g., `[SERVER]`, `[MODEL]`, `[DIVINE]`).

### B. Data Table Redesign (Points, Structures, Analysis)

The current tables are simple lists. They need to be redesigned to be more information-dense, interactive, and scalable.

-   **Layout & Density ("Tighten the Layout"):**
    -   Reduce row padding and whitespace to fit more rows on the screen.
    -   Consider a more compact font.
    -   Use alternating row colors for better readability.
    -   Implement horizontal and vertical borders for a clearer grid structure.

-   **Expanded Details ("More Details"):**
    -   **Points Table:** Add new columns for:
        -   `Type`: (e.g., "Given", "Intersection", "Center")
        -   `Parents`: (e.g., "Line(A,B), Circle(C,D)")
        -   `Analysis`: A compact icon (e.g., Φ) to indicate if the point is part of a key finding, with details on hover.
    -   **Structures Table:** Add a `Parents` column (e.g., "A, B" for a line).
    -   **Analysis Table:** This will be the primary display for results from `geometor.divine`. It needs columns for `Type` (e.g., "Golden Section"), `Elements` involved, and the numerical `Value` or ratio.

-   **Interactivity & Scalability ("Many Items"):**
    -   **Sorting:** Make all table columns sortable.
    -   **Filtering:** Add a search/filter box above each table to quickly find elements by label, type, or parents.
    -   **Highlighting:** Enhance the existing hover-highlighting with a click-to-select feature that persistently highlights an element in both the table and the SVG.
    -   **Virtual Scrolling:** For models with hundreds or thousands of elements, rendering the entire table is not feasible. Implement virtual scrolling to only render the visible rows, ensuring the UI remains fast.

### C. General UI Enhancements

-   **Toolbar:** Consolidate the construction action buttons (`Add Line`, `Add Circle`) into a more organized and visually appealing toolbar with icons.
-   **Layout Management:** Use a more robust CSS layout (like Flexbox or Grid) to ensure the different panels (SVG, Tables, Log) resize intelligently and are well-aligned.

## 3. Development Plan

1.  **Phase 1 (Layout Foundation):** Implement the basic three-panel layout (SVG, Data, Log) using a modern CSS framework. Create the empty Log panel.
2.  **Phase 2 (Log Panel Integration):** As the SSE stream is developed, pipe the incoming events into the Log panel for real-time display.
3.  **Phase 3 (Table Data Expansion):** Update the backend API and the `to_browser_dict` serializer to include the new data fields (Type, Parents, etc.).
4.  **Phase 4 (Table UI/UX):** Redesign the CSS for the tables, add the new columns, and implement sorting, filtering, and selection features.
5.  **Phase 5 (Scalability):** Investigate and implement a virtual scrolling library to handle large datasets in the tables.
