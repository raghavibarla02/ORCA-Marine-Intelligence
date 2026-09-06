/**
 * ORCA - Ocean Risk & Condition Analyzer
 * Main UI Logic & Global Controllers
 */

document.addEventListener('DOMContentLoaded', () => {
  initSidebar();
  initClock();
  initLocationSelector();
  initFloatingAI();
  initSirenSimulator();
});

/* --------------------------------------------------------------------------
   1. Sidebar Controller (Desktop Collapse + Mobile Offcanvas)
   -------------------------------------------------------------------------- */
function initSidebar() {
  const sidebar = document.getElementById('orca-sidebar');
  const mainContent = document.getElementById('orca-main-content');
  const toggleBtn = document.getElementById('sidebar-toggle-btn');
  const mobileToggleBtn = document.getElementById('mobile-sidebar-toggle');

  if (toggleBtn && sidebar && mainContent) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('collapsed');
      mainContent.classList.toggle('expanded');
      
      // Save user preference
      const isCollapsed = sidebar.classList.contains('collapsed');
      localStorage.setItem('orca_sidebar_collapsed', isCollapsed);
    });

    // Restore user state
    if (localStorage.getItem('orca_sidebar_collapsed') === 'true' && window.innerWidth > 992) {
      sidebar.classList.add('collapsed');
      mainContent.classList.add('expanded');
    }
  }

  if (mobileToggleBtn && sidebar) {
    mobileToggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('show-mobile');
    });
  }
}

/* --------------------------------------------------------------------------
   2. Live UTC / IST Marine Clock
   -------------------------------------------------------------------------- */
function initClock() {
  const clockEl = document.getElementById('live-marine-clock');
  if (!clockEl) return;

  function update() {
    const now = new Date();
    const utcHours = String(now.getUTCHours()).padStart(2, '0');
    const utcMins = String(now.getUTCMinutes()).padStart(2, '0');
    const utcSecs = String(now.getUTCSeconds()).padStart(2, '0');
    
    // IST is UTC + 5:30
    const istOffset = 5.5 * 60 * 60 * 1000;
    const istTime = new Date(now.getTime() + istOffset);
    const istHours = String(istTime.getUTCHours()).padStart(2, '0');
    const istMins = String(istTime.getUTCMinutes()).padStart(2, '0');
    const istSecs = String(istTime.getUTCSeconds()).padStart(2, '0');

    clockEl.innerHTML = `<i class="bi bi-clock me-1 text-info"></i> ${istHours}:${istMins}:${istSecs} IST <span class="text-secondary small">(${utcHours}:${utcMins} UTC)</span>`;
  }

  update();
  setInterval(update, 1000);
}

/* --------------------------------------------------------------------------
   3. Location Switcher & Quick Search
   -------------------------------------------------------------------------- */
function initLocationSelector() {
  const select = document.getElementById('station-select');
  if (select) {
    select.addEventListener('change', (e) => {
      const stationSlug = e.target.value;
      if (stationSlug) {
        window.location.href = `/?station=${stationSlug}`;
      }
    });
  }

  const globalSearch = document.getElementById('global-station-search');
  if (globalSearch) {
    globalSearch.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        const val = globalSearch.value.trim().toLowerCase();
        if (val) {
          window.location.href = `/?station=${val}`;
        }
      }
    });
  }
}

/* --------------------------------------------------------------------------
   4. Floating AI Chatbot Widget
   -------------------------------------------------------------------------- */
function initFloatingAI() {
  const fab = document.getElementById('ai-fab-btn');
  const modalEl = document.getElementById('aiQuickModal');
  const chatInput = document.getElementById('quick-chat-input');
  const chatSend = document.getElementById('quick-chat-send');
  const chatMessages = document.getElementById('quick-chat-messages');

  if (!fab || !modalEl) return;

  const modal = new bootstrap.Modal(modalEl);

  fab.addEventListener('click', () => {
    modal.show();
  });

  function sendQuickMessage(text) {
    const msg = text || (chatInput ? chatInput.value.trim() : '');
    if (!msg) return;

    if (chatInput) chatInput.value = '';

    // Append User message
    const userMsgEl = document.createElement('div');
    userMsgEl.className = 'chat-bubble-user';
    userMsgEl.innerHTML = `<strong>You:</strong> <div>${escapeHtml(msg)}</div>`;
    chatMessages.appendChild(userMsgEl);

    // Append Loading indicator
    const loaderEl = document.createElement('div');
    loaderEl.className = 'chat-bubble-ai text-muted';
    loaderEl.id = 'ai-loading-bubble';
    loaderEl.innerHTML = `<span class="spinner-border spinner-border-sm me-2 text-info"></span> Analyzing marine sensors...`;
    chatMessages.appendChild(loaderEl);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Send to /api/chat/
    fetch('/api/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => {
      const loader = document.getElementById('ai-loading-bubble');
      if (loader) loader.remove();

      const aiMsgEl = document.createElement('div');
      aiMsgEl.className = 'chat-bubble-ai';
      aiMsgEl.innerHTML = formatMarkdown(data.response || 'No response available.');
      chatMessages.appendChild(aiMsgEl);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    })
    .catch(err => {
      const loader = document.getElementById('ai-loading-bubble');
      if (loader) loader.remove();

      const errorEl = document.createElement('div');
      errorEl.className = 'chat-bubble-ai text-danger';
      errorEl.textContent = 'Error connecting to ORCA AI server.';
      chatMessages.appendChild(errorEl);
    });
  }

  if (chatSend && chatInput) {
    chatSend.addEventListener('click', () => sendQuickMessage());
    chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        sendQuickMessage();
      }
    });
  }

  // Quick Chips in modal
  document.querySelectorAll('.quick-prompt-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const query = chip.getAttribute('data-query');
      if (query) sendQuickMessage(query);
    });
  });
}

/* --------------------------------------------------------------------------
   5. Web Audio API Maritime Siren Simulator
   -------------------------------------------------------------------------- */
let audioCtx = null;
let sirenOsc1 = null;
let sirenOsc2 = null;
let sirenGain = null;
let isSirenPlaying = false;
let sirenInterval = null;

function initSirenSimulator() {
  const btn = document.getElementById('siren-toggle-btn');
  if (!btn) return;

  btn.addEventListener('click', () => {
    if (!isSirenPlaying) {
      startSiren();
      btn.classList.add('active');
      btn.innerHTML = `<i class="bi bi-volume-mute-fill"></i> SILENCE ALARM`;
    } else {
      stopSiren();
      btn.classList.remove('active');
      btn.innerHTML = `<i class="bi bi-megaphone-fill"></i> TEST SIREN`;
    }
  });
}

function startSiren() {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContext();

    sirenGain = audioCtx.createGain();
    sirenGain.gain.setValueAtTime(0.12, audioCtx.currentTime);
    sirenGain.connect(audioCtx.destination);

    sirenOsc1 = audioCtx.createOscillator();
    sirenOsc1.type = 'sawtooth';
    sirenOsc1.frequency.setValueAtTime(450, audioCtx.currentTime);
    sirenOsc1.connect(sirenGain);
    sirenOsc1.start();

    let high = false;
    sirenInterval = setInterval(() => {
      if (!audioCtx) return;
      if (high) {
        sirenOsc1.frequency.exponentialRampToValueAtTime(440, audioCtx.currentTime + 0.3);
      } else {
        sirenOsc1.frequency.exponentialRampToValueAtTime(780, audioCtx.currentTime + 0.3);
      }
      high = !high;
    }, 400);

    isSirenPlaying = true;
  } catch (e) {
    console.warn("Audio context not allowed or failed:", e);
  }
}

function stopSiren() {
  if (sirenInterval) clearInterval(sirenInterval);
  if (sirenOsc1) {
    try { sirenOsc1.stop(); } catch(e) {}
    sirenOsc1.disconnect();
  }
  if (audioCtx) {
    audioCtx.close();
    audioCtx = null;
  }
  isSirenPlaying = false;
}

/* --------------------------------------------------------------------------
   Helpers
   -------------------------------------------------------------------------- */
function escapeHtml(string) {
  const entityMap = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  };
  return String(string).replace(/[&<>"']/g, s => entityMap[s]);
}

function formatMarkdown(text) {
  // Simple markdown renderer for AI responses (bold, headers, bullets)
  let html = escapeHtml(text);
  
  // Headers
  html = html.replace(/^### (.*$)/gim, '<h5 class="text-info mt-2 mb-2">$1</h5>');
  html = html.replace(/^## (.*$)/gim, '<h4 class="text-primary mt-2 mb-2">$1</h4>');
  html = html.replace(/^# (.*$)/gim, '<h3 class="text-white mt-2 mb-2">$1</h3>');
  
  // Bold
  html = html.replace(/\*\*(.*?)\*\*/gim, '<strong class="text-white">$1</strong>');
  
  // Italics
  html = html.replace(/\*(.*?)\*/gim, '<em>$1</em>');
  
  // Bullet points
  html = html.replace(/^\* (.*$)/gim, '<li class="mb-1">$1</li>');
  html = html.replace(/<\/li>\n<li>/gim, '</li><li>');
  html = html.replace(/(<li>.*<\/li>)/gims, '<ul class="mb-2 ps-3">$1</ul>');

  // Line breaks
  html = html.replace(/\n\n/g, '<br/>');

  return html;
}
