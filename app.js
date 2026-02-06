const imageInput = document.getElementById('imageInput');
const preview = document.getElementById('preview');
const analyzeBtn = document.getElementById('analyzeBtn');
const manualQuery = document.getElementById('manualQuery');
const keywordList = document.getElementById('keywordList');
const results = document.getElementById('results');
const analysisPanel = document.getElementById('analysisPanel');
const resultsPanel = document.getElementById('resultsPanel');

let classifier;

const sites = [
  {
    name: 'Yoox',
    builder: (q) => `https://www.yoox.com/searchresult?text=${encodeURIComponent(q)}`,
  },
  {
    name: 'Net-a-Porter',
    builder: (q) => `https://www.net-a-porter.com/en-us/shop/search/${encodeURIComponent(q)}`,
  },
  {
    name: 'SSG',
    builder: (q) => `https://www.ssg.com/search.ssg?target=all&query=${encodeURIComponent(q)}`,
  },
  {
    name: 'Kream',
    builder: (q) => `https://kream.co.kr/search?keyword=${encodeURIComponent(q)}`,
  },
  {
    name: 'Jente',
    builder: (q) => `https://jente.kr/search?keyword=${encodeURIComponent(q)}`,
  },
  {
    name: 'SSENSE',
    builder: (q) => `https://www.ssense.com/en-us/search?q=${encodeURIComponent(q)}`,
  },
  {
    name: 'Cettire',
    builder: (q) => `https://www.cettire.com/search?q=${encodeURIComponent(q)}`,
  },
];

imageInput.addEventListener('change', () => {
  const file = imageInput.files?.[0];
  if (!file) {
    return;
  }

  preview.src = URL.createObjectURL(file);
  preview.hidden = false;
  analyzeBtn.disabled = false;
});

analyzeBtn.addEventListener('click', async () => {
  analyzeBtn.disabled = true;
  analyzeBtn.textContent = 'Analyzing image...';

  try {
    if (!classifier) {
      classifier = await mobilenet.load();
    }

    const predictions = await classifier.classify(preview, 5);
    const keywords = buildKeywords(predictions);
    const finalQuery = manualQuery.value.trim() || keywords.join(' ');

    renderKeywords(keywords);
    renderResults(finalQuery);
  } catch (error) {
    alert(`Failed to analyze image: ${error.message}`);
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = 'Analyze image & search';
  }
});

function buildKeywords(predictions) {
  const cleaned = predictions
    .flatMap((p) => p.className.split(','))
    .map((token) => token.trim().toLowerCase())
    .filter((token) => token.length > 2)
    .map((token) => token.replace(/[_-]/g, ' '));

  return [...new Set(cleaned)].slice(0, 6);
}

function renderKeywords(keywords) {
  analysisPanel.hidden = false;
  keywordList.innerHTML = '';

  keywords.forEach((kw) => {
    const li = document.createElement('li');
    li.textContent = kw;
    keywordList.appendChild(li);
  });
}

function renderResults(query) {
  resultsPanel.hidden = false;
  results.innerHTML = '';

  sites.forEach((site) => {
    const card = document.createElement('article');
    card.className = 'result-card';

    const title = document.createElement('h3');
    title.textContent = site.name;

    const link = document.createElement('a');
    link.href = site.builder(query);
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.textContent = `Search "${query}"`;

    card.appendChild(title);
    card.appendChild(link);
    results.appendChild(card);
  });
}
