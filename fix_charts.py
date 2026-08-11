import os

file_path = r'd:\SMIT PROJECT\frontend\js\portal.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We will replace the entire try-catch block that renders charts in renderOverview
old_charts_pattern = r'try \{\s*const pubRes = await ApiClient\.fetchSecure\(\'/api/analytics/public\'\);.*?\} catch\(e\) \{\s*console\.error\("Failed to render overview charts", e\);\s*\}'

new_charts_code = """try {
        const pubRes = await ApiClient.fetchSecure('/api/analytics/public');
        if (pubRes.ok) {
            const pubData = await pubRes.json();
            
            // Render Category Chart
            if (document.getElementById('categoryChartOverview')) {
                const labels = pubData.categories.map(c => c.category);
                const counts = pubData.categories.map(c => c.count);
                const colors = ['#0F4C81', '#0B7285', '#3B82F6', '#8B5CF6', '#F59E0B', '#10B981', '#6B7280'];
                
                new Chart(document.getElementById('categoryChartOverview'), {
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
                        cutout: '70%',
                        plugins: { legend: { position: 'right', labels: { color: Chart.defaults.color } } } 
                    }
                });
            }
            
            // Render Priority Chart
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
            }
        }
    } catch(e) {
        console.error("Failed to render overview charts", e);
    }"""

content = re.sub(old_charts_pattern, new_charts_code, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated charts in portal.js")
