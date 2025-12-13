# 3. API for Explorer Integration

-   The existing `/api/model` endpoint in `explorer` should be updated.
-   When the model is requested, the JSON response should include not only the geometric elements but also the latest analysis results from `divine`. This ensures that every construction action that creates a point also returns the immediate analysis of that point's impact.
