# Development Philosophy: UI-First Architecture

## Core Principle: Start with User Experience

When developing, the most basic fallback understanding of the project is to understand the "pages" and user workflows. **What the UI does is the MOST important** - we build the UI to accomplish something meaningful, which may require backend functionality. But we always think in terms of the user's experience: how the UI should **look** (first) and **behave** (second).

## Clean Architecture with SvelteKit:

### **Current Structure (Post-Migration):**
We follow a **component-driven, route-based architecture** using SvelteKit's file conventions:

```
src/renderer/
├── routes/ # File-based pages (URL structure)
│ ├── +layout.svelte # Global layout & effects
│ ├── +page.svelte # Entry page (/)
│ └── game/
│ └── +page.svelte # Game page (/game)
├── lib/ # Reusable components & utilities
│ ├── Draggable.svelte # Interaction components
│ └── mouseEffects.ts # Global behaviors
└── static/ # Assets (fonts, styles, images)
└── styles/ # Page-specific & global CSS
```

## Development Workflow:

### **1. Design the User Journey:**
- What does the user want to accomplish?
- What pages/screens do they need?
- How do they navigate between them?

### **2. Create the Route Structure:**
- Each user destination = a `+page.svelte` file
- Shared elements = `+layout.svelte` files
- URL structure matches folder structure

### **3. Build Components:**
- Start with visual appearance (HTML + CSS)
- Add interactivity (TypeScript logic)
- Extract reusable patterns into `lib/` components

### **4. Connect Backend (When Needed):**
- Use IPC for system operations
- Backend serves the UI, not the other way around
- Keep frontend-first thinking throughout

## Evolution from Legacy Approach:

### **Before (Manual Pages):**

```
pages/
├── EntryPage/
│ ├── entry-page.html # Structure
│ ├── entry-page.css # Styling
│ └── EntryPageINIT.js # Behavior
└── MainPage/ # Repeat pattern
```

### **After (SvelteKit Components):**

```
routes/
├── +page.svelte # All-in-one: structure + style + behavior
└── game/
└── +page.svelte # Self-contained page component
```

## The SvelteKit Advantage:

- **Unified thinking**: HTML, CSS, and TypeScript work together naturally
- **Reactive by default**: UI automatically updates when data changes
- **File-based routing**: URL structure emerges from folder organization
- **Component reusability**: Build once, use anywhere
- **Developer experience**: Hot reload makes iteration instant

This architecture scales from simple desktop apps to complex web applications, maintaining the same UI-first development philosophy throughout.