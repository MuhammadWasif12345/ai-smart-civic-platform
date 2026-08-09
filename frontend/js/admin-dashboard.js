// --------------------------------------------------------------------------------
// ADMIN DASHBOARD JAVASCRIPT
// Fetches analytics data from the backend and uses Chart.js to render it.
// --------------------------------------------------------------------------------

// Keep track of our chart instances so we can destroy and recreate them when refreshing
let categoryChartInstance = null;
let priorityChartInstance = null;

async function loadDashboardData() {
  const refreshIcon = document.getElementById("refreshIcon");
  refreshIcon.classList.add("loading-spinner"); // Make it spin
  refreshIcon.style.display = "inline-block";

  try {
    // 1. Fetch Overview Stats
    const overviewRes = await ApiClient.fetchSecure("/api/analytics/overview");
    if (overviewRes && overviewRes.ok) {
      const data = await overviewRes.json();
      document.getElementById("statTotal").innerText = data.total_complaints;
      document.getElementById("statOpen").innerText = data.open_complaints;
      document.getElementById("statCritical").innerText = data.critical_priority;
      document.getElementById("statResolved").innerText = data.resolved_this_week;
    }

    // 2. Fetch Category Distribution (for Pie Chart)
    const categoryRes = await ApiClient.fetchSecure("/api/analytics/distribution/category");
    if (categoryRes && categoryRes.ok) {
      const data = await categoryRes.json();
      renderCategoryChart(data);
    }

    // 3. Fetch Priority Distribution (for Bar Chart)
    const priorityRes = await ApiClient.fetchSecure("/api/analytics/distribution/priority");
    if (priorityRes && priorityRes.ok) {
      const data = await priorityRes.json();
      renderPriorityChart(data);
    }

    // 4. Fetch Resolution Time Stats (The core Batch 4 requirement)
    const timeRes = await ApiClient.fetchSecure("/api/analytics/resolution-time");
    if (timeRes && timeRes.ok) {
      const data = await timeRes.json();
      document.getElementById("statMean").innerText = data.mean_hours;
      document.getElementById("statMedian").innerText = data.median_hours;
      document.getElementById("statMode").innerText = data.mode_hours;
      document.getElementById("statStdDev").innerText = data.std_dev_hours;
      document.getElementById("statIQR").innerText = data.iqr_hours;
      
      // Update the plain English interpretation text
      document.getElementById("statInterpretation").innerHTML = 
        `<i data-lucide="info" style="width:18px; height:18px; display:inline; vertical-align:-3px; margin-right:5px;"></i> ${data.interpretation}`;
      lucide.createIcons(); // re-init the info icon we just injected
    }

  } catch (error) {
    console.error("Failed to load dashboard data", error);
  } finally {
    refreshIcon.classList.remove("loading-spinner");
  }
}

function renderCategoryChart(data) {
  const ctx = document.getElementById('categoryChart').getContext('2d');
  
  if (categoryChartInstance) {
    categoryChartInstance.destroy();
  }

  // Extract the labels and numbers from the API response
  const labels = data.map(d => d.category);
  const counts = data.map(d => d.count);
  
  // Pretty colors for the pie slices
  const colors = [
    '#0F4C81', '#0B7285', '#3B82F6', '#8B5CF6', '#F59E0B', '#10B981', '#6B7280'
  ];

  categoryChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: counts,
        backgroundColor: colors.slice(0, labels.length),
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'right' }
      },
      cutout: '70%' // Makes it a thin donut ring instead of a full pie
    }
  });
}

function renderPriorityChart(data) {
  const ctx = document.getElementById('priorityChart').getContext('2d');
  
  if (priorityChartInstance) {
    priorityChartInstance.destroy();
  }

  const labels = data.map(d => d.priority);
  const counts = data.map(d => d.count);
  
  // We map the colors to match our CSS variables for consistency
  const colorMap = {
    'Critical': '#C81E1E', // Red
    'High': '#A16207',     // Orange
    'Medium': '#854D0E',   // Yellow
    'Low': '#157347'       // Green
  };
  const backgroundColors = labels.map(label => colorMap[label] || '#6B7280');

  priorityChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Number of Complaints',
        data: counts,
        backgroundColor: backgroundColors,
        borderRadius: 4 // Soft rounded corners on the bars
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false } // Hide legend since the X-axis labels are clear enough
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1 } // Don't show decimal counts for complaints
        }
      }
    }
  });
}

// Load the data immediately when the page opens
document.addEventListener("DOMContentLoaded", () => {
  loadDashboardData();
});
