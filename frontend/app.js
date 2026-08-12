const state = {
  traces: [],
  variables: [],
  scrubIndex: 0,
  session: '',
  playing: false,
  playTimer: null,
};

const PALETTE = ['#1FAE85', '#3D8BE0', '#F2A65A', '#E0654C', '#2DD9A8', '#34D399'];

function colorFor(name) {
  let h = 0;
  for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) >>> 0;
  return PALETTE[h % PALETTE.length];
}

function fmtValue(raw) {
  let v;
  try { v = JSON.parse(raw); } catch (e) { v = raw; }
  if (typeof v === 'string') return '"' + v + '"';
  if (v === null) return 'None';
  if (typeof v === 'boolean') return v ? 'True' : 'False';
  return String(v);
}

async function fetchJSON(url, options) {
  const res = await fetch(API_BASE_URL + url, options);
  if (!res.ok) {
    let msg;
    try { msg = (await res.json()).detail; } catch (e) { msg = await res.text(); }
    throw new Error(msg || ('request failed (' + res.status + ')'));
  }
  return res.json();
}

/* ---- Navigation ------------------------------------------------------- */
const navLabels = { dashboard: 'Dashboard', timetravel: 'Time Travel', variables: 'Variables', snapshots: 'Snapshots', settings: 'Settings' };

document.querySelectorAll('.nav-item').forEach((btn) => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.nav-item').forEach((b) => b.classList.remove('active'));
    btn.classList.add('active');
    const target = btn.dataset.target;
    document.querySelectorAll('.page').forEach((p) => p.classList.remove('active'));
    document.getElementById('page-' + target).classList.add('active');
    document.getElementById('breadcrumbCurrent').textContent = navLabels[target];
  });
});

function goTo(target) {
  document.querySelector('.nav-item[data-target="' + target + '"]').click();
}

/* ---- Data loading ------------------------------------------------------- */
async function loadSessions() {
  const sessions = await fetchJSON('/api/sessions');
  const sel = document.getElementById('sessionSelect');
  sel.innerHTML = '<option value="">All sessions</option>';
  for (const s of sessions) {
    const opt = document.createElement('option');
    opt.value = s; opt.textContent = s;
    sel.appendChild(opt);
  }
  if (sessions.length) { state.session = sessions[sessions.length - 1]; sel.value = state.session; }

  const tbody = document.getElementById('sessionsTableBody');
  tbody.innerHTML = '';
  document.getElementById('sessionsEmptyHint').hidden = sessions.length > 0;
  for (const s of sessions) {
    const tr = document.createElement('tr');
    tr.innerHTML = '<td class="mono">' + s + '</td><td class="mono">—</td>' +
      '<td><button class="ghost" data-session="' + s + '">Open</button></td>';
    tr.querySelector('button').addEventListener('click', () => {
      state.session = s;
      document.getElementById('sessionSelect').value = s;
      load().then(() => goTo('timetravel'));
    });
    tbody.appendChild(tr);
  }
}

async function load() {
  const q = state.session ? '?session=' + encodeURIComponent(state.session) : '';
  const [traces, variables] = await Promise.all([
    fetchJSON('/api/timeline' + q),
    fetchJSON('/api/variables' + q),
  ]);
  state.traces = traces;
  state.variables = variables;
  state.scrubIndex = traces.length ? traces.length - 1 : 0;

  document.getElementById('sessionTag').textContent = state.session ? state.session : (traces.length ? 'all sessions' : 'no session');

  renderTicks();
  renderTransport();
  renderSnapshotPanels();
  renderVariablesTable();
  renderSnapshotsTable();
}

/* ---- Time Travel rendering ------------------------------------------------ */
function renderTicks() {
  const wrap = document.getElementById('ticks');
  wrap.innerHTML = '';
  const n = state.traces.length;
  const playBtn = document.getElementById('playBtn');
  const stepBack = document.getElementById('stepBack');
  const stepFwd = document.getElementById('stepFwd');
  playBtn.disabled = stepBack.disabled = stepFwd.disabled = n === 0;
  document.getElementById('ttEmptyHint').hidden = n > 0;

  state.traces.forEach((tr, i) => {
    const pct = n === 1 ? 0 : (i / (n - 1)) * 100;
    const tick = document.createElement('div');
    tick.className = 'tick' + (i === state.scrubIndex ? ' active' : '');
    tick.style.left = pct + '%';
    tick.title = 'L' + tr.line_number + ' ' + tr.variable_name;
    tick.addEventListener('click', () => { state.scrubIndex = i; renderAll(); });
    wrap.appendChild(tick);
  });
}

function renderTransport() {
  const n = state.traces.length;
  document.getElementById('counterIndex').textContent = n ? state.scrubIndex + 1 : 0;
  document.getElementById('counterTotal').textContent = n;
}

function reconstructStateAt(index) {
  const latest = new Map();
  for (let i = 0; i <= index; i++) latest.set(state.traces[i].variable_name, state.traces[i]);
  return Array.from(latest.values());
}

function renderSnapshotPanels() {
  const n = state.traces.length;
  if (!n) {
    ['infoLine','infoVar','infoScope','infoTime','infoValue'].forEach((id) => document.getElementById(id).textContent = '—');
    document.getElementById('snapshotVarsBody').innerHTML = '';
    return;
  }
  const row = state.traces[state.scrubIndex];
  document.getElementById('infoLine').textContent = row.line_number;
  document.getElementById('infoVar').textContent = row.variable_name;
  document.getElementById('infoScope').textContent = row.scope;
  document.getElementById('infoTime').textContent = new Date(row.timestamp * 1000).toLocaleTimeString();
  document.getElementById('infoValue').textContent = fmtValue(row.serialized_value);

  const body = document.getElementById('snapshotVarsBody');
  body.innerHTML = '';
  reconstructStateAt(state.scrubIndex).forEach((v) => {
    const tr = document.createElement('tr');
    tr.innerHTML = '<td><span class="var-dot" style="background:' + colorFor(v.variable_name) + '; color:' + colorFor(v.variable_name) + '"></span>' + v.variable_name + '</td>' +
      '<td class="mono">' + fmtValue(v.serialized_value) + '</td><td>' + v.scope + '</td><td class="mono">L' + v.line_number + '</td>';
    body.appendChild(tr);
  });
}

function renderAll() {
  renderTicks();
  renderTransport();
  renderSnapshotPanels();
}

function stepBy(delta) {
  if (!state.traces.length) return;
  state.scrubIndex = Math.min(Math.max(state.scrubIndex + delta, 0), state.traces.length - 1);
  renderAll();
}

document.getElementById('stepBack').addEventListener('click', () => stepBy(-1));
document.getElementById('stepFwd').addEventListener('click', () => stepBy(1));
document.getElementById('jumpStart').addEventListener('click', () => { state.scrubIndex = 0; renderAll(); });
document.getElementById('jumpEnd').addEventListener('click', () => { state.scrubIndex = state.traces.length - 1; renderAll(); });

document.getElementById('playBtn').addEventListener('click', () => {
  state.playing = !state.playing;
  document.getElementById('playBtn').textContent = state.playing ? '⏸' : '▶';
  if (state.playing) {
    if (state.scrubIndex >= state.traces.length - 1) state.scrubIndex = 0;
    state.playTimer = setInterval(() => {
      if (state.scrubIndex >= state.traces.length - 1) {
        clearInterval(state.playTimer);
        state.playing = false;
        document.getElementById('playBtn').textContent = '▶';
        return;
      }
      state.scrubIndex += 1;
      renderAll();
    }, 450);
  } else {
    clearInterval(state.playTimer);
  }
});

document.addEventListener('keydown', (e) => {
  if (e.target.tagName === 'INPUT') return;
  if (document.getElementById('page-timetravel').classList.contains('active')) {
    if (e.key === 'ArrowRight') { stepBy(1); e.preventDefault(); }
    if (e.key === 'ArrowLeft') { stepBy(-1); e.preventDefault(); }
  }
});

/* ---- Variables table -------------------------------------------------- */
function renderVariablesTable(filter) {
  const body = document.getElementById('variablesTableBody');
  body.innerHTML = '';
  const names = filter
    ? state.variables.filter((n) => n.toLowerCase().includes(filter.toLowerCase()))
    : state.variables;

  document.getElementById('varsEmptyHint').hidden = names.length > 0;

  names.forEach((name) => {
    const rows = state.traces.filter((t) => t.variable_name === name);
    const last = rows[rows.length - 1];
    const tr = document.createElement('tr');
    tr.innerHTML = '<td><span class="var-dot" style="background:' + colorFor(name) + '; color:' + colorFor(name) + '"></span>' + name + '</td>' +
      '<td class="mono">' + (last ? last.value_type : '') + '</td>' +
      '<td class="mono">' + (last ? fmtValue(last.serialized_value) : '') + '</td>' +
      '<td>' + (last ? last.scope : '') + '</td>' +
      '<td class="mono">' + rows.length + '</td>';
    body.appendChild(tr);
  });
}

document.getElementById('varSearch').addEventListener('input', (e) => renderVariablesTable(e.target.value));

/* ---- Snapshots table ---------------------------------------------------- */
function renderSnapshotsTable() {
  const body = document.getElementById('snapshotsTableBody');
  body.innerHTML = '';
  document.getElementById('snapsEmptyHint').hidden = state.traces.length > 0;
  state.traces.forEach((row, i) => {
    const tr = document.createElement('tr');
    tr.innerHTML = '<td class="mono">#' + (i + 1) + '</td><td class="mono">L' + row.line_number + '</td>' +
      '<td><span class="var-dot" style="background:' + colorFor(row.variable_name) + '; color:' + colorFor(row.variable_name) + '"></span>' + row.variable_name + '</td>' +
      '<td class="mono">' + fmtValue(row.serialized_value) + '</td><td>' + row.scope + '</td>' +
      '<td class="mono">' + new Date(row.timestamp * 1000).toLocaleTimeString() + '</td>';
    body.appendChild(tr);
  });
}

/* ---- Settings: parse + session switching ------------------------------- */
document.getElementById('parseForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const file = document.getElementById('parseFile').files[0];
  if (!file) return;
  const statusEl = document.getElementById('parseStatus');
  statusEl.textContent = 'parsing…';
  try {
    const formData = new FormData();
    formData.append('file', file);
    const result = await fetchJSON('/api/parse', {
      method: 'POST',
      body: formData,
    });
    statusEl.textContent = '✓ found ' + result.assignments_found + ' assignments';
    await loadSessions();
    state.session = result.session;
    document.getElementById('sessionSelect').value = result.session;
    await load();
    document.getElementById('parseFile').value = '';
  } catch (err) {
    statusEl.textContent = '✗ ' + err.message;
  }
});

document.getElementById('sessionSelect').addEventListener('change', (e) => {
  state.session = e.target.value;
  load();
});

/* ---- Theme toggle -------------------------------------------------------- */
function applyTheme(theme) {
  document.body.setAttribute('data-theme', theme);
  const isLight = theme === 'light';
  document.getElementById('themeIcon').textContent = isLight ? '☀️' : '🌙';
  document.getElementById('themeLabel').textContent = isLight ? 'Light mode' : 'Dark mode';
  document.getElementById('currentThemeLabel').textContent = isLight ? 'Light' : 'Dark';
  try { localStorage.setItem('pychronicle-theme', theme); } catch (e) {}
}
function toggleTheme() {
  applyTheme(document.body.getAttribute('data-theme') === 'light' ? 'dark' : 'light');
}
document.getElementById('themeBtn').addEventListener('click', toggleTheme);
document.getElementById('settingsThemeBtn').addEventListener('click', toggleTheme);

(function initTheme() {
  let saved = 'dark';
  try { saved = localStorage.getItem('pychronicle-theme') || 'dark'; } catch (e) {}
  applyTheme(saved);
})();

(async function init() {
  await loadSessions();
  await load();
})();
