import { defineConfig } from '@apps-in-toss/web-framework/config';

export default defineConfig({
  appName: 'smoking-area-finder',
  brand: {
    displayName: '너구리굴 찾기',
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
