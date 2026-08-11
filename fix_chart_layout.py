import os

file_path = r'd:\SMIT PROJECT\frontend\js\portal.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the chart HTML wrapper
old_html = '''      <div class="charts-grid">
        <div class="chart-card">
          <h3 style="margin-bottom: 1.5rem;">Category Distribution</h3>
          <canvas id="categoryChartOverview" height="250"></canvas>
        </div>
        <div class="chart-card">
          <h3 style="margin-bottom: 1.5rem;">Priority Breakdown</h3>
          <canvas id="priorityChartOverview" height="250"></canvas>
        </div>
      </div>'''

new_html = '''      <div class="charts-grid">
        <div class="chart-card">
          <h3 style="margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;"><i data-lucide="pie-chart" style="color: var(--brand-primary);"></i> Category Distribution</h3>
          <div style="position: relative; height: 280px; width: 100%;">
            <canvas id="categoryChartOverview"></canvas>
          </div>
        </div>
        <div class="chart-card">
          <h3 style="margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;"><i data-lucide="bar-chart" style="color: var(--warning);"></i> Priority Breakdown</h3>
          <div style="position: relative; height: 280px; width: 100%;">
            <canvas id="priorityChartOverview"></canvas>
          </div>
        </div>
      </div>'''

content = content.replace(old_html, new_html)

# Fix the Priority Chart JS
old_priority_js = '''            // Render Priority Chart
            if (document.getElementById('priorityChartOverview')) {
                const labels = pubData.priorities.map(p => p.priority);
                const counts = pubData.priorities.map(p => p.count);
                
                const colorMap = {
                    'Critical': '#C81E1E',
                    'High': '#A16207',
                    'Medium': '#854D0E',
                    'Low': '#157347'
                };
                const backgroundColors = labels.map(label => colorMap[label] || '#6B7280');
                
                new Chart(document.getElementById('priorityChartOverview'), {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Number of Complaints',
                            data: counts,
                            backgroundColor: backgroundColors,
                            borderRadius: 4
                        }]
                    },
                    options: { 
                        responsive: true, 
                        maintainAspectRatio: false, 
                        plugins: { legend: { display: false } }, 
                        scales: { 
                            y: { beginAtZero: true, ticks: { stepSize: 1, color: Chart.defaults.color }, grid: { color: 'rgba(148, 163, 184, 0.1)' } }, 
                            x: { ticks: { color: Chart.defaults.color }, grid: { display: false } } 
                        } 
                    }
                });
            }'''

new_priority_js = '''            // Render Priority Chart
            if (document.getElementById('priorityChartOverview')) {
                const allLabels = ['Critical', 'High', 'Low', 'Medium'];
                const allColors = ['#C81E1E', '#A16207', '#157347', '#854D0E'];
                
                const dataMap = {};
                pubData.priorities.forEach(p => { dataMap[p.priority] = p.count; });
                const counts = allLabels.map(l => dataMap[l] || 0);
                
                new Chart(document.getElementById('priorityChartOverview'), {
                    type: 'bar',
                    data: {
                        labels: allLabels,
                        datasets: [{
                            label: 'Number of Complaints',
                            data: counts,
                            backgroundColor: allColors,
                            borderRadius: 4
                        }]
                    },
                    options: { 
                        responsive: true, 
                        maintainAspectRatio: false, 
                        plugins: { legend: { display: false } }, 
                        scales: { 
                            y: { beginAtZero: true, ticks: { stepSize: 1, color: Chart.defaults.color }, grid: { color: 'rgba(148, 163, 184, 0.1)' } }, 
                            x: { ticks: { color: Chart.defaults.color }, grid: { display: false } } 
                        } 
                    }
                });
            }'''

content = content.replace(old_priority_js, new_priority_js)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated portal.js layout and priority chart logic")
