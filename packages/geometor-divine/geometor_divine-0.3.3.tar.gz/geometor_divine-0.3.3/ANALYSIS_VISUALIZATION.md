# Analysis Visualization Plan

## 1. Objective

To extend the `divine` library's capabilities beyond simple golden section identification. This plan outlines the steps to integrate, expose, and visualize deeper geometric relationships, such as groups, chains, and harmonic ranges, within the `geometor.explorer` UI.

## 2. Backend Refactoring & Integration (`divine`)

The core analysis logic exists but is not currently used by the event-driven system.

### Step 1: Create a Central Analysis Orchestrator

-   In `divine.py` or a new `orchestrator.py`, create a function, e.g., `run_full_analysis(model)`.
-   This function will be responsible for:
    1.  Collecting all golden sections currently in the model (`model.get_elements_by_class('golden')`).
    2.  Passing this list to the functions in `golden/groups.py` to get groups by size, points, and segments.
    3.  Passing the list to `golden/chains.py` to get all harmonic chains.
    4.  Collecting all lines in the model and passing them to `golden/ranges.py`.
    5.  Aggregating all these results into a single, structured Python dictionary.

### Step 2: Modify the Event Listener

-   The `point_added_listener` in `events.py` will be updated.
-   After a new golden section is found and added to the model, the listener will now call `run_full_analysis(model)`.
-   The results from the analysis will be published as a new SSE event (e.g., `analysis_groups_updated`).

## 3. API and Data Structure

The new `analysis_groups_updated` SSE event will push a JSON payload to the frontend.

-   **Payload Structure:**
    ```json
    {
      "groups_by_size": {
        "1.618": [{ "labels": ["A", "E", "B"] }, ...],
        ...
      },
      "groups_by_point": {
        "E": [{ "labels": ["A", "E", "B"] }, { "labels": ["C", "E", "D"] }],
        ...
      },
      "chains": [
        [{ "labels": ["A", "E", "B"] }, { "labels": ["B", "F", "C"] }],
        ...
      ],
      "harmonic_ranges": [
        { "labels": ["A", "B", "C", "D"] },
        ...
      ]
    }
    ```

## 4. Frontend Implementation (`explorer`)

### Step 1: New UI Components

-   Create new tabs or tables in the UI for "Groups," "Chains," and "Ranges."
-   These tables will be populated by the data from the `analysis_groups_updated` SSE event.

### Step 2: Interactive Highlighting

-   Each row in the new tables will represent a group or chain (e.g., a row in the "Chains" table would be a specific chain of sections).
-   When a user **hovers** over a row:
    -   A JavaScript function will iterate through the elements in that group/chain.
    -   It will add a specific, temporary CSS class (e.g., `.highlight-group-hover`) to the corresponding elements in the SVG and the main data tables.
-   When a user **clicks** on a row:
    -   It will apply a persistent class (e.g., `.highlight-group-selected`) to do the same, allowing the user to "lock" the highlight. Clicking again would deselect it.

### Step 3: CSS Styling

-   Create new CSS rules for the highlight classes. This could involve changing stroke color, increasing stroke width, or adding a glow effect to the SVG elements.
