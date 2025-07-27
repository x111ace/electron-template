import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),

	kit: {
		adapter: adapter({
            pages: 'dist/renderer',
            assets: 'dist/renderer',
            fallback: 'index.html',
            precompress: false,
            strict: true
        }),
        // Point SvelteKit to our existing renderer directory
        files: {
            assets: 'src/renderer/static',
            appTemplate: 'src/renderer/app.html',
            routes: 'src/renderer/routes',
            lib: 'src/renderer/lib'
        },
        // Prevents conflicts with Electron's 'app' module
        appDir: 'internal'
	}
};

export default config; 