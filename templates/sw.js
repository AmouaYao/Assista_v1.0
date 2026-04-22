const CACHE_NAME = 'e-menus-v1';
const urlsToCache = [
  '/',
  '/static/assets/css/styles.css',
  '/static/assets/js/scripts.js',
  '/static/assets/logos/wave.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request);
      })
  );
});
