import { resolve } from 'node:path';

import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    emptyOutDir: true,
    manifest: true,
    outDir: resolve(import.meta.dirname, 'src/static_dist'),
    rollupOptions: {
      input: resolve(import.meta.dirname, 'src/static_src/main.ts'),
    },
  },
});
