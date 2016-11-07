'use strict';

document.addEventListener('DOMContentLoaded', e => {

  navigator.serviceWorker.register('service-worker.js').then(registration => {

    registration.pushManager.subscribe().then(subscription => {
      console.log('GCM engpoint is: ', subscription.endpoint);
    });

  }).catch(error => console.log(error));
});
