let serverUrls = [];
let currentServerIndex = 0;

function getNextServerUrl() {
  const serverUrl = serverUrls[currentServerIndex];
  currentServerIndex = (currentServerIndex + 1) % serverUrls.length;
  return serverUrl;
}

async function modifyRequestBody(request) {
  const bodyText = await request.text();
  return new Request(request.url, {
    method: request.method,
    headers: {
      'Content-Type': 'application/json',
      // inne nagłówki...
    },
    mode: 'cors',
    credentials: 'same-origin',
    redirect: 'follow',
    referrer: 'no-referrer',
    body: bodyText
  });
}

async function handleServersRequest(request) {
  const modifiedRequest = await modifyRequestBody(request);

  return fetch(modifiedRequest).then(async response => {
    console.log(response);
    if (response.ok) {
      const serverList = await response.json();
      console.log(serverList);
      serverUrls = serverList.map(server => `http://${server.host}:${server.port}`);
      console.log(serverUrls);
    }
    return response;
  });
}

function modifyUrl(originalUrl) {
  const serverUrl = getNextServerUrl();
  return originalUrl.replace(/^(https?:\/\/[^\/]+)(\/.*)?$/, serverUrl + '$2');
}

self.addEventListener('fetch', event => {
  event.respondWith((async () => {
    const request = event.request;

    if (request.url.includes(coordinatorUrl) && request.method === 'GET') {
      // Pobranie parametrów z query string
      const url = new URL(request.url);
      const name = url.searchParams.get('name');
      const quality = url.searchParams.get('quality');

      if (!name || !quality) {
        return new Response('Invalid parameters', { status: 400, statusText: 'Bad Request' });
      }

      const data = { 'name': name, 'quality': parseInt(quality) };
      const modifiedRequest = new Request(request.url, {
        method: request.method,
        headers: {
          'Content-Type': 'application/json',
          // inne nagłówki...
        },
        mode: 'cors',
        credentials: 'same-origin',
        redirect: 'follow',
        referrer: 'no-referrer',
        body: JSON.stringify(data)
      });

      return handleServersRequest(modifiedRequest);
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

      return fetch(modifiedRequest);
    } else {
      return fetch(request);
    }
  })());
});

