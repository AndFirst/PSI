const videoPlayer = document.getElementById('video-player');
const videoSrc = 'http://localhost:5000/video2.m3u8'; // URL to your Flask server streaming endpoint

document.addEventListener('DOMContentLoaded', function() {
  if(Hls.isSupported()) {
      console.log('hls is supported');
      var hls = new Hls();
      hls.loadSource(videoSrc);
      hls.attachMedia(videoPlayer);
  } else {
    console.error('hls is not supported');
  }
});
