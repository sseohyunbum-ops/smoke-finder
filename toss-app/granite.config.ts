import { defineConfig } from '@apps-in-toss/web-framework/config';

export default defineConfig({
  appName: 'smoke-finder',
  brand: {
    displayName: '연기공간',
    primaryColor: '#FF7A45',
    icon: 'https://sseohyunbum-ops.github.io/smoke-finder/icon-512.png',
  },
  web: {
    host: 'localhost',
    port: 5173,
    commands: {
      dev: 'vite',
      build: 'vite build',
    },
  },
  permissions: [
    {
      name: 'geolocation',
      access: 'access',
    },
  ],
  outdir: 'dist',
});
