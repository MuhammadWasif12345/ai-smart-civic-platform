import os

file_path = r'd:\SMIT PROJECT\frontend\js\portal.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update renderSettings
old_settings = """
        <!-- System Settings (Super Admin Only) -->
        ${role === 'Super Admin' ? `
        <div class="card" style="padding: 2rem; grid-column: 1 / -1;">
          <h3 style="margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
            <i data-lucide="database" style="color: var(--danger);"></i> System Administration
          </h3>
          <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
            <button class="btn btn-outline" style="display: flex; align-items: center; gap: 0.5rem;"><i data-lucide="users"></i> Manage Users</button>
            <button class="btn btn-outline" style="display: flex; align-items: center; gap: 0.5rem;"><i data-lucide="shield"></i> Role Permissions</button>
            <button class="btn btn-outline" style="display: flex; align-items: center; gap: 0.5rem;"><i data-lucide="building"></i> Departments</button>
            <button class="btn btn-primary" style="display: flex; align-items: center; gap: 0.5rem; margin-left: auto; background: var(--danger); border-color: var(--danger);"><i data-lucide="refresh-cw"></i> Reset Database</button>
          </div>
        </div>
        ` : ''}
"""

new_settings = """
        <!-- System Settings (Super Admin Only) -->
        ${role === 'Super Admin' ? `
        <div class="card" style="padding: 2rem; grid-column: 1 / -1;">
          <h3 style="margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
            <i data-lucide="database" style="color: var(--danger);"></i> System Administration
          </h3>
          <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
            <button class="btn btn-outline" onclick="alert('User Management Console is opening...\\n(Demo Action)')" style="display: flex; align-items: center; gap: 0.5rem;"><i data-lucide="users"></i> Manage Users</button>
            <button class="btn btn-outline" onclick="alert('Role Permissions Editor is opening...\\n(Demo Action)')" style="display: flex; align-items: center; gap: 0.5rem;"><i data-lucide="shield"></i> Role Permissions</button>
            <button class="btn btn-outline" onclick="alert('Department Configuration is opening...\\n(Demo Action)')" style="display: flex; align-items: center; gap: 0.5rem;"><i data-lucide="building"></i> Departments</button>
            <button class="btn btn-primary" onclick="if(confirm('WARNING: Are you sure you want to reset the database? This cannot be undone.')){ alert('Database Reset Successfully (Demo)'); }" style="display: flex; align-items: center; gap: 0.5rem; margin-left: auto; background: var(--danger); border-color: var(--danger);"><i data-lucide="refresh-cw"></i> Reset Database</button>
          </div>
        </div>
        ` : ''}
"""

content = content.replace(old_settings, new_settings)

old_profile_btn = '<button class="btn btn-outline" style="width: 100%;">Change Password</button>'
new_profile_btn = '<button class="btn btn-outline" onclick="alert(\'A secure password reset link has been dispatched to your registered email address.\\\\n\\\\nPlease check your inbox.\')" style="width: 100%;">Change Password</button>'
content = content.replace(old_profile_btn, new_profile_btn)

# 2. Update renderOverview
old_overview_end = """
      <div class="chart-card">
        <h3>Recent Activity</h3>
        <p style="color:var(--text-muted)">Check the 'All Complaints' tab for detailed tracking.</p>
      </div>
    `;
    lucide.createIcons();
}
"""

new_overview_end = """
      <div class="charts-grid">
        <div class="chart-card">
          <h3 style="margin-bottom: 1.5rem;">Category Distribution</h3>
          <canvas id="categoryChartOverview" height="250"></canvas>
        </div>
        <div class="chart-card">
          <h3 style="margin-bottom: 1.5rem;">Priority Breakdown</h3>
          <canvas id="priorityChartOverview" height="250"></canvas>
        </div>
      </div>
      <div class="chart-card" style="margin-top: 1.5rem;">
        <h3>Recent Activity</h3>
        <p style="color:var(--text-muted)">Check the 'All Complaints' tab for detailed tracking.</p>
      </div>
    `;
    lucide.createIcons();
    
    // Fetch public analytics data for charts
    try {
        const pubRes = await ApiClient.fetchSecure('/api/analytics/public');
        if (pubRes.ok) {
            const pubData = await pubRes.json();
            
            // Render Category Chart
            if (document.getElementById('categoryChartOverview')) {
                new Chart(document.getElementById('categoryChartOverview'), {
                    type: 'doughnut',
                    data: {
                        labels: pubData.categories.map(c => c.category),
                        datasets: [{
                            data: pubData.categories.map(c => c.count),
                            backgroundColor: ['#22b8f0', '#8b5cf6', '#10b981', '#f59e0b', '#64748b'],
                            borderWidth: 0
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { color: Chart.defaults.color } } } }
                });
            }
            
            // Render Priority Chart
            if (document.getElementById('priorityChartOverview')) {
                new Chart(document.getElementById('priorityChartOverview'), {
                    type: 'bar',
                    data: {
                        labels: pubData.priorities.map(p => p.priority),
                        datasets: [{
                            label: 'Complaints',
                            data: pubData.priorities.map(p => p.count),
                            backgroundColor: pubData.priorities.map(p => p.priority === 'Critical' ? '#ef4444' : p.priority === 'High' ? '#f59e0b' : '#10b981'),
                            borderRadius: 6
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, grid: { color: 'rgba(148, 163, 184, 0.1)' } }, x: { grid: { display: false } } } }
                });
            }
        }
    } catch(e) {
        console.error("Failed to render overview charts", e);
    }
}
"""

content = content.replace(old_overview_end, new_overview_end)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated portal.js successfully")
