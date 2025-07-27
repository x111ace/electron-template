# Directory `src/renderer/` - The SvelteKit Frontend

## Current Architecture (SvelteKit + TypeScript)

The `renderer/` folder serves as the **frontend** of our application, now powered by SvelteKit for modern, reactive user interfaces with file-based routing and component composition.

## SvelteKit Structure:

### **Core Framework Files:**
- **`app.html`**: Main HTML template that wraps all pages
- **`routes/`**: File-based routing system (pages and layouts)
- **`lib/`**: Reusable components, utilities, and actions
- **`static/`**: Static assets (fonts, images, stylesheets)

### **Current Route Structure:**

```
routes/
├── +layout.svelte # Root layout with global mouse effects
├── +page.svelte # Entry page (/)
└── game/
└── +page.svelte # Game page (/game)
lib/
├── components/
│ ├── Draggable.svelte # Reusable draggable wrapper
│ └── MouseEffects.ts # Global interaction effects
├── stores/ # Svelte stores for state management
├── utils/ # Utility functions
└── api/ # API interfaces and IPC bridges
```

## IPC Communication:

### **Secure Bridge via `api.ts`:**
- Defines TypeScript interfaces for backend communication
- Works with both Electron (`electronAPI`) and future Tauri (`__TAURI__`)
- Type-safe message passing between frontend and backend

### **Current IPC Channels:**
- `notify`: Send messages from renderer to main process
- `my-custom-reply`: Receive responses from main process

## Relationship to Web Development:

### **SvelteKit Benefits:**
- **File-based routing**: Similar to Next.js, but faster and smaller
- **Server-side rendering**: Can pre-render static content for better performance
- **Universal patterns**: Skills transfer directly to web development

### **ICP Integration Potential:**
The SvelteKit frontend architecture directly translates to Internet Computer development:
- Routes become canister endpoints
- Svelte components work identically in web3 environments
- State management patterns apply to blockchain frontends
- Same TypeScript skills for IC SDK integration

## Future Evolution (Universal Frontend):

This SvelteKit architecture serves as a **universal frontend** that can work with:
- **Electron**: Current implementation
- **Tauri**: Upcoming migration (zero frontend changes needed)
- **Web browsers**: Standard SvelteKit deployment
- **ICP canisters**: Direct blockchain deployment

The renderer remains **framework-agnostic** - only the backend bridge changes.