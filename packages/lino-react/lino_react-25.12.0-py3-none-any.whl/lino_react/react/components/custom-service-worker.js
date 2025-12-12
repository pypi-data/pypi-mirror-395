import {precacheAndRoute} from 'workbox-precaching';


precacheAndRoute(self.__WB_MANIFEST);

self.registration.onupdatefound = (reg) => {
    const installingWorker = self.registration.installing;
    installingWorker.onstatechange = () => {
        if (installingWorker.state == "installed") {
            self.skipWaiting();
        }
    }
}

// https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData

self.addEventListener('notificationclose', function(e) {
    console.log('Closed notification!!!!!!');
});

self.addEventListener('notificationclick', function(e) {
    console.log('notifi event', e);
    let notification = e.notification;
    let action = e.action;
    // if (action === 'explore' || action === "") {
    notification.close();
    self.clients.openWindow(notification.data.action_url);
    // } else {
    //     notification.close();
    // }
});

const cacheFetch = async (request) => {
    const resp = await self.caches.match(request);
    if (resp) return resp;
    return fetch(request);
}

self.addEventListener('fetch', (e) => {
    console.log('custom service worker fetch event', e);
    // e.respondWith(cacheFirst(e.request));
    e.respondWith(function() {
        let resp = fetch(e.request);
        // if (resp.json().version_mismatch) {
        //     self.caches.keys().forEach((key, i) => {
        //         self.caches.delete(key);
        //     });
        // }
        return resp;
    }());
});

// see notify.models.Message.send__browser_messag(): data = dict(body=, subject=, id=)

self.addEventListener('push', (e) => {
    let data = e.data.json();
    let options = {
        body: data.body,
        data: {
            action_url: data.action_url,
            dateOfArrival: Date.now(),
        },
        requireInteraction: true,
        // actions: [
        //     {
        //         action: 'activate',
        //         title: data.action_title,
        //     }
        // ]
    };
    e.waitUntil(self.registration.showNotification(data.subject, options));
});
