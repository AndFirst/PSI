const videoPlayer = document.getElementById('video-player');
const videoNameInput = document.getElementById('video-name');
const serverUrls = ['http://localhost:5000', 'http://localhost:5001'];
let currentServerIndex = 0;

function getNextServerUrl() {
  const serverUrl = serverUrls[currentServerIndex];
  currentServerIndex = (currentServerIndex + 1) % serverUrls.length; // Round-robin
  return serverUrl;
}

function loadSource(videoUrl) {
  if (Hls.isSupported()) {
    const hls = new Hls();
    hls.loadSource(videoUrl);
    hls.attachMedia(videoPlayer);
  } else {
      console.error('HLS is not supported');
  }
}

function loadVideo() {
  const videoName = videoNameInput.value.trim();

  if (videoName) {
    const serverUrl = getNextServerUrl();
    const videoUrl = `${serverUrl}/${videoName}.m3u8`;
    loadSource(videoUrl);
  } else {
      console.error('Please enter a valid video name');
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const defaultVideoName = 'video';
  const defaultVideoUrl = `${getNextServerUrl()}/${defaultVideoName}.m3u8`;
  loadSource(defaultVideoUrl);
});
