const videoPlayer = document.getElementById('video-player');
const videoNameInput = document.getElementById('video-name');
const videoQualitySelect = document.getElementById('video-resolution');

function loadSource(videoUrl) {
  if (Hls.isSupported()) {
    const hls = new Hls();
    hls.loadSource(videoUrl);
    hls.attachMedia(videoPlayer);
  } else {
    window.alert('HLS is not supported');
  }
}

function loadVideo() {
  const videoName = videoNameInput.value.trim();
  const videoQuality = videoQualitySelect.value;

  if (videoName) {
    const videoUrl = `${videoName}/${videoQuality}/hls.m3u8`;
    loadSource(videoUrl);
  } else {
      window.alert('Please enter a valid video name');
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const defaultVideoName = 'video';
  const defaultVideoQuality = '720p';
  const defaultVideoUrl = `${defaultVideoName}/${defaultVideoQuality}/hls.m3u8`;
  loadSource(defaultVideoUrl);
});
