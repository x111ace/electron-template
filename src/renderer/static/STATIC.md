# Directory `src/renderer/static/` - Static Assets

## SvelteKit Static Asset Management

This directory contains **static files** that are served directly by the Vite development server and included in production builds without processing. These assets are available at the root path (`/`) in your application.

## Current Structure:

```
static/
├── fonts/
│ └── aattackgraffiti/
│ ├── placeholder.txt # Font installation guide
│ └── [font-files.woff2] # Custom web fonts
└── styles/
├── main.css # Global styles & font definitions
├── entry-page.css # Entry page specific styles
└── game-page.css # Game page specific styles
```


## Asset Categories:

### **Fonts (`/fonts/`):**
- Custom web fonts in WOFF2 format for optimal performance
- Font conversion tools available in `convert_font_style.ipynb`
- Referenced in CSS via relative URLs: `url('../fonts/fontname/file.woff2')`

### **Styles (`/styles/`):**
- **`main.css`**: Global styles, font-face definitions, body styling
- **Page-specific CSS**: Linked via `<svelte:head>` in individual page components
- Scoped component styles are defined within `.svelte` files themselves

### **Future Assets:**
- **`/images/`**: Icons, logos, backgrounds
- **`/icons/`**: App icons, favicons
- **`/data/`**: Static JSON files, configuration

## Usage Patterns:

### **In SvelteKit Components:**
```svelte
<svelte:head>
    <link rel="stylesheet" href="/styles/entry-page.css" />
</svelte:head>
```

### **In CSS Files:**
```css
@font-face {
    font-family: 'CustomFont';
    src: url('../fonts/customfont/customfont.woff2') format('woff2');
}
```

### **Asset URLs:**
- Static assets are served from the root: `/fonts/`, `/styles/`, `/images/`
- Vite automatically handles asset optimization and caching
- Development server serves from `src/renderer/static/`
- Production builds copy to `dist/renderer/`

## Development vs Production:

### **Development:**
- Vite dev server serves files directly from this directory
- Changes are immediately available (no restart needed)
- Source maps and debugging information preserved

### **Production:**
- Assets are copied to `dist/renderer/` during build
- Automatic optimization (minification, compression)
- Cache-busting via file hashing for optimal performance

## Best Practices:

1. **Optimize assets before adding**: Compress images, convert fonts to WOFF2
2. **Use semantic naming**: Font folders match font-family names
3. **Separate by type**: Keep fonts, images, and styles organized
4. **Reference correctly**: Use absolute paths (`/fonts/`) in CSS, relative paths (`../fonts/`) in imports

This directory bridges the gap between development convenience and production performance, ensuring your assets are efficiently delivered to users.
