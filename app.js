const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const statusEl = document.getElementById('status');
const sourceLang = document.getElementById('sourceLang');
const targetLang = document.getElementById('targetLang');
const video = document.getElementById('video');
const overlay = document.getElementById('overlay');
const viewer = document.getElementById('viewer');
const lens = document.getElementById('lens');
const lensText = document.getElementById('lensText');
const rawText = document.getElementById('rawText');
const translatedText = document.getElementById('translatedText');
const captureCanvas = document.getElementById('captureCanvas');

const overlayCtx = overlay.getContext('2d');
const captureCtx = captureCanvas.getContext('2d', { willReadFrequently: true });

let stream;
let frameTimer;
let isProcessing = false;
let lastTranslation = '';
let lastRawText = '';
let hasPointer = false;

const OCR_INTERVAL_MS = 1500;
const LENS_SIZE = 180;
const DEFAULT_TARGET = 'en';

targetLang.value = DEFAULT_TARGET;

startBtn.addEventListener('click', startCamera);
stopBtn.addEventListener('click', stopCamera);

sourceLang.addEventListener('change', clearOutput);
targetLang.addEventListener('change', () => {
  clearOutput();
  statusEl.textContent = 'Target language changed. Keep hovering to translate.';
});

viewer.addEventListener('pointermove', (event) => {
  hasPointer = true;
  lens.hidden = false;
  moveLens(event);
});

viewer.addEventListener('pointerleave', () => {
  hasPointer = false;
  lens.hidden = true;
  overlayCtx.clearRect(0, 0, overlay.width, overlay.height);
});

async function startCamera() {
  if (stream) {
    return;
  }

  try {
    statusEl.textContent = 'Requesting camera access...';

    stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: { ideal: 'environment' },
      },
      audio: false,
    });

    video.srcObject = stream;
    await video.play();

    syncCanvasSize();
    window.addEventListener('resize', syncCanvasSize);

    frameTimer = setInterval(processFrame, OCR_INTERVAL_MS);

    startBtn.disabled = true;
    stopBtn.disabled = false;
    statusEl.textContent = 'Camera on. Hover over text to translate.';
  } catch (error) {
    statusEl.textContent = `Could not start camera: ${error.message}`;
  }
}

function stopCamera() {
  if (!stream) {
    return;
  }

  stream.getTracks().forEach((track) => track.stop());
  stream = null;

  if (frameTimer) {
    clearInterval(frameTimer);
    frameTimer = null;
  }

  window.removeEventListener('resize', syncCanvasSize);
  overlayCtx.clearRect(0, 0, overlay.width, overlay.height);

  startBtn.disabled = false;
  stopBtn.disabled = true;
  lens.hidden = true;
  statusEl.textContent = 'Camera stopped.';
}

function syncCanvasSize() {
  const rect = video.getBoundingClientRect();
  overlay.width = rect.width;
  overlay.height = rect.height;
  captureCanvas.width = rect.width;
  captureCanvas.height = rect.height;
}

function moveLens(event) {
  const rect = viewer.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;

  const boundedX = clamp(x, LENS_SIZE / 2, rect.width - LENS_SIZE / 2);
  const boundedY = clamp(y, LENS_SIZE / 2, rect.height - LENS_SIZE / 2);

  lens.style.left = `${boundedX}px`;
  lens.style.top = `${boundedY}px`;

  drawFocusBox(boundedX, boundedY);
}

function drawFocusBox(centerX, centerY) {
  overlayCtx.clearRect(0, 0, overlay.width, overlay.height);
  overlayCtx.strokeStyle = '#facc15';
  overlayCtx.lineWidth = 2;
  overlayCtx.setLineDash([6, 4]);
  overlayCtx.strokeRect(
    centerX - LENS_SIZE / 2,
    centerY - LENS_SIZE / 2,
    LENS_SIZE,
    LENS_SIZE
  );
  overlayCtx.setLineDash([]);
}

async function processFrame() {
  if (!stream || !hasPointer || isProcessing || lens.hidden) {
    return;
  }

  isProcessing = true;

  try {
    const lensRect = lens.getBoundingClientRect();
    const viewerRect = viewer.getBoundingClientRect();

    const x = clamp(lensRect.left - viewerRect.left - LENS_SIZE / 2, 0, captureCanvas.width - LENS_SIZE);
    const y = clamp(lensRect.top - viewerRect.top - LENS_SIZE / 2, 0, captureCanvas.height - LENS_SIZE);

    captureCtx.drawImage(video, 0, 0, captureCanvas.width, captureCanvas.height);

    const roi = captureCtx.getImageData(x, y, LENS_SIZE, LENS_SIZE);
    const roiCanvas = document.createElement('canvas');
    roiCanvas.width = LENS_SIZE;
    roiCanvas.height = LENS_SIZE;
    roiCanvas.getContext('2d').putImageData(roi, 0, 0);

    const result = await Tesseract.recognize(roiCanvas, sourceLang.value === 'auto' ? 'eng' : mapToTesseract(sourceLang.value), {
      logger: () => {},
    });

    const text = cleanText(result.data.text);
    if (!text || text === lastRawText) {
      return;
    }

    lastRawText = text;
    rawText.textContent = text;

    const translated = await translateText(text, sourceLang.value, targetLang.value);
    if (translated) {
      lastTranslation = translated;
      translatedText.textContent = translated;
      lensText.textContent = translated;
      statusEl.textContent = 'Live translation updated.';
    }
  } catch (error) {
    statusEl.textContent = `Translation error: ${error.message}`;
  } finally {
    isProcessing = false;
  }
}

function mapToTesseract(lang) {
  const map = {
    en: 'eng',
    es: 'spa',
    fr: 'fra',
    de: 'deu',
    it: 'ita',
    pt: 'por',
    ja: 'jpn',
    ko: 'kor',
    zh: 'chi_sim',
    ar: 'ara',
    hi: 'hin',
  };

  return map[lang] || 'eng';
}

async function translateText(text, source, target) {
  if (!text.trim()) {
    return '';
  }

  if (source !== 'auto' && source === target) {
    return text;
  }

  const url = new URL('https://api.mymemory.translated.net/get');
  url.searchParams.set('q', text);
  url.searchParams.set('langpair', `${source === 'auto' ? 'auto' : source}|${target}`);

  const response = await fetch(url.toString());
  if (!response.ok) {
    throw new Error(`Translate API failed (${response.status})`);
  }

  const data = await response.json();
  const translated = data?.responseData?.translatedText?.trim();

  return translated || '';
}

function clearOutput() {
  lastRawText = '';
  lastTranslation = '';
  rawText.textContent = 'No text yet.';
  translatedText.textContent = 'No translation yet.';
  lensText.textContent = 'Point at text';
}

function cleanText(text) {
  return text.replace(/\s+/g, ' ').trim();
}

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}
