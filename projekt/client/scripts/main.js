const videoPlayer = document.getElementById('video-player');
const videoSrc = 'http://localhost:5000/hls.m3u8'; // URL to your Flask server streaming endpoint

document.addEventListener('DOMContentLoaded', function() {
  if(Hls.isSupported()) {
      var hls = new Hls();
      hls.loadSource(videoSrc);
      hls.attachMedia(videoPlayer);
  }
});