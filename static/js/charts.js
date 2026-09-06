/**
 * ORCA - Ocean Risk & Condition Analyzer
 * Chart.js and Custom Gauges Controller
 * Includes 7-Day SST, Wind, Wave, and Chlorophyll Trend Charts
 */

/* --------------------------------------------------------------------------
   1. Home Page Mini Charts (Wave & Wind 24h Trends)
   -------------------------------------------------------------------------- */
function initHomeMiniCharts(trendData) {
  if (!trendData || !trendData.labels) return;

  // Wave Chart
  const waveCanvas = document.getElementById('miniWaveChart');
  if (waveCanvas) {
    const ctxWave = waveCanvas.getContext('2d');
    const waveGradient = ctxWave.createLinearGradient(0, 0, 0, 160);
    waveGradient.addColorStop(0, 'rgba(0, 210, 211, 0.45)');
    waveGradient.addColorStop(1, 'rgba(0, 210, 211, 0.0)');

    new Chart(ctxWave, {
      type: 'line',
      data: {
        labels: trendData.labels,
        datasets: [{
          label: 'Wave Height (m)',
          data: trendData.waves,
          borderColor: '#00d2d3',
          borderWidth: 2.5,
          backgroundColor: waveGradient,
          fill: true,
          tension: 0.35,
          pointRadius: 0,
          pointHoverRadius: 5,
          pointHoverBackgroundColor: '#00f2fe',
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(10, 25, 47, 0.95)',
            titleColor: '#00d2d3',
            bodyColor: '#fff',
            borderColor: 'rgba(0, 210, 211, 0.3)',
            borderWidth: 1,
            displayColors: false,
            callbacks: {
              label: (ctx) => `Wave: ${ctx.parsed.y} meters`
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: {
              color: '#8ba3c7',
              font: { size: 10 },
              maxTicksLimit: 6
            }
          },
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: {
              color: '#8ba3c7',
              font: { size: 10 },
              callback: (val) => val + 'm'
            }
          }
        }
      }
    });
  }

  // Wind Chart
  const windCanvas = document.getElementById('miniWindChart');
  if (windCanvas) {
    const ctxWind = windCanvas.getContext('2d');
    const windGradient = ctxWind.createLinearGradient(0, 0, 0, 160);
    windGradient.addColorStop(0, 'rgba(10, 189, 227, 0.45)');
    windGradient.addColorStop(1, 'rgba(10, 189, 227, 0.0)');

    new Chart(ctxWind, {
      type: 'line',
      data: {
        labels: trendData.labels,
        datasets: [{
          label: 'Wind Speed (knots)',
          data: trendData.winds,
          borderColor: '#0abde3',
          borderWidth: 2.5,
          backgroundColor: windGradient,
          fill: true,
          tension: 0.35,
          pointRadius: 0,
          pointHoverRadius: 5,
          pointHoverBackgroundColor: '#48dbfb',
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(10, 25, 47, 0.95)',
            titleColor: '#0abde3',
            bodyColor: '#fff',
            borderColor: 'rgba(10, 189, 227, 0.3)',
            borderWidth: 1,
            displayColors: false,
            callbacks: {
              label: (ctx) => `Wind: ${ctx.parsed.y} knots`
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: {
              color: '#8ba3c7',
              font: { size: 10 },
              maxTicksLimit: 6
            }
          },
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: {
              color: '#8ba3c7',
              font: { size: 10 },
              callback: (val) => val + 'kt'
            }
          }
        }
      }
    });
  }
}

/* --------------------------------------------------------------------------
   2. Risk Score Gauge (Canvas/SVG Semi-circle Arc)
   -------------------------------------------------------------------------- */
function drawRiskGauge(score) {
  const canvas = document.getElementById('riskGaugeCanvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;
  const centerX = width / 2;
  const centerY = height - 20;
  const radius = width / 2 - 25;

  ctx.clearRect(0, 0, width, height);

  // Background arc
  ctx.beginPath();
  ctx.arc(centerX, centerY, radius, Math.PI, 2 * Math.PI, false);
  ctx.lineWidth = 18;
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
  ctx.lineCap = 'round';
  ctx.stroke();

  // Progress arc
  const scoreRatio = Math.min(Math.max(score, 0), 100) / 100;
  const endAngle = Math.PI + (scoreRatio * Math.PI);

  let arcColor = '#1dd1a1'; // Green Safe
  if (score > 40 && score <= 70) {
    arcColor = '#feca57'; // Yellow Moderate
  } else if (score > 70) {
    arcColor = '#ff6b6b'; // Red Danger
  }

  ctx.beginPath();
  ctx.arc(centerX, centerY, radius, Math.PI, endAngle, false);
  ctx.lineWidth = 18;
  ctx.strokeStyle = arcColor;
  ctx.lineCap = 'round';
  ctx.stroke();

  // Needle point
  const needleAngle = endAngle;
  const needleX = centerX + (radius) * Math.cos(needleAngle);
  const needleY = centerY + (radius) * Math.sin(needleAngle);

  ctx.beginPath();
  ctx.arc(needleX, needleY, 8, 0, 2 * Math.PI);
  ctx.fillStyle = '#ffffff';
  ctx.shadowColor = arcColor;
  ctx.shadowBlur = 12;
  ctx.fill();
  ctx.shadowBlur = 0;
}

/* --------------------------------------------------------------------------
   3. Analytics Page Comprehensive Charts (SST, Wind, Wave, Chlorophyll)
   -------------------------------------------------------------------------- */
function initAnalyticsCharts(data) {
  if (!data) return;

  // 1. Wave Height Trend Chart
  const waveAnalyticsCanvas = document.getElementById('analyticsWaveChart');
  if (waveAnalyticsCanvas) {
    new Chart(waveAnalyticsCanvas.getContext('2d'), {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: [
          {
            label: 'Peak Wave Height (m)',
            data: data.wave_heights_max,
            borderColor: '#ff9f43',
            backgroundColor: 'rgba(255, 159, 67, 0.1)',
            borderDash: [5, 5],
            tension: 0.3,
            fill: false,
          },
          {
            label: 'Average Wave Height (m)',
            data: data.wave_heights_avg,
            borderColor: '#00d2d3',
            backgroundColor: 'rgba(0, 210, 211, 0.25)',
            tension: 0.3,
            fill: true,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#e2f1ff', font: { size: 12 } } },
          tooltip: {
            backgroundColor: '#0a192f',
            borderColor: 'rgba(0, 210, 211, 0.4)',
            borderWidth: 1
          }
        },
        scales: {
          x: { ticks: { color: '#8ba3c7' }, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
          y: {
            ticks: { color: '#8ba3c7', callback: (v) => v + ' m' },
            grid: { color: 'rgba(255, 255, 255, 0.05)' }
          }
        }
      }
    });
  }

  // 2. Sea Surface Temperature & Anomaly Chart
  const sstCanvas = document.getElementById('analyticsSstChart');
  if (sstCanvas) {
    new Chart(sstCanvas.getContext('2d'), {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: [
          {
            label: 'Observed SST (°C)',
            data: data.sst_trends,
            borderColor: '#ff6b6b',
            backgroundColor: 'rgba(255, 107, 107, 0.2)',
            fill: true,
            tension: 0.3
          },
          {
            label: 'Climatological Baseline (°C)',
            data: data.sst_baseline,
            borderColor: '#0abde3',
            borderDash: [4, 4],
            fill: false
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#e2f1ff' } }
        },
        scales: {
          x: { ticks: { color: '#8ba3c7' }, grid: { display: false } },
          y: {
            min: 27,
            max: 32,
            ticks: { color: '#8ba3c7', callback: (v) => v + ' °C' },
            grid: { color: 'rgba(255, 255, 255, 0.05)' }
          }
        }
      }
    });
  }

  // 3. 7-Day Surface Wind Speed & Gusts Chart
  const windAnalyticsCanvas = document.getElementById('analyticsWindChart');
  if (windAnalyticsCanvas) {
    new Chart(windAnalyticsCanvas.getContext('2d'), {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: [{
          label: 'Wind Speed (knots)',
          data: data.wind_speeds_avg,
          borderColor: '#0abde3',
          backgroundColor: 'rgba(10, 189, 227, 0.25)',
          fill: true,
          tension: 0.3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#e2f1ff' } }
        },
        scales: {
          x: { ticks: { color: '#8ba3c7' }, grid: { display: false } },
          y: {
            ticks: { color: '#8ba3c7', callback: (v) => v + ' kt' },
            grid: { color: 'rgba(255, 255, 255, 0.05)' }
          }
        }
      }
    });
  }

  // 4. 7-Day Chlorophyll-a Concentration Trend Chart
  const chlaCanvas = document.getElementById('analyticsChlorophyllChart');
  if (chlaCanvas && data.chlorophyll_trends) {
    new Chart(chlaCanvas.getContext('2d'), {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: [
          {
            label: 'Satellite Chlorophyll-a (mg/m³)',
            data: data.chlorophyll_trends,
            borderColor: '#10ac84',
            backgroundColor: 'rgba(16, 172, 132, 0.25)',
            fill: true,
            tension: 0.35,
            pointRadius: 4,
            pointBackgroundColor: '#1dd1a1'
          },
          {
            label: 'Pelagic Bloom Threshold (1.5 mg/m³)',
            data: data.chlorophyll_baseline,
            borderColor: '#feca57',
            borderDash: [4, 4],
            fill: false
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#e2f1ff' } },
          tooltip: {
            callbacks: {
              label: (ctx) => `Chlorophyll: ${ctx.parsed.y} mg/m³`
            }
          }
        },
        scales: {
          x: { ticks: { color: '#8ba3c7' }, grid: { display: false } },
          y: {
            min: 1.0,
            max: 4.0,
            ticks: { color: '#8ba3c7', callback: (v) => v + ' mg/m³' },
            grid: { color: 'rgba(255, 255, 255, 0.05)' }
          }
        }
      }
    });
  }
}
