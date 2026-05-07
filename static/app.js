const partyNameMap={TVK:'Tamilaga Vettri Kazhagam - TVK',DMK:'Dravida Munnetra Kazhagam - DMK',ADMK:'All India Anna Dravida Munnetra Kazhagam - ADMK',AIADMK:'All India Anna Dravida Munnetra Kazhagam - ADMK',INC:'Indian National Congress - INC',PMK:'Pattali Makkal Katchi - PMK',IUML:'Indian Union Muslim League - IUML',CPI:'Communist Party of India - CPI',VCK:'Viduthalai Chiruthaigal Katchi - VCK','CPI(M)':'Communist Party of India (Marxist) - CPI(M)',BJP:'Bharatiya Janata Party - BJP',DMDK:'Desiya Murpokku Dravida Kazhagam - DMDK',AMMKMNKZ:'Amma Makkal Munnettra Kazagam - AMMKMNKZ'};
const partyLogoMap = {
  TVK: 'https://m.media-amazon.com/images/I/71SNsN9E2vL._SL1500_.jpg',
  DMK: 'https://m.media-amazon.com/images/I/61RUjvZZuyL._SL1500_.jpg',
  ADMK: 'https://m.media-amazon.com/images/I/71tftHQGCcL._UF1000,1000_QL80_.jpg',
  AIADMK: 'https://www.thestatesman.com/wp-content/uploads/2017/08/1490172942-aiadmk-symbol.jpg',
  INC: 'https://m.media-amazon.com/images/I/41ieXlOwDmL._SL1200_.jpg',
  PMK: 'https://m.media-amazon.com/images/I/71a4ZP1A70L._SY625_.jpg',
  CPI: 'https://m.media-amazon.com/images/I/41ieXlOwDmL._SL1200_.jpg',
  IUML: 'https://m.media-amazon.com/images/I/51of-PRfgcL._AC_UL480_FMwebp_QL65_.jpg',
  VCK: 'https://upload.wikimedia.org/wikipedia/en/0/0e/Viduthalai_Chiruthaigal_Katchi_Party_logo.png',
  CPIM: 'https://m.media-amazon.com/images/I/515CHEmp8bL.jpg',
  BJP: 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Logo_of_the_Bharatiya_Janata_Party.svg/1280px-Logo_of_the_Bharatiya_Janata_Party.svg.png',
  DMDK: 'https://upload.wikimedia.org/wikipedia/commons/2/22/Indian_Election_Symbol_Nagara.svg',
  AMMKMNKZ: 'https://upload.wikimedia.org/wikipedia/commons/9/9e/All_India_Majlis-e-Ittehadul_Muslimeen_logo.svg'
};
const staticConstituencies = [
  { constituency_name: 'Chepauk-Thiruvallikeni', leading_party: 'DMK', vote_share: 57.4, turnout_pct: 74.2, lat: 13.0604, lon: 80.2825 },
  { constituency_name: 'Coimbatore South', leading_party: 'TVK', vote_share: 49.8, turnout_pct: 78.6, lat: 11.0168, lon: 76.9558 },
  { constituency_name: 'Madurai Central', leading_party: 'AIADMK', vote_share: 46.1, turnout_pct: 76.4, lat: 9.9252, lon: 78.1198 },
  { constituency_name: 'Salem North', leading_party: 'PMK', vote_share: 44.9, turnout_pct: 79.1, lat: 11.6643, lon: 78.1460 },
  { constituency_name: 'Tirunelveli', leading_party: 'INC', vote_share: 48.7, turnout_pct: 77.2, lat: 8.7139, lon: 77.7567 },
  { constituency_name: 'Villupuram', leading_party: 'DMK', vote_share: 51.6, turnout_pct: 75.8, lat: 11.9401, lon: 79.4861 },
  { constituency_name: 'Erode East', leading_party: 'TVK', vote_share: 47.2, turnout_pct: 80.3, lat: 11.3410, lon: 77.7172 },
  { constituency_name: 'Nagapattinam', leading_party: 'CPI', vote_share: 45.5, turnout_pct: 81.0, lat: 10.7656, lon: 79.8428 }
];
const staticCloseFights = [
  { constituency: 'Coimbatore South', winner_party: 'TVK', runner_party: 'DMK', margin_votes: 1268 },
  { constituency: 'Madurai Central', winner_party: 'AIADMK', runner_party: 'DMK', margin_votes: 932 },
  { constituency: 'Villupuram', winner_party: 'DMK', runner_party: 'AIADMK', margin_votes: 1504 },
  { constituency: 'Tirunelveli', winner_party: 'INC', runner_party: 'TVK', margin_votes: 1889 },
  { constituency: 'Salem North', winner_party: 'PMK', runner_party: 'DMK', margin_votes: 2094 }
];
const staticPartySummary = [
  { party: 'TVK', party_name: 'Tamilaga Vettri Kazhagam - TVK', won: 108, leading: 0, total: 108 },
  { party: 'DMK', party_name: 'Dravida Munnetra Kazhagam - DMK', won: 59, leading: 0, total: 59 },
  { party: 'ADMK', party_name: 'All India Anna Dravida Munnetra Kazhagam - ADMK', won: 47, leading: 0, total: 47 },
  { party: 'INC', party_name: 'Indian National Congress - INC', won: 5, leading: 0, total: 5 },
  { party: 'PMK', party_name: 'Pattali Makkal Katchi - PMK', won: 4, leading: 0, total: 4 },
  { party: 'IUML', party_name: 'Indian Union Muslim League - IUML', won: 2, leading: 0, total: 2 },
  { party: 'CPI', party_name: 'Communist Party of India - CPI', won: 2, leading: 0, total: 2 },
  { party: 'VCK', party_name: 'Viduthalai Chiruthaigal Katchi - VCK', won: 2, leading: 0, total: 2 },
  { party: 'CPI(M)', party_name: 'Communist Party of India (Marxist) - CPI(M)', won: 2, leading: 0, total: 2 },
  { party: 'BJP', party_name: 'Bharatiya Janata Party - BJP', won: 1, leading: 0, total: 1 },
  { party: 'DMDK', party_name: 'Desiya Murpokku Dravida Kazhagam - DMDK', won: 1, leading: 0, total: 1 },
  { party: 'AMMKMNKZ', party_name: 'Amma Makkal Munnettra Kazagam - AMMKMNKZ', won: 1, leading: 0, total: 1 }
];

const THEME_KEY = 'dashboard-theme';
const DEFAULT_BOT_MESSAGE = `
Welcome to the Election Intelligence Copilot 🇮🇳

Ask anything about:
• Party performance
• Constituency trends
• Vote share analysis
• Swing predictions
• Turnout insights
• Candidate comparisons
• ML-based election forecasting

Transform complex election data into
clear, interactive, and intelligent insights.
`;
let map;
let mapLayer;
let partyChart;
let turnoutChart;
let allPartiesBarChart;
const errorBox = document.getElementById('errorBox');
const themeToggle = document.getElementById('themeToggle');
const floatingChatbot = document.getElementById('floatingChatbot');
const floatingChatMessages = document.getElementById('floatingChatMessages');
const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');
const chatSendBtn = document.getElementById('chatSendBtn');
const chatCloseBtn = document.getElementById('chatCloseBtn');
const chatOpenBtn = document.getElementById('chatOpenBtn');
const refreshBtn = document.getElementById('refreshBtn');
let chatPending = false;

function pushChatMessage(role, message){
  if(!floatingChatMessages) return;
  const li = document.createElement('li');
  li.className = `chat-msg ${role}`;
  li.innerHTML = `<span class="chat-avatar">${role === 'user' ? '<i class="bi bi-person-fill"></i>' : '<i class="bi bi-stars"></i>'}</span><div class="chat-bubble">${String(message || '').replace(/</g,'&lt;').replace(/>/g,'&gt;')}</div>`;
  floatingChatMessages.appendChild(li);
  floatingChatMessages.scrollTop = floatingChatMessages.scrollHeight;
}

function setChatPending(isPending){
  chatPending = isPending;
  if(chatInput) chatInput.disabled = isPending;
  if(chatSendBtn) chatSendBtn.disabled = isPending;
}

function showChatTypingLoader(){
  if(!floatingChatMessages) return null;
  const li = document.createElement('li');
  li.className = 'chat-msg bot typing';
  li.setAttribute('data-chat-loader', 'true');
  li.innerHTML = `<span class="chat-avatar"><i class="bi bi-stars"></i></span><div class="chat-bubble"><span class="chat-typing-dots" aria-label="Gemini is typing"><span></span><span></span><span></span></span></div>`;
  floatingChatMessages.appendChild(li);
  floatingChatMessages.scrollTop = floatingChatMessages.scrollHeight;
  return li;
}

function hideChatTypingLoader(loaderNode){
  const target = loaderNode || (floatingChatMessages ? floatingChatMessages.querySelector('[data-chat-loader="true"]') : null);
  if(target && target.parentNode){
    target.parentNode.removeChild(target);
  }
}

function openChatbot(){
  if(floatingChatbot) floatingChatbot.classList.remove('is-hidden');
  if(chatOpenBtn) chatOpenBtn.style.display = 'none';
}

function closeChatbot(){
  if(floatingChatbot) floatingChatbot.classList.add('is-hidden');
  if(chatOpenBtn) chatOpenBtn.style.display = 'inline-flex';
}

async function sendChatMessage(message){
  const prompt = String(message || '').trim();
  if(!prompt || chatPending) return;
  pushChatMessage('user', prompt);
  setChatPending(true);
  const loaderNode = showChatTypingLoader();
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: prompt })
    });
    if(!response.ok){
      throw new Error(`chat api failed: ${response.status}`);
    }
    const payload = await response.json();
    hideChatTypingLoader(loaderNode);
    pushChatMessage('bot', payload.reply || 'No response available right now.');
  } catch (error) {
    hideChatTypingLoader(loaderNode);
    pushChatMessage('bot', 'Chat is temporarily unavailable. Please refresh and try again.');
  } finally {
    setChatPending(false);
    if(chatInput) chatInput.focus();
  }
}

function applyTheme(theme){
  document.documentElement.setAttribute('data-theme', theme);
  if(themeToggle){
    themeToggle.textContent = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
  }
}

function initTheme(){
  const stored = localStorage.getItem(THEME_KEY);
  const fallback = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  applyTheme(stored || fallback);
}

function toggleTheme(){
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  const next = current === 'dark' ? 'light' : 'dark';
  localStorage.setItem(THEME_KEY, next);
  applyTheme(next);
}

function setLoading(isLoading){
  document.body.classList.toggle('is-loading', isLoading);
  if(refreshBtn){
    refreshBtn.disabled = isLoading;
    refreshBtn.textContent = isLoading ? 'Refreshing...' : 'Refresh';
  }
  const root = document.getElementById('topCards');
  if(!root) return;
  if(isLoading && !root.children.length){
    root.innerHTML = Array.from({length: 6}).map(() =>
      "<div class='card skeleton-card'><div class='skeleton-line'></div><div class='skeleton-pill'></div></div>"
    ).join('');
  }
}

function animateCount(el, value, suffix=''){
  if(!el) return;
  const target = Number(value || 0);
  const duration = 900;
  const start = performance.now();
  function frame(now){
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = `${Math.round(target * eased)}${suffix}`;
    if(progress < 1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}

function normalizePartyKey(text){
  return String(text || '').toUpperCase().replace(/[^A-Z]/g, '');
}

function extractTrailingPartyCode(text){
  const source = String(text || '').toUpperCase().trim();
  const match = source.match(/-\s*([A-Z0-9()]+)\s*$/);
  return match ? match[1] : '';
}

function getPartyLogo(party){
  const raw = String(party || '').toUpperCase().trim();
  const normalized = normalizePartyKey(raw);
  const trailingCode = extractTrailingPartyCode(raw);

  if(partyLogoMap[raw]) return partyLogoMap[raw];
  if(trailingCode && partyLogoMap[trailingCode]) return partyLogoMap[trailingCode];

  const normalizedKeyEntry = Object.keys(partyLogoMap).find(k => normalizePartyKey(k) === normalized);
  if(normalizedKeyEntry) return partyLogoMap[normalizedKeyEntry];

  const boundaryEntry = Object.keys(partyLogoMap)
    .sort((a, b) => b.length - a.length)
    .find(k => new RegExp(`(^|[^A-Z0-9])${k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}($|[^A-Z0-9])`).test(raw));

  return boundaryEntry ? partyLogoMap[boundaryEntry] : '';
}

function getPartyInitials(party){
  const source = String(party || '').trim();
  if(!source) return 'P';
  if(/^[A-Za-z0-9()./&-]{2,10}$/.test(source) && !/\s/.test(source)){
    return source.toUpperCase();
  }
  if(source.includes('-')){
    const parts = source.split('-').map(s => s.trim()).filter(Boolean);
    if(parts.length) return parts[parts.length - 1].toUpperCase();
  }
  const words = source.split(/\s+/).filter(Boolean);
  if(words.length === 1) return words[0].toUpperCase();
  return words.slice(0, 2).map(w => w[0]).join('').toUpperCase();
}

function partyIdentityHtml(party, className = 'party-identity'){
  const logoUrl = getPartyLogo(party);
  const initials = getPartyInitials(party);
  return `<span class="${className}"><img class="party-logo" src="${logoUrl}" alt="${party} logo" loading="lazy" onerror="this.style.display='none'; this.nextElementSibling.style.display='inline-flex';" /><span class="party-fallback" style="display:${logoUrl ? 'none' : 'inline-flex'}">${initials}</span><span class="party-label">${party}</span></span>`;
}

function partyLogoBadgeHtml(party){
  const logoUrl = getPartyLogo(party);
  const initials = getPartyInitials(party);
  return `<span class="party-badge"><img class="party-logo" src="${logoUrl}" alt="${party} logo" loading="lazy" onerror="this.style.display='none'; this.nextElementSibling.style.display='inline-flex';" /><span class="party-fallback" style="display:${logoUrl ? 'none' : 'inline-flex'}">${initials}</span></span>`;
}

function showError(message){
  if(!errorBox) return;
  errorBox.style.display='block';
  errorBox.textContent=message;
}
function clearError(){
  if(!errorBox) return;
  errorBox.style.display='none';
  errorBox.textContent='';
}

function buildFallbackSummary(constituencies){
  const party_table = staticPartySummary.map(row => ({ ...row }));

  return {
    total_ac: 234,
    majority: 118,
    top_cards: party_table.slice(0, 7),
    party_table,
    updated: new Date().toISOString()
  };
}

async function loadAll(){
  try {
    clearError();
    setLoading(true);
    const [summaryResult,constituenciesResult]=await Promise.allSettled([
      fetchJson('/api/summary', 5000),
      fetchJson('/api/constituencies', 5000)
    ]);

    const apiConstituencies = constituenciesResult.status === 'fulfilled' ? constituenciesResult.value : [];
    const constituencies = (apiConstituencies && apiConstituencies.length) ? apiConstituencies : staticConstituencies;
    const summary = summaryResult.status === 'fulfilled' && summaryResult.value
      ? summaryResult.value
      : buildFallbackSummary(constituencies);

    if(!summary.top_cards || !summary.party_table){
      const fallbackSummary = buildFallbackSummary(constituencies);
      summary.top_cards = fallbackSummary.top_cards;
      summary.party_table = fallbackSummary.party_table;
      summary.total_ac = summary.total_ac || fallbackSummary.total_ac;
    }
    const analytics = {
      high_turnout: [...constituencies].sort((a,b)=>Number(b.turnout_pct||0)-Number(a.turnout_pct||0)).slice(0,5),
      close_fights: staticCloseFights,
      gemini_summary: '',
      ml: { status: 'skipped', reason: 'Analytics loading...' },
      data_quality: {
        shape: {
          rows: constituencies.length,
          columns: 7
        },
        duplicates: 0
      }
    };

    const totalAcEl = document.getElementById('totalAc');
    if(totalAcEl){
      totalAcEl.textContent='0';
      animateCount(totalAcEl, summary.total_ac);
    }
    const updatedAt = new Date(summary.updated);
    const dd = String(updatedAt.getDate()).padStart(2, '0');
    const mm = String(updatedAt.getMonth() + 1).padStart(2, '0');
    const yyyy = updatedAt.getFullYear();
    const hh = String(updatedAt.getHours()).padStart(2, '0');
    const min = String(updatedAt.getMinutes()).padStart(2, '0');
    const ss = String(updatedAt.getSeconds()).padStart(2, '0');
    document.getElementById('lastUpdated').textContent=`${dd}/${mm}/${yyyy}, ${hh}:${min}:${ss}`;
    renderCards(summary.top_cards);
    renderPartyTable(summary.party_table, summary.total_ac);
    renderMap(constituencies);
    renderLists(analytics);
    renderConstituencyTable(constituencies);
    renderCharts(summary, analytics);
    renderGeminiSummary();

    fetchJson('/api/analytics', 6000)
      .then((analyticsBase) => {
        const hydrated = {
          ...analytics,
          ...analyticsBase,
          high_turnout: (analyticsBase.high_turnout && analyticsBase.high_turnout.length)
            ? analyticsBase.high_turnout
            : analytics.high_turnout,
          close_fights: (analyticsBase.close_fights && analyticsBase.close_fights.length)
            ? analyticsBase.close_fights
            : analytics.close_fights,
          data_quality: {
            shape: {
              rows: (analyticsBase.data_quality?.shape?.rows ?? 0) || constituencies.length,
              columns: (analyticsBase.data_quality?.shape?.columns ?? 0) || 7
            },
            duplicates: analyticsBase.data_quality?.duplicates ?? 0
          }
        };
        renderLists(hydrated);
        renderCharts(summary, hydrated);
        renderGeminiSummary();
      })
      .catch(() => {});
  } catch (e) {
    console.error(e);
    const summary = buildFallbackSummary(staticConstituencies);
    const analytics = {
      high_turnout: [...staticConstituencies].sort((a,b)=>Number(b.turnout_pct||0)-Number(a.turnout_pct||0)).slice(0,5),
      close_fights: staticCloseFights,
      gemini_summary: '',
      ml: { status: 'skipped', reason: 'Analytics loading...' },
      data_quality: { shape: { rows: staticConstituencies.length, columns: 7 }, duplicates: 0 }
    };
    renderCards(summary.top_cards);
    renderPartyTable(summary.party_table, summary.total_ac);
    renderMap(staticConstituencies);
    renderLists(analytics);
    renderConstituencyTable(staticConstituencies);
    renderCharts(summary, analytics);
    showError('Live APIs are delayed. Showing baseline dashboard data instantly.');
    renderGeminiSummary();
  } finally {
    setLoading(false);
  }
}

async function fetchJson(url, timeoutMs = 6000){
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, { signal: controller.signal });
    if(!response.ok){
      const text = await response.text();
      throw new Error(`${url} -> ${response.status} ${text}`);
    }
    return response.json();
  } catch (error) {
    if(error && error.name === 'AbortError'){
      throw new Error(`${url} -> timeout after ${timeoutMs}ms`);
    }
    throw error;
  } finally {
    clearTimeout(timer);
  }
}
function renderCards(items){
  const root=document.getElementById('topCards');
  if(!root) return;
  root.innerHTML='';
  (items || []).forEach((i, index)=>{
    const d=document.createElement('div');
    d.className='card';
    d.style.setProperty('--card-index', index);
    const partyLabel = i.party_name || partyNameMap[i.party] || i.party || '';
    const partyCode = getPartyInitials(partyLabel);
    const isTVK = String(partyLabel).toUpperCase().includes('TVK');
    d.innerHTML=`${isTVK ? "<span class='card-crown' aria-label='Crown'>👑</span>" : ''}<div class='card-top'>${partyLogoBadgeHtml(partyLabel)}<span class='party-code'>${partyCode}</span></div><div class='party-full-name'>${partyLabel}</div><div class='n'>0</div>`;
    const n = d.querySelector('.n');
    animateCount(n, i.won);
    root.appendChild(d);
  });
}
function renderPartyTable(rows,total){
  const tbody=document.querySelector('#partyTable tbody');
  if(!tbody) return;
  tbody.innerHTML='';
  rows.forEach(r=>{const tr=document.createElement('tr'); const p=r.party_name||partyNameMap[r.party]||r.party; tr.innerHTML=`<td>${partyIdentityHtml(p, 'party-identity compact')}</td><td>${r.won}</td><td>${r.leading}</td><td>${r.total}</td>`; tbody.appendChild(tr);});
  const tr=document.createElement('tr'); tr.innerHTML=`<td><strong>Total</strong></td><td><strong>${total}</strong></td><td><strong>0</strong></td><td><strong>${total}</strong></td>`; tbody.appendChild(tr);
}
function renderMap(points){
  if(!map){
    map=L.map('map').setView([11.1,78.2],7);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap contributors'}).addTo(map);
  }
  if(!points.length) return;
  if(mapLayer){ map.removeLayer(mapLayer); }
  mapLayer=L.layerGroup();
  points.forEach(p=>{if(p.lat&&p.lon){L.circleMarker([p.lat,p.lon],{radius:6,weight:1,fillOpacity:0.65}).addTo(mapLayer).bindPopup(`<b>${p.constituency_name}</b><br/>${p.leading_party}<br/>Vote share: ${Number(p.vote_share||0).toFixed(1)}%<br/>Turnout: ${Number(p.turnout_pct||0).toFixed(1)}%`);}});
  mapLayer.addTo(map);
  if(points.length){
    const bounds=L.latLngBounds(points.filter(p=>p.lat&&p.lon).map(p=>[Number(p.lat),Number(p.lon)]));
    if(bounds.isValid()) map.fitBounds(bounds.pad(0.1));
  }
}
function renderLists(data){
  const t=document.getElementById('turnoutList');
  const c=document.getElementById('closeList');
  if(!t || !c) return;
  t.innerHTML=''; c.innerHTML='';
  (data.high_turnout || []).forEach(i=>{
    const li=document.createElement('li');
    li.textContent=`${i.constituency_name || i.constituency || '-'} - ${i.leading_party || i.winner_party || '-'} (${Number(i.turnout_pct||0).toFixed(1)}%)`;
    t.appendChild(li);
  });

  (data.close_fights || []).forEach(i=>{
    const li=document.createElement('li');
    if(i.margin_votes !== undefined){
      li.textContent=`${i.constituency} - ${i.winner_party} vs ${i.runner_party} (margin ${i.margin_votes} votes)`;
    } else {
      li.textContent=`${i.constituency_name || '-'} - ${i.leading_party || '-'} (${Number(i.vote_share||0).toFixed(1)}%)`;
    }
    c.appendChild(li);
  });

  const mlBox=document.getElementById('mlStatus');
  const qualityBox=document.getElementById('dataQuality');
  if(mlBox){
    if(data.ml && data.ml.status === 'ok'){
      mlBox.textContent = data.ml.scores.map(s => `${s.model}: ${s.accuracy}`).join(' | ');
    } else {
      mlBox.textContent = (data.ml && data.ml.reason) ? data.ml.reason : 'ML analysis skipped';
    }
  }

  if(qualityBox && data.data_quality){
    const shape = data.data_quality.shape || {};
    qualityBox.textContent = `Rows: ${shape.rows ?? '-'} | Columns: ${shape.columns ?? '-'} | Duplicates: ${data.data_quality.duplicates ?? '-'}`;
  }
}

function renderConstituencyTable(rows){
  const tbody=document.querySelector('#constTable tbody');
  if(!tbody) return;
  tbody.innerHTML='';
  rows.slice(0,234).forEach(r=>{
    const tr=document.createElement('tr');
    tr.innerHTML=`<td>${r.constituency_name}</td><td>${r.leading_party}</td><td>${Number(r.vote_share||0).toFixed(1)}%</td><td>${Number(r.turnout_pct||0).toFixed(1)}%</td>`;
    tbody.appendChild(tr);
  });
}

function renderGeminiSummary(){
  if(!floatingChatMessages) return;
  floatingChatMessages.innerHTML = '';
  pushChatMessage('bot', DEFAULT_BOT_MESSAGE);
}

function renderCharts(summary, analytics){
  const partyCanvas = document.getElementById('partySeatsChart');
  const turnoutCanvas = document.getElementById('turnoutChart');
  const allPartiesCanvas = document.getElementById('allPartiesBarChart');
  if(!partyCanvas || !turnoutCanvas || !allPartiesCanvas) return;

  const parties = (summary.party_table || []).slice(0, 10);
  const labels = parties.map(p => p.party_name || partyNameMap[p.party] || p.party);
  const wonValues = parties.map(p => p.won);

  if(partyChart){ partyChart.destroy(); }
  partyChart = new Chart(partyCanvas, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data: wonValues,
        backgroundColor: ['#2563eb','#ef4444','#10b981','#f59e0b','#8b5cf6','#14b8a6','#f43f5e','#22c55e','#06b6d4','#eab308']
      }]
    },
    options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
  });

  const turnout = (analytics.high_turnout || []).slice(0, 8);
  const tLabels = turnout.map(i => i.constituency_name || i.constituency || '-');
  const tValues = turnout.map(i => Number(i.turnout_pct || 0));

  if(turnoutChart){ turnoutChart.destroy(); }
  turnoutChart = new Chart(turnoutCanvas, {
    type: 'bar',
    data: {
      labels: tLabels,
      datasets: [{ label: 'Turnout %', data: tValues, backgroundColor: '#3b82f6' }]
    },
    options: {
      responsive: true,
      indexAxis: 'y',
      scales: { x: { beginAtZero: true, max: 100 } },
      plugins: { legend: { display: false } }
    }
  });

  if(allPartiesBarChart){ allPartiesBarChart.destroy(); }
  const allParties = (summary.party_table || []);
  allPartiesBarChart = new Chart(allPartiesCanvas, {
    type: 'bar',
    data: {
      labels: allParties.map(p => p.party_name || partyNameMap[p.party] || p.party),
      datasets: [{
        label: 'Seats Won',
        data: allParties.map(p => Number(p.won || 0)),
        backgroundColor: ['#2563eb','#ef4444','#10b981','#f59e0b','#8b5cf6','#14b8a6','#f43f5e','#22c55e','#06b6d4','#eab308'],
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
    }
  });
}

if(themeToggle){
  themeToggle.addEventListener('click', toggleTheme);
}
if(chatCloseBtn){
  chatCloseBtn.addEventListener('click', closeChatbot);
}
if(chatOpenBtn){
  chatOpenBtn.addEventListener('click', openChatbot);
}
if(chatForm){
  chatForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    if(chatPending) return;
    const prompt = chatInput ? chatInput.value : '';
    if(!String(prompt || '').trim()) return;
    if(chatInput) chatInput.value = '';
    await sendChatMessage(prompt);
  });
}
if(refreshBtn){
  refreshBtn.addEventListener('click', async (event) => {
    event.preventDefault();
    if(refreshBtn.disabled) return;
    await loadAll();
  });
}
initTheme();
openChatbot();
loadAll();
