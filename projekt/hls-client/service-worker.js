let serverUrls = [];
let currentServerIndex = 0;

function getNextServerUrl() {
  const serverUrl = serverUrls[currentServerIndex];
  currentServerIndex = (currentServerIndex + 1) % serverUrls.length;
  return serverUrl;
}

self.addEventListener('fetch', event => {
  (async () => {
    const request = event.request;
    console.log(request);

    if (request.url.includes('/servers/')) {
      const modifiedHeaders = new Headers(request.headers);
      modifiedHeaders.set('Content-Type', 'application/json');  
      event.respondWith(fetch(request, { headers: modifiedHeaders }).then(async response => {
        console.log(response);
        if (response.ok) {
          const serverList = await response.json();
          console.log(serverList)
          serverUrls = serverList.map(server => `http://${server.host}:${server.port}`);
          console.log(serverUrls);
        }
        return response;
      }));
    } else if (request.url.endsWith('.m3u8') || request.url.endsWith('.ts')) {
      const newUrl = modifyUrl(request.url);
      const modifiedRequest = new Request(newUrl, {
        method: request.method,
        headers: request.headers,
        mode: 'cors',
        credentials: 'same-origin',
        redirect: 'follow',
        referrer: 'no-referrer',
      });

      console.log(modifiedRequest);

      event.respondWith(fetch(modifiedRequest));
    } else {
      event.respondWith(fetch(request));
    }
  })();
});
  function modifyUrl(originalUrl) {
    const serverUrl = getNextServerUrl();
    return originalUrl.replace(/^(https?:\/\/[^\/]+)(\/.*)?$/, serverUrl + '$2');
  }