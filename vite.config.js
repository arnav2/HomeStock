import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  root: 'electron/renderer',
  build: {
    outDir: path.resolve(__dirname, 'electron/renderer'),
    emptyOutDir: false,
    rollupOptions: {
      input: path.resolve(__dirname, 'electron/renderer/index.html'),
    },
  },
  base: './',
  server: {
    port: 5173,
  },
});

