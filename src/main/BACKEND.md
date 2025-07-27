# Directory `src/main/` - The Electron Backend

## Current Architecture (Electron + SvelteKit)

The `main/` folder serves as the **backend** of our Electron application, housing the main process that manages the application lifecycle, native system interactions, and secure communication with the frontend.

## What Lives Here:

### **Core Files:**
- **`main.ts`**: The application's entry point. Handles window creation, lifecycle events, and initial setup.
- **`preload.ts`**: Security bridge script that exposes controlled APIs to the renderer process via `contextBridge`.

## What Can Be Written Here:

### **TypeScript/JavaScript:**
- Main process logic (window management, menus, system tray)
- File system operations
- Database connections  
- API integrations
- Business logic that requires Node.js capabilities

### **Other Languages via Child Processes:**
- **Rust binaries**: Spawn Rust executables for performance-critical operations
- **Python scripts**: Data processing, ML operations via child_process
- **C/C++ modules**: Native addons for system-level functionality
- **Shell scripts**: System automation and build processes

## Multi-Language Integration Strategies:

### **File Organization by Feature:**

```
src/main/
├── core/
│ ├── main.ts # Main window & lifecycle
│ └── preload.ts # Security bridge
├── features/
│ ├── file-processing/
│ │ ├── handler.ts # TypeScript coordinator
│ │ ├── processor.rs # Rust performance module
│ │ └── analysis.py # Python data analysis
│ └── database/
│ ├── connection.ts # TypeScript DB interface
│ └── queries.sql # SQL definitions
└── utils/
├── process-manager.ts # Child process coordination
└── ipc-handlers.ts # IPC message routing
```

## Future Evolution (Tauri Ready):

This architecture is designed to evolve seamlessly into Tauri, where:
- `main.ts` logic → `src-tauri/src/main.rs`
- `preload.ts` IPC → Tauri commands with `#[tauri::command]`
- Multi-language support → Native FFI bindings
- Same feature-based organization principles apply

## Philosophy:

Different languages and file types can coexist in the same feature folder, as long as they serve the **same functional purpose**. Organization by **feature** rather than **file type** creates maintainable, cohesive modules.