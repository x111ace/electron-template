# Directory `src/renderer/routes/` - SvelteKit File-Based Routing

## SvelteKit Routing System

This directory implements **file-based routing**, where the folder structure directly determines your application's URL structure. Each `+page.svelte` file becomes a route accessible to users.

## Current Route Structure:

```
routes/
├── +layout.svelte # Root layout (wraps all pages)
├── +page.svelte # Entry page - URL: /
└── game/
└── +page.svelte # Game page - URL: /game
```


## Route Types:

### **Pages (`+page.svelte`):**
- Define the content and behavior for a specific URL
- Automatically receive routing data via `export let data`
- Can include page-specific styles via `<svelte:head>`

### **Layouts (`+layout.svelte`):**
- Wrap multiple pages with shared functionality
- Root layout applies to all routes
- Nested layouts possible for section-specific shared elements

## Current Routes Explained:

### **Root Route (`/`) - Entry Page:**
```svelte
<!-- +page.svelte -->
<script>
    import { goto } from '$app/navigation';
    // Navigation logic to /game route
</script>

<div class="entry-page-container">
    <h1>Welcome, Traveler!</h1>
    <button on:click={() => goto('/game')}>Enter Game</button>
</div>
```

### **Game Route (`/game`) - Interactive Page:**
```svelte
<!-- game/+page.svelte -->
<script>
    import Draggable from '$lib/Draggable.svelte';
    // Escape key returns to root route
</script>

<Draggable>
    <div class="centered-box">Interactive content</div>
</Draggable>
```

### **Root Layout - Global Functionality:**
```svelte
<!-- +layout.svelte -->
<script>
    import { pixelExplosion } from '$lib/mouseEffects';
</script>

<div use:pixelExplosion style="height: 100vh; width: 100vw;">
    <slot /> <!-- All pages render here -->
</div>
```

## Navigation Patterns:

### **Programmatic Navigation:**
```typescript
import { goto } from '$app/navigation';

// Navigate to different routes
await goto('/');           // Go to entry page
await goto('/game');       // Go to game page
```

### **Keyboard Navigation:**
```typescript
// Example: ESC key returns to home
window.addEventListener('keydown', async (e) => {
    if (e.key === 'Escape') {
        await goto('/');
    }
});
```

## Future Route Expansion:

### **Planned Routes:**

```
routes/
├── +layout.svelte # Global layout
├── +page.svelte # Entry/home page
├── game/
│ ├── +layout.svelte # Game section layout
│ ├── +page.svelte # Main game page
│ └── settings/
│ └── +page.svelte # Game settings: /game/settings
├── profile/
│ └── +page.svelte # User profile: /profile
└── settings/
└── +page.svelte # App settings: /settings
```

## Advanced Routing Features:

### **Dynamic Routes:**

```
routes/
└── user/
└── [id]/
└── +page.svelte # /user/123, /user/456, etc.
```


### **Route Parameters:**
```svelte
<script>
    export let data;
    // Access route parameters via data.params
</script>
```

### **Loading States:**
```svelte
<!-- +page.svelte -->
<script>
    import { page } from '$app/stores';
    // Access current route information
</script>
```

## Integration with Desktop App:

Unlike web applications, desktop apps typically have:
- **Deep linking disabled**: Users don't manually type URLs
- **Controlled navigation**: All navigation happens programmatically
- **Persistent state**: Routes can maintain state across navigation

This routing system provides the structure and navigation patterns while maintaining the contained experience users expect from desktop applications.

## Development Benefits:

1. **Predictable structure**: URL matches folder structure
2. **Easy navigation**: Import `goto` and navigate anywhere
3. **Shared layouts**: Global functionality applied consistently
4. **Hot reload**: Route changes update instantly
5. **Type safety**: Full TypeScript support throughout routing
