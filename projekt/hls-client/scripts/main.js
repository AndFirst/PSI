const videoPlayer = document.getElementById('video-player');
const videoNameInput = document.getElementById('video-name');
const serverUrl = 'http://localhost:5000'; // URL to your Flask server streaming endpoint

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
    const videoUrl = `${serverUrl}/${videoName}.m3u8`;
    loadSource(videoUrl);
  } else {
      console.error('Please enter a valid video name');
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const defaultVideoName = 'video';
  const defaultVideoUrl = `${serverUrl}/${defaultVideoName}.m3u8`;
  loadSource(defaultVideoUrl);
});
