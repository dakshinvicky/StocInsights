// STOCKINS8 PRO TERMINAL - Client Logic

let globalFiiDiiData = { daily: [], stocks: [] };
let globalDividendsData = [];
let currentStockFilter = 'all';
let stockSortCol = 'Stock';
let stockSortAsc = true;
let divSortCol = 'stock';
let divSortAsc = true;

// On-Demand Purge & Reload Data (Authentic Server Timestamp Check)
async function purgeAndReloadData() {
  const syncBtn = document.querySelector('.header-actions .btn-cyan');
  if (syncBtn) {
    syncBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> SYNCING LIVE DATA...`;
    syncBtn.disabled = true;
  }

  // Clear in-memory datasets
  globalFiiDiiData = { daily: [], stocks: [] };
  globalDividendsData = [];

  // Clear local storage caches
  localStorage.removeItem('stockins8_cache_fii');
  localStorage.removeItem('stockins8_cache_div');

  // Show loading indicators
  document.getElementById('daily-table-body').innerHTML = `<tr><td colspan="5" class="loading-state"><i class="fa-solid fa-sync fa-spin text-cyan"></i> Purging cache & fetching latest server dataset...</td></tr>`;
  document.getElementById('stocks-table-body').innerHTML = `<tr><td colspan="8" class="loading-state"><i class="fa-solid fa-sync fa-spin text-emerald"></i> Refreshing stock shareholdings...</td></tr>`;
  document.getElementById('dividends-table-body').innerHTML = `<tr><td colspan="5" class="loading-state"><i class="fa-solid fa-sync fa-spin text-amber"></i> Fetching corporate dividend schedules...</td></tr>`;

  // Fetch latest JSON with cache-busting parameter
  await loadData();

  if (syncBtn) {
    syncBtn.innerHTML = `<i class="fa-solid fa-check text-emerald"></i> SYNCED!`;
    setTimeout(() => {
      syncBtn.innerHTML = `<i class="fa-solid fa-bolt"></i> LIVE SYNC & RELOAD`;
      syncBtn.disabled = false;
    }, 2000);
  }
}

// Theme Switcher
function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);

  const icon = document.getElementById('theme-icon');
  if (icon) {
    icon.className = newTheme === 'dark' ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
  }
}

// Initialization (Direct Load)
document.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  const icon = document.getElementById('theme-icon');
  if (icon) {
    icon.className = savedTheme === 'dark' ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
  }

  loadData();
});

function switchTab(tabName) {
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));

  if (tabName === 'fii') {
    document.getElementById('tab-fii-btn').classList.add('active');
    document.getElementById('tab-fii').classList.add('active');
  } else if (tabName === 'dividends') {
    document.getElementById('tab-div-btn').classList.add('active');
    document.getElementById('tab-dividends').classList.add('active');
  }
}

function setCapitalPreset(amount) {
  document.querySelectorAll('.btn-preset').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');
  document.getElementById('div-investment-input').value = amount;
  renderDividendsTable();
}

function formatNumber(val, decimals = 2) {
  if (val === null || val === undefined || isNaN(val)) return 'N/A';
  return parseFloat(val).toLocaleString('en-IN', { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
}

// Load static JSON datasets
async function loadData() {
  const timestamp = Date.now();
  try {
    const fiiRes = await fetch(`data/fii_dii.json?sync=true&t=${timestamp}`);
    if (fiiRes.ok) {
      globalFiiDiiData = await fiiRes.json();
      if (globalFiiDiiData.updated_at) {
        document.getElementById('last-updated').innerText = `Synced: ${globalFiiDiiData.updated_at}`;
      }
      renderFiiDiiSection();
    }
  } catch (err) {
    console.warn('Could not load fii_dii.json:', err);
    document.getElementById('daily-table-body').innerHTML = `<tr><td colspan="5" class="loading-state">No static data found. Run <code>python main.py generate</code> or click Live Sync.</td></tr>`;
  }

  try {
    const divRes = await fetch(`data/dividends.json?sync=true&t=${timestamp}`);
    if (divRes.ok) {
      const divJson = await divRes.json();
      globalDividendsData = divJson.dividends || [];
      renderDividendsTable();
    }
  } catch (err) {
    console.warn('Could not load dividends.json:', err);
    document.getElementById('dividends-table-body').innerHTML = `<tr><td colspan="5" class="loading-state">No static dividend data found. Run <code>python main.py generate</code> or click Live Sync.</td></tr>`;
  }
}

function renderFiiDiiSection() {
  const daily = globalFiiDiiData.daily || [];

  let fiiNet = 0, diiNet = 0;
  daily.forEach(item => {
    const cat = (item.Category || '').toUpperCase();
    const netValStr = String(item['Net Value (Rs Cr)'] || '').replace(/,/g, '').replace(/\+/g, '');
    const val = parseFloat(netValStr) || 0;
    if (cat.includes('FII') || cat.includes('FPI')) fiiNet = val;
    if (cat.includes('DII')) diiNet = val;
  });

  document.getElementById('ticker-fii').innerHTML = `<span class="${fiiNet >= 0 ? 'text-emerald' : 'text-rose'}">₹ ${formatNumber(fiiNet)} Cr</span>`;
  document.getElementById('ticker-dii').innerHTML = `<span class="${diiNet >= 0 ? 'text-emerald' : 'text-rose'}">₹ ${formatNumber(diiNet)} Cr</span>`;

  const fiiElem = document.getElementById('fii-net-val');
  fiiElem.innerText = `₹ ${formatNumber(fiiNet)} Cr`;
  fiiElem.className = `metric-amount ${fiiNet >= 0 ? 'text-emerald' : 'text-rose'}`;
  document.getElementById('fii-sentiment').innerText = fiiNet >= 0 ? '🟢 Net Buyers' : '🔴 Net Sellers';

  const diiElem = document.getElementById('dii-net-val');
  diiElem.innerText = `₹ ${formatNumber(diiNet)} Cr`;
  diiElem.className = `metric-amount ${diiNet >= 0 ? 'text-emerald' : 'text-rose'}`;
  document.getElementById('dii-sentiment').innerText = diiNet >= 0 ? '🟢 Net Buyers' : '🔴 Net Sellers';

  const totalFlow = fiiNet + diiNet;
  const totalElem = document.getElementById('total-flow-val');
  totalElem.innerText = `₹ ${formatNumber(totalFlow)} Cr`;
  totalElem.className = `metric-amount ${totalFlow >= 0 ? 'text-emerald' : 'text-rose'}`;

  const sentBadge = document.getElementById('market-sentiment-badge');
  if (totalFlow > 1000) {
    sentBadge.innerText = '🔥 Strongly Bullish';
    sentBadge.className = 'sentiment-badge badge-emerald';
  } else if (totalFlow >= 0) {
    sentBadge.innerText = '🟢 Mildly Bullish';
    sentBadge.className = 'sentiment-badge badge-emerald';
  } else {
    sentBadge.innerText = '🔴 Bearish Flow';
    sentBadge.className = 'sentiment-badge badge-rose';
  }

  const dailyBody = document.getElementById('daily-table-body');
  if (daily.length > 0) {
    dailyBody.innerHTML = daily.map(row => {
      const netStr = row['Net Value (Rs Cr)'] || '0.00';
      const isPos = !netStr.includes('-');
      return `
        <tr>
          <td><strong style="color: var(--accent-cyan);">${row.Category || ''}</strong></td>
          <td class="font-mono">${row.Date || ''}</td>
          <td class="font-mono">₹ ${row['Buy Value (Rs Cr)'] || '0.00'}</td>
          <td class="font-mono">₹ ${row['Sell Value (Rs Cr)'] || '0.00'}</td>
          <td><span class="${isPos ? 'badge-emerald' : 'badge-rose'}">₹ ${netStr}</span></td>
        </tr>
      `;
    }).join('');
  } else {
    dailyBody.innerHTML = `<tr><td colspan="5" class="loading-state">No daily activity records found.</td></tr>`;
  }

  renderStockTable();
}

function setStockFilter(filterType) {
  currentStockFilter = filterType;
  document.querySelectorAll('.pill-group .pill-btn').forEach(btn => btn.classList.remove('active'));

  if (filterType === 'all') document.getElementById('filter-all-btn').classList.add('active');
  if (filterType === 'fii-buy') document.getElementById('filter-fii-buy-btn').classList.add('active');
  if (filterType === 'fii-sell') document.getElementById('filter-fii-sell-btn').classList.add('active');
  if (filterType === 'dii-buy') document.getElementById('filter-dii-buy-btn').classList.add('active');

  renderStockTable();
}

function filterStockTable() {
  renderStockTable();
}

function sortStockTable(colName) {
  if (stockSortCol === colName) {
    stockSortAsc = !stockSortAsc;
  } else {
    stockSortCol = colName;
    stockSortAsc = true;
  }
  renderStockTable();
}

function renderStockTable() {
  const stocks = globalFiiDiiData.stocks || [];
  const searchInput = (document.getElementById('stock-search-input').value || '').trim().toUpperCase();

  let filtered = stocks.filter(stock => {
    const sym = (stock.Stock || '').toUpperCase();
    const fiiChange = parseFloat(stock['FII QoQ Change (%)']) || 0;
    const diiChange = parseFloat(stock['DII QoQ Change (%)']) || 0;

    const matchesSearch = !searchInput || sym.includes(searchInput);
    let matchesPill = true;

    if (currentStockFilter === 'fii-buy') matchesPill = fiiChange > 0;
    if (currentStockFilter === 'fii-sell') matchesPill = fiiChange < 0;
    if (currentStockFilter === 'dii-buy') matchesPill = diiChange > 0;

    return matchesSearch && matchesPill;
  });

  filtered.sort((a, b) => {
    let valA = a[stockSortCol];
    let valB = b[stockSortCol];
    if (valA === null || valA === undefined) valA = -9999;
    if (valB === null || valB === undefined) valB = -9999;
    if (typeof valA === 'string') return stockSortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
    return stockSortAsc ? valA - valB : valB - valA;
  });

  const tbody = document.getElementById('stocks-table-body');
  if (filtered.length > 0) {
    tbody.innerHTML = filtered.map(row => {
      const fiiChange = row['FII QoQ Change (%)'];
      const diiChange = row['DII QoQ Change (%)'];

      const fiiBadge = fiiChange > 0 ? `<span class="badge-emerald">+${fiiChange}%</span>` : (fiiChange < 0 ? `<span class="badge-rose">${fiiChange}%</span>` : `<span class="badge-neutral">${fiiChange}%</span>`);
      const diiBadge = diiChange > 0 ? `<span class="badge-emerald">+${diiChange}%</span>` : (diiChange < 0 ? `<span class="badge-rose">${diiChange}%</span>` : `<span class="badge-neutral">${diiChange}%</span>`);

      return `
        <tr>
          <td><strong style="font-size: 0.95rem;">${row.Stock || ''}</strong></td>
          <td class="font-mono">${row.CMP ? '₹ ' + formatNumber(row.CMP) : 'N/A'}</td>
          <td>${row['Latest Quarter'] || 'N/A'}</td>
          <td>${row['Prev Quarter'] || 'N/A'}</td>
          <td class="font-mono">${formatNumber(row['FII (%)'])}%</td>
          <td>${fiiBadge}</td>
          <td class="font-mono">${formatNumber(row['DII (%)'])}%</td>
          <td>${diiBadge}</td>
        </tr>
      `;
    }).join('');
  } else {
    tbody.innerHTML = `<tr><td colspan="8" class="loading-state">No matching stock shareholding records found.</td></tr>`;
  }
}

function sortDividendsTable(colName) {
  if (divSortCol === colName) {
    divSortAsc = !divSortAsc;
  } else {
    divSortCol = colName;
    divSortAsc = true;
  }
  renderDividendsTable();
}

function renderDividendsTable() {
  const searchInput = (document.getElementById('div-search-input').value || '').trim().toUpperCase();
  const investAmt = parseFloat(document.getElementById('div-investment-input').value) || 100000;

  let processed = globalDividendsData.map(item => {
    const cmp = parseFloat(item.CMP);
    const divPerShare = parseFloat(item['Divident per share']);
    let calculated = 0;
    if (cmp > 0 && divPerShare > 0) {
      calculated = (investAmt / cmp) * divPerShare;
    }
    return {
      ...item,
      calculated_div: Math.round(calculated * 100) / 100
    };
  });

  let filtered = processed.filter(item => {
    const sym = (item.stock || '').toUpperCase();
    return !searchInput || sym.includes(searchInput);
  });

  document.getElementById('ticker-div').innerText = `${filtered.length} Announced Actions`;
  document.getElementById('div-count-badge').innerText = filtered.length;
  document.getElementById('div-count-val').innerText = filtered.length;

  const maxDiv = filtered.reduce((max, item) => Math.max(max, item['Divident per share'] || 0), 0);
  document.getElementById('div-max-val').innerText = `₹ ${formatNumber(maxDiv)}`;

  const maxEarnings = filtered.reduce((max, item) => Math.max(max, item.calculated_div || 0), 0);
  document.getElementById('div-top-calc-val').innerText = `₹ ${formatNumber(maxEarnings)}`;
  document.getElementById('div-top-calc-sub').innerText = `Based on ₹${investAmt.toLocaleString('en-IN')} capital`;

  filtered.sort((a, b) => {
    let valA = a[divSortCol];
    let valB = b[divSortCol];
    if (valA === null || valA === undefined) valA = -9999;
    if (valB === null || valB === undefined) valB = -9999;
    if (typeof valA === 'string') return divSortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
    return divSortAsc ? valA - valB : valB - valA;
  });

  const tbody = document.getElementById('dividends-table-body');
  if (filtered.length > 0) {
    tbody.innerHTML = filtered.map(row => {
      return `
        <tr>
          <td><strong style="font-size: 0.95rem; color: var(--accent-amber);">${row.stock || ''}</strong></td>
          <td class="font-mono">${row['dividentex date'] || 'N/A'}</td>
          <td class="font-mono">${row.CMP ? '₹ ' + formatNumber(row.CMP) : 'N/A'}</td>
          <td class="font-mono">${row['Divident per share'] ? '₹ ' + formatNumber(row['Divident per share']) : 'N/A'}</td>
          <td><strong class="font-mono text-emerald" style="font-size: 1rem;">₹ ${formatNumber(row.calculated_div)}</strong></td>
        </tr>
      `;
    }).join('');
  } else {
    tbody.innerHTML = `<tr><td colspan="5" class="loading-state">No upcoming dividends found.</td></tr>`;
  }
}

function exportTableToCSV(tableId, filename) {
  const table = document.getElementById(tableId);
  const rows = Array.from(table.querySelectorAll('tr'));

  const csvContent = rows.map(row => {
    const cols = Array.from(row.querySelectorAll('th, td'));
    return cols.map(col => `"${col.innerText.replace(/"/g, '""').trim()}"`).join(',');
  }).join('\n');

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
