const CACHE_NAME = 'my-cache-v1.1.0'; // به‌روزرسانی ورژن کش
const urlsToCache = [
    '/', // صفحه اصلی
    '/static/styles.css', // فایل CSS
    '/static/script.js', // فایل جاوااسکریپت
    '/static/icons/icon-48x48.png', // آیکون‌ها
    '/static/icons/icon-72x72.png',
    '/static/icons/icon-96x96.png',
    '/static/icons/icon-144x144.png',
    '/static/icons/icon-192x192.png',
    '/static/icons/icon-384x384.png',
    '/static/icons/icon-512x512.png'
];

// نصب سرویس ورکِر و کش کردن منابع
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(urlsToCache);
        })
    );
});

// پاسخ به درخواست‌های شبکه از کش
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});

// مدیریت کش (حذف کش‌های قدیمی)
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        return caches.delete(cache); // حذف کش‌های قدیمی
                    }
                })
            );
        })
    );
});
