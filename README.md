
```bash
cd electron-gui
# init project
python xyzutils.py -i
# print file tree
python xyzutils.py -t
# clean build artifacts
python xyzutils.py -c
# clean dependencies
python xyzutils.py -f
# start dev server
python xyzutils.py -d
```
```
{
    "folders": 20,
    "files": {
        "total": 44,
        "by_type": {
            "TypeScript": {
                "files": 4,
                "lines": 187
            },
            "CSS": {
                "files": 3,
                "lines": 68
            },
            "Svelte": {
                "files": 5,
                "lines": 133
            },
            "Jupyter Notebook": {
                "files": 1,
                "lines": 215
            },
            "HTML": {
                "files": 1,
                "lines": 14
            },
            "JavaScript": {
                "files": 2,
                "lines": 34
            },
            "Python": {
                "files": 1,
                "lines": 376
            }
        }
    }
}
electron-gui/
├── config/
│   ├── tsconfig.main.json                          # TypeScript config for Electron main process (ES modules)
│   └── tsconfig.preload.json                       # TypeScript config for preload script (CommonJS for security)
├── src/
│   ├── main/
│   │   ├── BACKEND.md                              # Documentation explaining Electron backend architecture
│   │   ├── main.ts :: 63 lines                     # Electron main process - window management, lifecycle, IPC setup
│   │   └── preload.ts :: 37 lines                  # Security bridge exposing controlled APIs to renderer via contextBridge
│   ├── renderer/
│   │   ├── lib/
│   │   │   ├── COMPS.md                            # Documentation for reusable components and utilities
│   │   │   └── mouseEffects.ts :: 69 lines         # Svelte action for global pixel explosion click effects
│   │   ├── routes/
│   │   │   ├── entry/
│   │   │   │   ├── styles/
│   │   │   │   │   └── entry-page.css :: 34 lines  # Styles specific to entry page (buttons, layout)
│   │   │   │   └── +page.svelte :: 24 lines        # Entry page route (/entry) with welcome message and navigation button
│   │   │   ├── game/
│   │   │   │   ├── styles/
│   │   │   │   │   └── game-page.css :: 15 lines   # Styles specific to game page (draggable box)
│   │   │   │   ├── +page.svelte :: 28 lines        # Game page route (/game) with draggable box and ESC navigation
│   │   │   │   └── Draggable.svelte :: 58 lines    # Reusable drag-and-drop wrapper component with mouse handling
│   │   │   ├── +layout.svelte :: 9 lines           # Root layout with global mouse effects
│   │   │   ├── +page.svelte :: 14 lines            # Root page route (/) that redirects to entry page
│   │   │   └── ROUTES.md                           # Documentation explaining SvelteKit file-based routing system
│   │   ├── static/
│   │   │   ├── fonts/
│   │   │   │   ├── aattackgraffiti/
│   │   │   │   │   └── placeholder.txt             # Instructions for adding custom font files
│   │   │   │   └── convert_font.ipynb :: 215 lines # Jupyter notebook for font format conversion
│   │   │   ├── styles/
│   │   │   │   └── main.css :: 19 lines            # Global styles, font-face definitions, body styling
│   │   │   └── STATIC.md                           # Documentation for static asset management in SvelteKit
│   │   ├── utils/
│   │   │   └── UTILS.md                            # Documentation for renderer utility functions (currently empty)
│   │   ├── api.ts :: 18 lines                      # TypeScript interfaces for electronAPI and IPC type safety
│   │   ├── app.html :: 14 lines                    # SvelteKit main HTML template wrapping all pages
│   │   └── RENDERER.md                             # Documentation explaining SvelteKit frontend architecture
│   ├── shared/
│   │   └── SHARED.md                               # Documentation for code shared between main and renderer processes
│   └── CODE.md                                     # Project philosophy and UI-first development principles
├── .gitignore                                      # Git ignore patterns for build artifacts and dependencies
├── BUILDME.md                                      # Complete build instructions and migration history documentation
├── package.json                                    # NPM dependencies, scripts, and SvelteKit configuration
├── README.md                                       # Project overview with quick start commands and file tree
├── svelte.config.js :: 28 lines                    # SvelteKit configuration with static adapter and custom paths
├── tsconfig.json                                   # Root TypeScript config extending SvelteKit's generated config
├── vite.config.js :: 6 lines                       # Vite configuration for SvelteKit integration
└── xyzutils.py :: 376 lines                        # Python utility for project management (init, dev, clean, build)
```