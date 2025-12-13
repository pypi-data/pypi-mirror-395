# SSE Integration Plan for GEOMETOR Explorer

## 1. Objective

To decouple the frontend UI from long-running backend processes (intersections, analysis) and provide a real-time, responsive user experience. When a user adds an element to the construction, the UI should update incrementally as the server discovers new points and analytical insights, rather than freezing until the entire calculation is complete.

## 2. High-Level Architecture

We will implement a Server-Sent Events (SSE) based architecture.

1.  **Client Connection:** On page load, the frontend JavaScript will establish a persistent, one-way connection to a new `/stream` endpoint on the Flask server using the browser's native `EventSource` API.
2.  **User Action:** The user initiates an action (e.g., adding a circle). The frontend sends a standard, non-blocking HTTP request to the existing API endpoint (e.g., `POST /api/construct/circle`).
3.  **Backend Trigger:** The API endpoint receives the request, performs the initial action on the `geometor.model` object (which is very fast), and immediately returns a `202 Accepted` response.
4.  **Event Publishing:** The methods within `geometor.model` (e.g., `construct_circle`) will publish events like `line_added`, `point_added` as they execute. These events will be caught by listeners within the Flask application.
5.  **Message Queue:** The event listeners will push the event data (e.g., the new point's coordinates and label) into a simple, in-memory message queue.
6.  **Server Push:** The `/stream` endpoint, connected to the client, continuously monitors the message queue. When a new event appears in the queue, the endpoint formats it as an SSE message and pushes it over the open connection to the client.
7.  **Client-Side Update:** The client's `EventSource` object receives the event. A corresponding JavaScript event listener fires, parsing the data and performing a small, incremental update to the UI (e.g., adding a single new point to the SVG, updating one row in the analysis table).

## 3. Backend Implementation Plan (Flask)

### Dependencies
-   We will use Python's built-in `queue.Queue` for the in-memory message bus. This is sufficient for a single-worker Flask development server. For production, this could be swapped for a more robust system like Redis.

### New `/stream` Endpoint
-   **Path:** `/api/stream`
-   **Method:** `GET`
-   **Functionality:**
    -   Set the response `Content-Type` to `text/event-stream`.
    -   Use a generator function (`def stream(): ... yield data`) to hold the connection open.
    -   Listen to the message queue. When a message is available, format it as `event: <event_name>\ndata: <json_payload>\n\n` and `yield` it.

### Message Queue
-   A single, shared instance of `queue.Queue` will be created within the Flask application context.
-   This queue will be accessible to both the standard API endpoints and the `/stream` endpoint.

### Modify Existing Endpoints (`/api/construct/*`)
-   These endpoints will be modified to be non-blocking.
-   They will no longer call `to_browser_dict(model)` or return the entire model.
-   Their role is to trigger the model operation and return an immediate `202 Accepted`.

### Update Model Event Listeners
-   The listener function currently attached to the `point_added` event (which calls `analyze_model`) will be modified.
-   It will now put a message onto the queue for each new point and for any new analysis results.

## 4. Frontend Implementation Plan (JavaScript)

### Establish SSE Connection
-   On application start, create a single `EventSource` instance:
    ```javascript
    const eventSource = new EventSource('/api/stream');
    ```

### Event Listeners
-   Attach listeners for each event type we define:
    ```javascript
    eventSource.addEventListener('point_added', (e) => {
        const pointData = JSON.parse(e.data);
        // Logic to render the new point in SVG
    });

    eventSource.addEventListener('analysis_updated', (e) => {
        const analysisData = JSON.parse(e.data);
        // Logic to update the analysis table in the UI
    });

    eventSource.onerror = (err) => {
        console.error("EventSource failed:", err);
        // EventSource will automatically try to reconnect
    };
    ```

### UI State Management
-   The UI will need a "loading" or "processing" indicator that is activated when a construction request is sent and deactivated when a special `processing_finished` event is received.

## 5. Event Naming and Data Structures

The following events and payloads should be defined:

-   **`model_reset` / `construction_loaded`**
    -   **Description:** Fired when a new model is created or loaded. The payload will be the entire model. This is the initial state dump.
    -   **Payload:** The full output of `to_browser_dict(model)`.

-   **`point_added`**
    -   **Description:** Fired for each new point.
    -   **Payload:** A JSON object for a single point: `{ "label": "E", "x": "0.5", "y": "0.866", "classes": ["intersection"], ... }`

-   **`line_added` / `circle_added` / etc.**
    -   **Description:** Fired for new structural elements.
    -   **Payload:** A JSON object for that element.

-   **`analysis_updated`**
    -   **Description:** Fired when `divine` finds new insights.
    -   **Payload:** A JSON object with the analysis results, structured for easy display.

-   **`processing_finished`**
    -   **Description:** A simple signal that the backend has finished all work related to the last user action.
    -   **Payload:** `{ "status": "complete" }`

## 6. Development Steps

1.  **Phase 1 (Backend):** Implement the `/stream` endpoint and the in-memory queue. Modify one endpoint (e.g., `/api/construct/line`) and its corresponding model events to push to the queue.
2.  **Phase 2 (Frontend):** Implement the `EventSource` connection and the listener for `point_added`. Verify that new intersection points appear in the UI in real-time.
3.  **Phase 3 (Expand):** Roll out the pattern to all other construction endpoints and UI components.
4.  **Phase 4 (Analysis):** Integrate the `divine` analysis, having it push `analysis_updated` events to the queue.
5.  **Phase 5 (Refinement):** Add robust error handling and UI state indicators.
