const serverUrls = ['http://localhost:5000', 'http://localhost:5001'];
let currentServerIndex = 0;

function getNextServerUrl() {
  const serverUrl = serverUrls[currentServerIndex];
  currentServerIndex = (currentServerIndex + 1) % serverUrls.length;
  return serverUrl;
}

self.addEventListener('fetch', event => {
    const request = event.request;
  
    if (request.url.endsWith('.m3u8') || request.url.endsWith('.ts')) {
      const newUrl = modifyUrl(request.url);
      const modifiedRequest = new Request(newUrl, {
        method: request.method,
        headers: request.headers,
        mode: 'cors',
        credentials: 'same-origin',
        redirect: 'follow',
        referrer: 'no-referrer',
      });
  
      event.respondWith(fetch(modifiedRequest));
    } else {
      event.respondWith(fetch(request));
    }
  });
  
  function modifyUrl(originalUrl) {
    const serverUrl = getNextServerUrl();

    const urlWithoutProtocol = originalUrl.replace(/^https?:\/\//, '');
    const parts = urlWithoutProtocol.split('/');
    parts[0] = serverUrl;

    return parts.join('/');
  }