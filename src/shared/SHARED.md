# Directory `src/shared/` Explained:

This directory is used to store code or resources that are used by both the main process (`src/main/`) and the renderer process (`src/renderer/`). This avoids code duplication and ensures consistency across the app.

## Common Contents:

*   TypeScript Types/Interfaces: 

Shared TypeScript definitions (e.g., data models or interfaces) that both processes need. For example, if you're using IPC to pass data between main and renderer, you can define the data structure here.

*   Utility Functions: 

Functions that might be used in both processes, like data formatting or validation logic.