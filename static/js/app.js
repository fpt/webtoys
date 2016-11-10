'use strict';

document.addEventListener('DOMContentLoaded', e => {

  navigator.serviceWorker.register('/static/js/service-worker.js').then(registration => {

    registration.pushManager.subscribe({userVisibleOnly:true}).then(subscription => {
      console.log('GCM engpoint is: ', subscription.endpoint);
    });

  }).catch(error => console.log(error));
});
