const videoElement = document.querySelector('.input_video');
const canvasElement = document.querySelector('.output_canvas');
const canvasCtx = canvasElement.getContext('2d');
const cursor = document.getElementById('cursor');
const statusText = document.getElementById('gestureStatus');

const hands = new Hands({
  locateFile: (file) => {
    return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
  }
});

hands.setOptions({
  maxNumHands: 1,
  modelComplexity: 1,
  minDetectionConfidence: 0.7,
  minTrackingConfidence: 0.7
});

hands.onResults(onResults);

function onResults(results) {
  canvasCtx.save();
  canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
  canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

  if (results.multiHandLandmarks.length > 0) {
    const landmarks = results.multiHandLandmarks[0];
    const x = landmarks[8].x * window.innerWidth;
    const y = landmarks[8].y * window.innerHeight;

    cursor.style.left = `${x}px`;
    cursor.style.top = `${y}px`;

    statusText.innerText = "Index Finger Detected - Moving Cursor";
  } else {
    statusText.innerText = "No Hand Detected";
  }

  canvasCtx.restore();
}

function startCamera() {
  const camera = new Camera(videoElement, {
    onFrame: async () => {
      await hands.send({ image: videoElement });
    },
    width: 640,
    height: 480
  });
  camera.start();
}
