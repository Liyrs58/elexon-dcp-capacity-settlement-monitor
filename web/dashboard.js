const fmt = new Intl.NumberFormat('en-GB');
const pct = (value) => value === null || value === undefined ? '—' : `${value >= 0 ? '+' : ''}${(value * 100).toFixed(1)}%`;
const esc = (value) => String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));

const STATIC_SITE = window.location.hostname.endsWith('github.io') || window.location.protocol === 'file:' || window.location.port === '4173';
let staticScenarioInputsPromise;

async function getStaticScenario(path) {
  staticScenarioInputsPromise ??= fetch('api/scenario-inputs.json', {cache: 'no-store'}).then(response => response.json());
  const inputs = await staticScenarioInputsPromise;
  const query = new URLSearchParams(path.split('?')[1] || '');
  const throttle = Math.min(1, Math.max(0, Number(query.get('throttle') ?? 0)));
  const reserve = Math.min(0.8, Math.max(0, Number(query.get('reserve') ?? 0)));
  const multiplier = Math.max(0, Number(query.get('multiplier') ?? 1));
  const horizon = Math.max(0, Number(query.get('horizon') ?? 24));
  const arrivals = Math.max(0, inputs.new_pair_arrivals_per_hour) * multiplier + Math.max(0, inputs.historic_arrivals_per_hour) * (1 - throttle);
  const capacity = Math.max(0, inputs.capacity_per_hour) * (1 - reserve);
  const netGrowth = arrivals - capacity;
  return {
    new_pair_arrivals_per_hour: Number(inputs.new_pair_arrivals_per_hour.toFixed(2)),
    historic_arrivals_per_hour: Number(inputs.historic_arrivals_per_hour.toFixed(2)),
    projected_arrivals_per_hour: Number(arrivals.toFixed(2)),
    registration_capacity_after_reserve_per_hour: Number(capacity.toFixed(2)),
    net_queue_growth_per_hour: Number(netGrowth.toFixed(2)),
    current_backlog: Math.round(inputs.current_backlog),
    projected_backlog: Math.round(Math.max(0, inputs.current_backlog + netGrowth * horizon)),
    horizon_hours: Math.round(horizon),
    historic_throttle_fraction: throttle,
    reserved_capacity_fraction: reserve,
    demand_multiplier: multiplier,
  };
}

async function getJson(path) {
  if (STATIC_SITE) {
    if (path.startsWith('/api/scenario')) return getStaticScenario(path);
    const query = new URLSearchParams(path.split('?')[1] || '');
    const basePath = path.split('?')[0].replace(/^\//, '');
    const suffix = basePath === 'api/contributors' && query.get('hours') === '336' ? '-336' : '';
    const staticPath = `${basePath}${suffix}.json`;
    const response = await fetch(staticPath, {cache: 'no-store'});
    if (!response.ok) throw new Error(`Static request failed: ${staticPath}`);
    return response.json();
  }
  const response = await fetch(path, {cache: 'no-store'});
  if (!response.ok) throw new Error(`Request failed: ${path}`);
  return response.json();
}

function setState(state) {
  const badge = document.getElementById('stateBadge');
  badge.textContent = state;
  badge.className = `state-badge state-${state.toLowerCase().replaceAll(' ', '-')}`;
}

function demoTime(value) {
  const d = new Date(value);
  const start = new Date('2026-01-01T00:00');
  const day = Math.floor((d - start) / 86400000) + 1;
  return `D${String(day).padStart(2, '0')} · ${String(d.getHours()).padStart(2, '0')}:00`;
}

function drawLine(targetId, rows, specs, accessibleTitle) {
  const target = document.getElementById(targetId);
  if (!rows.length) { target.innerHTML = '<div class="chart-empty">No demo rows for this window.</div>'; return; }
  const W = 800, H = 210, L = 43, R = 10, T = 10, B = 30;
  const iw = W - L - R, ih = H - T - B;
  const all = rows.flatMap(row => specs.map(s => Number(row[s.key] || 0)));
  let max = Math.max(1, ...all);
  max = Math.ceil(max / (max > 100 ? 100 : max > 25 ? 25 : 5)) * (max > 100 ? 100 : max > 25 ? 25 : 5);
  const x = i => L + (rows.length === 1 ? iw / 2 : i * iw / (rows.length - 1));
  const y = v => T + ih - (Number(v || 0) / max) * ih;
  const pathFor = key => rows.map((row, i) => `${i ? 'L' : 'M'}${x(i).toFixed(1)},${y(row[key]).toFixed(1)}`).join(' ');
  const grid = Array.from({length: 5}, (_, i) => {
    const value = max * i / 4, yy = y(value);
    const axis = specs[0].unit === '%' ? `${value.toFixed(1)}%` : fmt.format(Math.round(value));
    return `<line class="chart-gridline" x1="${L}" y1="${yy}" x2="${W-R}" y2="${yy}"/><text class="chart-axis" x="${L-7}" y="${yy+3}" text-anchor="end">${axis}</text>`;
  }).join('');
  const tickCount = Math.min(6, rows.length);
  const ticks = Array.from({length: tickCount}, (_, i) => {
    const index = Math.round(i * (rows.length - 1) / Math.max(1, tickCount - 1));
    return `<text class="chart-axis" x="${x(index)}" y="${H-8}" text-anchor="middle">${demoTime(rows[index].timestamp)}</text>`;
  }).join('');
  const lines = specs.map(s => `<path d="${pathFor(s.key)}" class="${s.className}" aria-label="${esc(s.label)}"/>`).join('');
  const lastDots = specs.map(s => `<circle class="chart-dot" cx="${x(rows.length-1)}" cy="${y(rows.at(-1)[s.key])}" r="3.5" stroke="${s.color}"/>`).join('');
  target.innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(accessibleTitle)}">${grid}${lines}${lastDots}${ticks}</svg>`;
}

function drawDualTrend(targetId, rows) {
  const target = document.getElementById(targetId);
  target.innerHTML = '<div class="mini-trend"><div class="mini-title"><span>Backlog</span><small>items</small></div><div id="backlogTrend" class="chart"></div></div><div class="mini-trend"><div class="mini-title"><span>Processing latency</span><small>minutes</small></div><div id="latencyTrend" class="chart"></div></div>';
  drawLine('backlogTrend', rows, [{key:'backlog',label:'Backlog',color:'#df9a54',className:'chart-line-backlog'}], 'Synthetic backlog trend');
  drawLine('latencyTrend', rows, [{key:'latency',label:'Latency',color:'#138b92',className:'chart-line-arrivals'}], 'Synthetic processing latency trend');
}

function drawVarianceBars(rows) {
  const target = document.getElementById('varianceChart');
  const ordered = [...rows].sort((a,b) => (b.actual-b.forecast) - (a.actual-a.forecast)).slice(0, 8);
  const max = Math.max(1, ...ordered.map(r => Math.max(0, r.actual-r.forecast)));
  target.innerHTML = ordered.map(row => {
    const amount = row.actual-row.forecast;
    const label = `${row.participant_id} · ${row.submission_type}`;
    return `<div class="bar-row"><span class="bar-label" title="${esc(label)}">${esc(label)}</span><div class="bar-track"><div class="bar-fill" style="width:${Math.max(2, amount/max*100)}%"></div></div><span class="bar-value">+${fmt.format(amount)}</span></div>`;
  }).join('') || '<div class="chart-empty">No positive deviations in this sample.</div>';
}

function renderOverview(data) {
  setState(data.state);
  document.getElementById('backlogValue').textContent = fmt.format(data.backlog);
  const delta = data.backlog_change_24h;
  document.getElementById('backlogDelta').textContent = `${delta >= 0 ? '+' : ''}${fmt.format(delta)}`;
  document.getElementById('throughputValue').textContent = fmt.format(data.processed);
  document.getElementById('varianceValue').textContent = pct(data.forecast_variance_24h);
  document.getElementById('runsValue').textContent = `${data.delayed_runs_24h} / ${data.total_runs_24h}`;
  document.getElementById('runSummary').textContent = `${data.delayed_runs_24h} delayed · synthetic`;
}

function renderRuns(rows) {
  const body = document.getElementById('runsTable');
  const recent = rows.slice(-8).reverse();
  body.innerHTML = recent.map(row => `<tr><td>${demoTime(row.timestamp)}</td><td>${esc(row.service_run_type)}</td><td>${fmt.format(row.delay_minutes)} min</td><td><span class="run-status ${row.status === 'Delayed' ? 'run-delayed' : 'run-on-time'}">${esc(row.status)}</span></td></tr>`).join('') || '<tr><td class="empty-row" colspan="4">No scheduled demo runs.</td></tr>';
}

function renderDrivers(rows) {
  const body = document.getElementById('driversTable');
  body.innerHTML = rows.map(row => {
    const variance = row.variance === null ? 'n/a' : pct(row.variance);
    return `<tr><td>${esc(row.participant_id)}</td><td>${esc(row.participant_type)}</td><td>${esc(row.submission_type)}</td><td>${fmt.format(row.actual)}</td><td>${fmt.format(row.forecast)}</td><td class="${row.variance >= 0 ? 'driver-variance' : 'negative'}">${variance}</td><td>${fmt.format(row.peak_segment_backlog)}</td><td>${fmt.format(row.retries)}</td></tr>`;
  }).join('') || '<tr><td class="empty-row" colspan="8">No generated segments.</td></tr>';
}

async function refreshDrivers() {
  const hours = document.getElementById('driverWindow').value;
  const [contributors, accuracy] = await Promise.all([getJson(`/api/contributors?hours=${hours}`), getJson('/api/forecast')]);
  renderDrivers(contributors);
  drawVarianceBars(accuracy.filter(r => r.actual > r.forecast));
}

async function refreshScenario() {
  const multiplier = Number(document.getElementById('demandSlider').value) / 100;
  const throttle = Number(document.getElementById('throttleSlider').value) / 100;
  const reserve = Number(document.getElementById('reserveSlider').value) / 100;
  const horizon = Number(document.getElementById('horizonSelect').value);
  document.getElementById('demandLabel').textContent = `+${Math.round((multiplier-1)*100)}%`;
  document.getElementById('throttleLabel').textContent = `${Math.round(throttle*100)}%`;
  document.getElementById('reserveLabel').textContent = `${Math.round(reserve*100)}%`;
  const d = await getJson(`/api/scenario?multiplier=${multiplier}&throttle=${throttle}&reserve=${reserve}&horizon=${horizon}`);
  const change = d.projected_backlog-d.current_backlog;
  document.getElementById('scenarioStart').textContent = fmt.format(d.current_backlog);
  document.getElementById('scenarioEnd').textContent = fmt.format(d.projected_backlog);
  document.getElementById('scenarioChange').textContent = `${change >= 0 ? '+' : ''}${fmt.format(change)} over ${horizon}h`;
  document.getElementById('scenarioGrowth').textContent = `${d.net_queue_growth_per_hour >= 0 ? '+' : ''}${d.net_queue_growth_per_hour.toFixed(1)}`;
  const time = d.net_queue_growth_per_hour > 0 && d.current_backlog < 900 ? (900-d.current_backlog)/d.net_queue_growth_per_hour : null;
  document.getElementById('scenarioTime').textContent = time === null ? 'Not valid' : `${time.toFixed(1)}h`;
  const target = document.getElementById('scenarioChart');
  const max = Math.max(900, d.current_backlog, d.projected_backlog);
  const endPct = Math.min(100, d.projected_backlog/max*100);
  target.innerHTML = `<div class="projection"><div class="projection-head"><span>Current queue</span><strong>${fmt.format(d.current_backlog)}</strong></div><div class="projection-track"><i style="width:${Math.min(100,d.current_backlog/max*100)}%"></i></div><div class="projection-head"><span>Projected after ${horizon} hours</span><strong>${fmt.format(d.projected_backlog)}</strong></div><div class="projection-track projection-end"><i style="width:${endPct}%"></i></div><div class="projection-threshold"><span>Demo alert reference</span><strong>900</strong></div><p>Projected arrivals: ${d.projected_arrivals_per_hour.toFixed(1)}/hour · registration capacity after reserve: ${d.registration_capacity_after_reserve_per_hour.toFixed(1)}/hour</p></div>`;
}

async function refreshNote() {
  const note = await getJson('/api/incident-note');
  document.getElementById('incidentNote').textContent = note.note;
}

function renderHypotheses(rows) {
  const target = document.getElementById('hypothesisList');
  target.innerHTML = rows.map(row => `<article class="panel evidence-card"><div class="evidence-kicker"><span>${esc(row.code)}</span>${esc(row.confidence)} CONFIDENCE</div><h3>${esc(row.question)}</h3><p><strong>Why it matters:</strong> ${esc(row.why_it_matters)}</p><p><strong>Method:</strong> ${esc(row.method)}</p><p><strong>Result:</strong> ${esc(row.result)}</p><p><strong>Conclusion:</strong> ${esc(row.conclusion)}</p><p><strong>Limit:</strong> ${esc(row.limitation)}</p><p><strong>Next check:</strong> ${esc(row.next_check)}</p></article>`).join('');
}

function renderImpact(data) {
  const target = document.getElementById('impactPanel');
  const fields = [
    ['Current demo state', data.state], ['Who may be affected', data.who_may_be_affected],
    ['Settlement impact', data.potential_settlement_impact], ['Payment impact', data.potential_payment_impact],
    ['Customer action', data.customer_action], ['What remains uncertain', data.uncertainty],
    ['Next owner', data.next_owner], ['Next update', data.next_update],
  ];
  target.innerHTML = fields.map(([label, value]) => `<article class="panel"><div class="eyebrow">${esc(label)}</div><p>${esc(value)}</p></article>`).join('');
}

function renderImprovements(rows) {
  document.getElementById('improvementTable').innerHTML = rows.map(row => `<tr><td>${esc(row.problem)}</td><td>${esc(row.action)}</td><td>${esc(row.benefit)}</td><td>${esc(row.risk)}</td><td>${esc(row.measure)}</td><td><span class="run-status run-on-time">${esc(row.status)}</span></td></tr>`).join('');
}

async function refreshOperationalViews(view) {
  if (view === 'hypotheses') renderHypotheses(await getJson('/api/hypotheses'));
  if (view === 'impact') renderImpact(await getJson('/api/customer-impact'));
  if (view === 'improvements') renderImprovements(await getJson('/api/improvements'));
}

function showView(view) {
  document.querySelectorAll('.view').forEach(node => node.classList.toggle('active', node.id === `view-${view}`));
  document.querySelectorAll('.nav-item').forEach(node => node.classList.toggle('active', node.dataset.view === view));
  if (view === 'drivers') refreshDrivers();
  if (view === 'scenario') refreshScenario();
  if (view === 'note') refreshNote();
  if (['hypotheses','impact','improvements'].includes(view)) refreshOperationalViews(view);
  window.scrollTo({top:0,behavior:'smooth'});
}

async function loadDashboard() {
  try {
    const [overview, series, runs, validation] = await Promise.all([getJson('/api/overview'), getJson('/api/timeseries?hours=168'), getJson('/api/runs?hours=168'), getJson('/api/validation')]);
    renderOverview(overview);
    drawLine('flowChart', series, [
      {key:'received',label:'Arrivals',color:'#138b92',className:'chart-line-arrivals'},
      {key:'processed',label:'Processed',color:'#8abeb7',className:'chart-line-processed'},
    ], 'Synthetic registrations received and processed by hour');
    drawDualTrend('queueChart', series);
    drawLine('qualityChart', series, [
      {key:'failure_rate_pct',label:'Validation failures',color:'#138b92',className:'chart-line-arrivals',unit:'%'},
      {key:'retry_rate_pct',label:'Retries',color:'#df9a54',className:'chart-line-backlog',unit:'%'},
    ], 'Synthetic validation failure and retry rates by hour');
    renderRuns(runs);
    document.getElementById('validationSummary').textContent = `${validation.status}. ${validation.row_count} interval rows passed ${validation.checks.length} named controls before analysis. Errors: ${validation.error_count || 0}. Warnings: ${validation.warning_count || 0}.`;
    document.getElementById('validationChecks').innerHTML = validation.checks.map(check => `<span class="tag">${esc(check)}</span>`).join('');
  } catch (error) {
    console.error(error);
    document.querySelector('.content-wrap').insertAdjacentHTML('afterbegin','<div class="error-box">The local demo could not load its generated data. Restart it from the project folder.</div>');
  }
}

document.querySelectorAll('.nav-item').forEach(button => button.addEventListener('click', () => showView(button.dataset.view)));
document.querySelectorAll('[data-go]').forEach(button => button.addEventListener('click', () => showView(button.dataset.go)));
document.getElementById('driverWindow').addEventListener('change', refreshDrivers);
['demandSlider','throttleSlider','reserveSlider','horizonSelect'].forEach(id => document.getElementById(id).addEventListener('input', refreshScenario));
document.getElementById('copyNote').addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(document.getElementById('incidentNote').textContent);
    document.getElementById('copyNote').textContent = 'Copied';
    setTimeout(() => document.getElementById('copyNote').textContent = 'Copy note', 1400);
  } catch { document.getElementById('copyNote').textContent = 'Select text to copy'; }
});
loadDashboard();
