# Directory `src/renderer/lib/` - Reusable Components & Utilities

## SvelteKit Library Directory

This directory contains **reusable components, utilities, and actions** that can be imported throughout your application using the `$lib` alias. This promotes code reuse and maintains clean component architecture.

## Current Structure:

```
lib/
├── Draggable.svelte # Reusable drag-and-drop wrapper component
├── mouseEffects.ts # Global mouse interaction actions
└── [future-components/] # Additional reusable components
```


## Component Categories:

### **Interactive Components:**

#### **`Draggable.svelte` - Drag & Drop Wrapper:**
```svelte
<script>
    // Self-contained dragging logic
    // Handles mouse events, positioning, boundaries
</script>

<div bind:this={element} on:mousedown={handleMouseDown}>
    <slot></slot>  <!-- Wraps any content -->
</div>
```

**Usage:**
```svelte
<Draggable>
    <div class="my-content">Drag me around!</div>
</Draggable>
```

### **Action Libraries:**

#### **`mouseEffects.ts` - Global Interactions:**
```typescript
export function pixelExplosion(node: HTMLElement, config = {}) {
    // Svelte action for click effects
    // Automatically cleans up on component destroy
}
```

**Usage:**
```svelte
<div use:pixelExplosion>Click for effects!</div>
```

## Import Patterns:

### **From Other Components:**
```svelte
<script>
    import Draggable from '$lib/Draggable.svelte';
    import { pixelExplosion } from '$lib/mouseEffects';
</script>
```

### **From Routes:**
```svelte
<script>
    import MyComponent from '$lib/MyComponent.svelte';
</script>
```

## Component Design Principles:

### **1. Self-Contained Logic:**
- Each component manages its own state
- Minimal external dependencies
- Clear, documented props interface

### **2. Composable Design:**
- Use `<slot>` for flexible content
- Accept configuration via props
- Support event forwarding when needed

### **3. TypeScript Integration:**
```svelte
<script lang="ts">
    export let config: ComponentConfig;
    export let onAction: (data: ActionData) => void;
</script>
```

## Future Component Categories:

### **UI Components:**

```
lib/
├── ui/
│ ├── Button.svelte # Styled button variants
│ ├── Modal.svelte # Overlay dialogs
│ ├── Tooltip.svelte # Hover information
│ └── Layout.svelte # Grid/flex utilities
```

### **Data Components:**

```
ib/
├── data/
│ ├── DataTable.svelte # Sortable, filterable tables
│ ├── Chart.svelte # Visualization components
│ └── Form.svelte # Form handling utilities
```

### **System Integration:**

```
lib/
├── system/
│ ├── FileDropzone.svelte # Drag-and-drop file handling
│ ├── WindowControls.svelte # Custom title bar
│ └── SystemTray.svelte # System tray integration
```

## Actions vs Components:

### **Use Actions For:**
- Global behaviors (mouse effects, keyboard shortcuts)
- DOM manipulation utilities
- Event handling patterns
- Third-party library integration

### **Use Components For:**
- Visual UI elements
- Complex interaction patterns
- Reusable page sections
- State management containers

## Best Practices:

### **Component Naming:**
- PascalCase for components: `MyComponent.svelte`
- camelCase for actions: `myAction.ts`
- Descriptive, feature-focused names

### **Props Interface:**
```svelte
<script lang="ts">
    // Required props
    export let title: string;
    
    // Optional props with defaults
    export let enabled: boolean = true;
    export let config: Config = defaultConfig;
    
    // Event handlers
    export let onSelect: (item: Item) => void = () => {};
</script>
```

### **Documentation:**
- Clear component purpose in comments
- Props documentation with types
- Usage examples in comments
- Event specifications

This library architecture ensures your components are **reusable, maintainable, and type-safe**, supporting rapid development while maintaining code quality.