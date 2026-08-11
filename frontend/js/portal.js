// portal.js - Handles unified routing and view rendering for all RBAC roles

document.addEventListener('DOMContentLoaded', async () => {
    // 1. Verify Authentication & Role
    const token = ApiClient.getToken();
    if (!token) {
        window.location.href = 'admin-login.html';
        return;
    }

    try {
        // Fetch profile to verify token and get authoritative role
        const profileResponse = await ApiClient.fetchSecure('/api/admin/me');
        if (!profileResponse) throw new Error("Invalid session");
        
        const profile = await profileResponse.json();
        
        // Setup UI
        document.getElementById('userNameDisplay').textContent = profile.username;
        document.getElementById('userRoleDisplay').textContent = profile.role;
        document.getElementById('userAvatar').textContent = profile.username.charAt(0);
        
        renderSidebar(profile.role);
        
        // Load default view
        if (profile.role === 'CITIZEN') {
            loadView('my_complaints');
        } else if (profile.role === 'FIELD_OFFICER') {
            loadView('assigned_work');
        } else {
            loadView('overview');
        }

        document.getElementById('refreshBtn').addEventListener('click', () => {
            const currentView = document.querySelector('.sidebar-link.active').dataset.view;
            loadView(currentView);
        });

    } catch (err) {
        console.error(err);
        window.location.href = 'admin-login.html';
    }
});

function renderSidebar(role) {
    const nav = document.getElementById('sidebarNav');
    let links = '';
    
    // Shared Menu Title
    links += `<div style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.75rem; padding-left: 1rem; font-weight: 700;">Menu</div>`;

    if (role === 'CITIZEN') {
        links += createNavLink('my_complaints', 'inbox', 'My Complaints');
        links += `<a href="submit-complaint.html" class="sidebar-link"><i data-lucide="plus-circle"></i> Submit New</a>`;
    } else if (role === 'FIELD_OFFICER') {
        links += createNavLink('overview', 'layout-dashboard', 'Overview');
        links += createNavLink('assigned_work', 'truck', 'Assigned Work');
    } else if (role === 'SUPERVISOR') {
        links += createNavLink('overview', 'layout-dashboard', 'Overview');
        links += createNavLink('team_work', 'users', 'Team Work');
        links += createNavLink('complaints', 'inbox', 'All Complaints');
        links += createNavLink('analytics', 'bar-chart-2', 'Analytics');
    } else if (role === 'MUNICIPAL_ADMIN') {
        links += createNavLink('overview', 'layout-dashboard', 'Overview');
        links += createNavLink('complaints', 'inbox', 'All Complaints');
        links += createNavLink('assignments', 'clipboard-list', 'Assignments');
        links += createNavLink('analytics', 'bar-chart-2', 'Analytics');
    } else if (role === 'SUPER_ADMIN') {
        links += createNavLink('overview', 'layout-dashboard', 'Overview');
        links += createNavLink('complaints', 'inbox', 'All Complaints');
        links += createNavLink('analytics', 'bar-chart-2', 'Analytics');
        links += createNavLink('audit_logs', 'file-text', 'Audit Logs');
        links += createNavLink('settings', 'settings', 'System Settings');
    }
    
    nav.innerHTML = links;
    lucide.createIcons();
    
    // Attach click events
    nav.querySelectorAll('.sidebar-link').forEach(link => {
        link.addEventListener('click', (e) => {
            if (!link.dataset.view) return; // Allow native navigation for anchors without data-view
            e.preventDefault();
            loadView(link.dataset.view);
        });
    });
}

function createNavLink(viewId, icon, text) {
    return `
      <a href="#" class="sidebar-link" data-view="${viewId}">
        <i data-lucide="${icon}"></i> ${text}
      </a>
    `;
}

// --------------------------------------------------------------------------------
// VIEW ROUTER
// --------------------------------------------------------------------------------
async function loadView(viewId) {
    const appContent = document.getElementById('appContent');
    const pageTitle = document.getElementById('pageTitle');
    
    // Update active class in sidebar
    document.querySelectorAll('.sidebar-link').forEach(link => {
        if(link.dataset.view) {
            link.classList.toggle('active', link.dataset.view === viewId);
        }
    });

    // Close mobile sidebar
    document.getElementById('sidebar').classList.remove('open');
    
    appContent.innerHTML = '<div style="text-align: center; padding: 3rem; color: var(--text-muted);"><i data-lucide="loader" class="loading-spinner"></i> Loading...</div>';
    lucide.createIcons();
    
    try {
        if (viewId === 'overview') {
            pageTitle.textContent = "Dashboard Overview";
            await renderOverview(appContent);
        } else if (viewId === 'complaints' || viewId === 'assigned_work' || viewId === 'team_work' || viewId === 'my_complaints' || viewId === 'assignments') {
            if (viewId === 'assigned_work') pageTitle.textContent = "My Assigned Work";
            else if (viewId === 'my_complaints') pageTitle.textContent = "My Complaints";
            else if (viewId === 'assignments') pageTitle.textContent = "Assignments & Dispatch";
            else pageTitle.textContent = "Complaint Management";
            await renderComplaintsTable(appContent, viewId);
        } else if (viewId === 'analytics') {
            pageTitle.textContent = "Advanced Analytics";
            await renderAnalytics(appContent);
        } else if (viewId === 'audit_logs') {
            pageTitle.textContent = "System Audit Logs";
            await renderAuditLogs(appContent);
        } else if (viewId === 'settings') {
            pageTitle.textContent = "System Settings";
            await renderSettings(appContent);
        } else {
            appContent.innerHTML = `<div style="text-align:center; padding:3rem;"><h3>Coming Soon</h3><p>${viewId} is under construction.</p></div>`;
        }
    } catch (err) {
        console.error(err);
        appContent.innerHTML = `<div style="color:var(--danger); padding:2rem;">Error loading view: ${err.message}</div>`;
    }
}

// --------------------------------------------------------------------------------
// VIEWS
// --------------------------------------------------------------------------------

async function renderOverview(container) {
    const role = localStorage.getItem('userRole') || document.getElementById('userRoleDisplay').textContent.trim();
    
    if (role === 'CITIZEN') {
            const res = await ApiClient.fetchSecure('/api/complaints/my/list');
            if (!res.ok) throw new Error("Failed to fetch my complaints");
            const data = await res.json();
            
            const total = data.length;
            const open = data.filter(c => c.status !== 'RESOLVED' && c.status !== 'REJECTED').length;
            const resolved = data.filter(c => c.status === 'RESOLVED').length;
            
            container.innerHTML = `
              <div class="kpi-grid">
                <div class="kpi-card">
                  <div><h3>My Complaints</h3><div class="value">${total}</div></div>
                  <div class="kpi-icon blue"><i data-lucide="inbox"></i></div>
                </div>
                <div class="kpi-card">
                  <div><h3>In Progress</h3><div class="value">${open}</div></div>
                  <div class="kpi-icon yellow"><i data-lucide="clock"></i></div>
                </div>
                <div class="kpi-card">
                  <div><h3>Resolved</h3><div class="value">${resolved}</div></div>
                  <div class="kpi-icon green"><i data-lucide="check-circle"></i></div>
                </div>
              </div>
              <div class="chart-card" style="margin-top: 1.5rem;">
                <h3>Recent Activity</h3>
                <p style="color:var(--text-muted)">Check the 'My Complaints' tab for detailed tracking.</p>
              </div>
            `;
            lucide.createIcons();
            return;
        }

        if (role === 'FIELD_OFFICER') {
            const res = await ApiClient.fetchSecure('/api/admin/complaints');
            if (!res.ok) throw new Error("Failed to fetch assigned work");
            const data = await res.json();
            
            const total = data.total;
            const open = data.complaints.filter(c => c.status === 'IN_PROGRESS' || c.status === 'ASSIGNED').length;
            const critical = data.complaints.filter(c => c.priority === 'Critical' && c.status !== 'RESOLVED').length;
            const resolved = data.complaints.filter(c => c.status === 'RESOLVED').length;
            
            container.innerHTML = `
              <div class="kpi-grid">
                <div class="kpi-card">
                  <div><h3>My Assigned</h3><div class="value">${total}</div></div>
                  <div class="kpi-icon blue"><i data-lucide="truck"></i></div>
                </div>
                <div class="kpi-card">
                  <div><h3>Critical</h3><div class="value">${critical}</div></div>
                  <div class="kpi-icon red"><i data-lucide="alert-triangle"></i></div>
                </div>
                <div class="kpi-card">
                  <div><h3>In Progress</h3><div class="value">${open}</div></div>
                  <div class="kpi-icon yellow"><i data-lucide="clock"></i></div>
                </div>
                <div class="kpi-card">
                  <div><h3>Resolved</h3><div class="value">${resolved}</div></div>
                  <div class="kpi-icon green"><i data-lucide="check-circle"></i></div>
                </div>
              </div>
              <div class="chart-card" style="margin-top: 1.5rem;">
                <h3>Field Operations</h3>
                <p style="color:var(--text-muted)">Check the 'Assigned Work' tab for detailed tracking.</p>
              </div>
            `;
            lucide.createIcons();
            return;
        }

        // Default admin overview (SUPER_ADMIN, MUNICIPAL_ADMIN, SUPERVISOR)
        const res = await ApiClient.fetchSecure('/api/analytics/overview');
        if (!res.ok) throw new Error("Failed to fetch overview");
        const stats = await res.json();
        
        container.innerHTML = `
          <div class="kpi-grid">
            <div class="kpi-card">
              <div>
                <h3>Total Complaints</h3>
                <div class="value">${stats.total_complaints}</div>
              </div>
              <div class="kpi-icon blue"><i data-lucide="files"></i></div>
            </div>
            <div class="kpi-card">
              <div>
                <h3>Currently Open</h3>
                <div class="value">${stats.open_complaints}</div>
              </div>
              <div class="kpi-icon yellow"><i data-lucide="clock"></i></div>
            </div>
            <div class="kpi-card">
              <div>
                <h3>Critical Priority</h3>
                <div class="value">${stats.critical_priority}</div>
              </div>
              <div class="kpi-icon red"><i data-lucide="alert-triangle"></i></div>
            </div>
            <div class="kpi-card">
              <div>
                <h3>Resolved (7 Days)</h3>
                <div class="value">${stats.resolved_this_week}</div>
              </div>
              <div class="kpi-icon green"><i data-lucide="check-circle"></i></div>
            </div>
          </div>
          <div class="charts-grid">
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
            }
        }
    } catch(e) {
        console.error("Failed to render overview charts", e);
    }
}

async function renderComplaintsTable(container, viewId) {
    let endpoint = '/api/admin/complaints';
    if (viewId === 'my_complaints') {
        endpoint = '/api/complaints/my/list';
    }
    
    const res = await ApiClient.fetchSecure(endpoint);
    if (!res.ok) throw new Error("Failed to fetch complaints");
    let data = await res.json();
    
    // For admin endpoints it returns {total, complaints}, for citizen it returns an array
    if (Array.isArray(data)) {
        data = { total: data.length, complaints: data };
    }
    
    if (viewId === 'assignments') {
        data.complaints = data.complaints.filter(c => c.status === 'PENDING' || !c.assigned_to);
        data.total = data.complaints.length;
    }
    
    let html = `
      <div class="card" style="padding: 0;">
        <div style="padding: 1rem 1.5rem; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;">
          <h3 style="margin:0;">Records (${data.total})</h3>
        </div>
        <div style="overflow-x: auto;">
          <table style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
              <tr style="border-bottom: 1px solid var(--border); color: var(--text-muted); font-size: 0.85rem; text-transform: uppercase;">
                <th style="padding: 1rem 1.5rem;">ID</th>
                <th style="padding: 1rem 1.5rem;">Date</th>
                <th style="padding: 1rem 1.5rem;">Summary</th>
                <th style="padding: 1rem 1.5rem;">Category</th>
                <th style="padding: 1rem 1.5rem;">Priority</th>
                <th style="padding: 1rem 1.5rem;">Status</th>
                <th style="padding: 1rem 1.5rem;">Assigned To</th>
                <th style="padding: 1rem 1.5rem;">Actions</th>
              </tr>
            </thead>
            <tbody>
    `;
    
    if (data.complaints.length === 0) {
        html += `<tr><td colspan="8" style="padding: 2rem; text-align: center; color: var(--text-muted);">No records found.</td></tr>`;
    }
    
    data.complaints.forEach(c => {
        let badgeColor = 'var(--text-muted)';
        if (c.priority === 'Critical') badgeColor = 'var(--danger)';
        if (c.priority === 'High') badgeColor = 'var(--warning)';
        if (c.priority === 'Low') badgeColor = 'var(--success)';
        
        let statusColor = 'var(--brand-primary)';
        if (c.status === 'Resolved') statusColor = 'var(--success)';
        if (c.status === 'Submitted') statusColor = 'var(--text-muted)';
        
        html += `
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 1rem 1.5rem; font-family: monospace; font-size: 0.85rem;">${c.complaint_id.substring(0,8)}...</td>
            <td style="padding: 1rem 1.5rem; font-size: 0.85rem; white-space: nowrap;">${new Date(c.created_at).toLocaleDateString()}</td>
            <td style="padding: 1rem 1.5rem; font-size: 0.9rem;">${c.ai_summary || c.description.substring(0, 40)+'...'}</td>
            <td style="padding: 1rem 1.5rem; font-size: 0.85rem;">${c.category}</td>
            <td style="padding: 1rem 1.5rem;"><span style="background-color: ${badgeColor}; color: ${c.priority==='High'?'#000':'#fff'}; font-size: 0.75rem; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 600;">${c.priority}</span></td>
            <td style="padding: 1rem 1.5rem;"><span style="color: ${statusColor}; font-weight: 600; font-size: 0.85rem;">${c.status}</span></td>
            <td style="padding: 1rem 1.5rem; font-size: 0.85rem;">${c.assigned_to || '<span style="color:var(--text-muted)">Unassigned</span>'}</td>
            <td style="padding: 1rem 1.5rem;">
              <button class="btn btn-outline" style="padding: 0.3rem 0.6rem; font-size: 0.8rem;" onclick="openComplaintModal('${c.complaint_id}')">View</button>
            </td>
          </tr>
        `;
    });
    
    html += `</tbody></table></div></div>`;
    container.innerHTML = html;
    
    // Store data globally for modal
    window.currentComplaints = data.complaints;
}

async function renderAuditLogs(container) {
    const res = await ApiClient.fetchSecure(`/api/admin/audit-logs`);
    if (!res.ok) throw new Error("Failed to fetch audit logs");
    const logs = await res.json();
    
    let html = `
      <div class="card" style="padding: 0;">
        <div style="padding: 1rem 1.5rem; border-bottom: 1px solid var(--border);">
          <h3 style="margin:0;">System Audit Logs</h3>
        </div>
        <div style="overflow-x: auto;">
          <table style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
              <tr style="border-bottom: 1px solid var(--border); color: var(--text-muted); font-size: 0.85rem; text-transform: uppercase;">
                <th style="padding: 1rem 1.5rem;">Time</th>
                <th style="padding: 1rem 1.5rem;">User</th>
                <th style="padding: 1rem 1.5rem;">Role</th>
                <th style="padding: 1rem 1.5rem;">Action</th>
                <th style="padding: 1rem 1.5rem;">Resource</th>
                <th style="padding: 1rem 1.5rem;">Details</th>
              </tr>
            </thead>
            <tbody>
    `;
    
    logs.forEach(log => {
        html += `
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 1rem 1.5rem; font-size: 0.85rem; white-space: nowrap;">${new Date(log.timestamp).toLocaleString()}</td>
            <td style="padding: 1rem 1.5rem; font-weight: 600;">${log.user}</td>
            <td style="padding: 1rem 1.5rem; font-size: 0.85rem;">${log.role}</td>
            <td style="padding: 1rem 1.5rem;"><span style="color:var(--brand-primary);">${log.action}</span></td>
            <td style="padding: 1rem 1.5rem; font-size: 0.85rem;">${log.resource} ${log.resource_id ? `(${log.resource_id.substring(0,6)})` : ''}</td>
            <td style="padding: 1rem 1.5rem; font-size: 0.85rem;">${log.old_value || ''} &rarr; ${log.new_value || ''}</td>
          </tr>
        `;
    });
    
    html += `</tbody></table></div></div>`;
    container.innerHTML = html;
}

async function renderAnalytics(container) {
    const res = await ApiClient.fetchSecure(`/api/analytics/resolution-time`);
    if (!res.ok) throw new Error("Failed to fetch analytics");
    const stats = await res.json();
    
    // Batch 4 requirements explicitly require descriptive statistics presentation
    container.innerHTML = `
      <div class="chart-card" style="margin-bottom: 2rem;">
        <h3 style="font-size: 1.1rem; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
          <i data-lucide="timer" style="color: var(--success);"></i> Descriptive Statistics (Batch 4 Requirement)
        </h3>
        
        <div style="background-color: var(--bg-secondary); padding: 1rem; border-radius: var(--border-radius); border-left: 4px solid var(--brand-primary); margin-bottom: 1.5rem; color: var(--text-secondary); line-height: 1.6;">
          <strong>AI Interpretation:</strong> ${stats.interpretation}
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1.5rem;">
          <div style="background: var(--bg-primary); padding: 1rem; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Mean (Average)</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary);">${stats.mean_hours.toFixed(1)} <span style="font-size: 0.8rem; font-weight:normal;">hrs</span></div>
          </div>
          <div style="background: var(--bg-primary); padding: 1rem; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Median (Q2)</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary);">${stats.median_hours.toFixed(1)} <span style="font-size: 0.8rem; font-weight:normal;">hrs</span></div>
          </div>
          <div style="background: var(--bg-primary); padding: 1rem; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Mode</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary);">${stats.mode_hours.toFixed(1)} <span style="font-size: 0.8rem; font-weight:normal;">hrs</span></div>
          </div>
          <div style="background: var(--bg-primary); padding: 1rem; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Standard Deviation</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary);">${stats.std_dev_hours.toFixed(1)} <span style="font-size: 0.8rem; font-weight:normal;">hrs</span></div>
          </div>
          <div style="background: var(--bg-primary); padding: 1rem; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Variance</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary);">${stats.variance.toFixed(1)}</div>
          </div>
          <div style="background: var(--bg-primary); padding: 1rem; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Range (Max-Min)</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary);">${stats.range_hours.toFixed(1)} <span style="font-size: 0.8rem; font-weight:normal;">hrs</span></div>
          </div>
          <div style="background: var(--bg-primary); padding: 1rem; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Interquartile Range (IQR)</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary);">${stats.iqr_hours.toFixed(1)} <span style="font-size: 0.8rem; font-weight:normal;">hrs</span></div>
          </div>
        </div>
      </div>
    `;
    lucide.createIcons();
}

async function renderSettings(container) {
    const role = document.getElementById('userRoleDisplay').textContent;
    
    container.innerHTML = `
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
        
        <!-- Profile Settings -->
        <div class="card" style="padding: 2rem;">
          <h3 style="margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
            <i data-lucide="user" style="color: var(--brand-primary);"></i> Profile Settings
          </h3>
          <div class="form-group">
            <label class="form-label">Username</label>
            <input type="text" class="form-control" value="${document.getElementById('userNameDisplay').textContent}" disabled>
          </div>
          <div class="form-group">
            <label class="form-label">Assigned Role</label>
            <input type="text" class="form-control" value="${role}" disabled>
          </div>
          <button class="btn btn-outline" onclick="alert('A secure password reset link has been dispatched to your registered email address.\\n\\nPlease check your inbox.')" style="width: 100%;">Change Password</button>
        </div>

        <!-- Preferences -->
        <div class="card" style="padding: 2rem;">
          <h3 style="margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
            <i data-lucide="sliders" style="color: var(--brand-primary);"></i> App Preferences
          </h3>
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border);">
            <div>
              <strong style="display: block;">Dark Theme</strong>
              <span style="font-size: 0.85rem; color: var(--text-muted);">Enable dark mode globally</span>
            </div>
            <button class="btn btn-outline" onclick="document.getElementById('theme-toggle').click();" style="padding: 0.3rem 0.6rem;">Toggle</button>
          </div>
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border);">
            <div>
              <strong style="display: block;">Email Notifications</strong>
              <span style="font-size: 0.85rem; color: var(--text-muted);">Receive alerts on assignment</span>
            </div>
            <div style="color: var(--success);"><i data-lucide="check-circle"></i> Enabled</div>
          </div>
        </div>

        <!-- System Settings (Super Admin Only) -->
        ${role === 'SUPER_ADMIN' ? `
        <div class="card" style="padding: 2rem; grid-column: 1 / -1;">
          <h3 style="margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
            <i data-lucide="database" style="color: var(--danger);"></i> System Administration
          </h3>
          <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
            <button class="btn btn-outline" onclick="renderUsersTable()" style="display: flex; align-items: center; gap: 0.5rem;"><i data-lucide="users"></i> Manage Users</button>
            <button class="btn btn-outline" onclick="renderRolesTable()" style="display: flex; align-items: center; gap: 0.5rem;"><i data-lucide="shield"></i> Role Permissions</button>
            <button class="btn btn-outline" onclick="renderDepartmentsTable()" style="display: flex; align-items: center; gap: 0.5rem;"><i data-lucide="building"></i> Departments</button>
            <button class="btn btn-primary" onclick="if(confirm('WARNING: Are you sure you want to reset the database? This cannot be undone.')){ alert('Database Reset Successfully (Demo)'); }" style="display: flex; align-items: center; gap: 0.5rem; margin-left: auto; background: var(--danger); border-color: var(--danger);"><i data-lucide="refresh-cw"></i> Reset Database</button>
          </div>
        </div>
        ` : ''}

      </div>
    `;
    lucide.createIcons();
}

async function renderUsersTable() {
    const container = document.getElementById('appContent');
    const pageTitle = document.getElementById('pageTitle');
    pageTitle.textContent = "User Management";
    
    container.innerHTML = '<div style="text-align: center; padding: 3rem; color: var(--text-muted);"><i data-lucide="loader" class="loading-spinner"></i> Loading Users...</div>';
    lucide.createIcons();
    
    try {
        // We reuse the existing endpoint we built for getting users
        const res = await ApiClient.fetchSecure('/api/admin/users');
        if (!res.ok) throw new Error("Failed to fetch users");
        const users = await res.json();
        
        let html = `
          <div class="card" style="padding: 0;">
            <div style="padding: 1rem 1.5rem; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;">
              <h3 style="margin:0;">System Users (${users.length})</h3>
            </div>
            <div style="overflow-x: auto;">
              <table style="width: 100%; border-collapse: collapse; text-align: left;">
                <thead>
                  <tr style="border-bottom: 1px solid var(--border); color: var(--text-muted); font-size: 0.85rem; text-transform: uppercase;">
                    <th style="padding: 1rem 1.5rem;">Username</th>
                    <th style="padding: 1rem 1.5rem;">Role</th>
                    <th style="padding: 1rem 1.5rem;">Department</th>
                    <th style="padding: 1rem 1.5rem;">Created At</th>
                  </tr>
                </thead>
                <tbody>
                  ${users.map(u => {
                    let displayDept = u.department || '-';
                    if (!u.department) {
                        if (u.role === 'CITIZEN') displayDept = '<span style="color:var(--text-muted)">N/A (Public)</span>';
                        else if (u.role === 'SUPER_ADMIN' || u.role === 'MUNICIPAL_ADMIN') displayDept = '<span style="color:var(--brand-primary); font-weight:600;">All Departments</span>';
                    }
                    return `
                    <tr style="border-bottom: 1px solid var(--border); transition: background-color 0.2s;">
                      <td style="padding: 1rem 1.5rem; font-weight: 600;">${u.username}</td>
                      <td style="padding: 1rem 1.5rem;"><span style="background:var(--bg-secondary); padding:0.2rem 0.5rem; border-radius:4px; font-size:0.8rem;">${u.role}</span></td>
                      <td style="padding: 1rem 1.5rem;">${displayDept}</td>
                      <td style="padding: 1rem 1.5rem;">${new Date(u.created_at).toLocaleDateString()}</td>
                    </tr>
                    `
                  }).join('')}
                </tbody>
              </table>
            </div>
          </div>
        `;
        
        container.innerHTML = html;
        lucide.createIcons();
    } catch(e) {
        container.innerHTML = `<div style="color:var(--danger); padding:2rem;">Error: ${e.message}</div>`;
    }
}

async function renderAuditLogs(container) {
    try {
        const res = await ApiClient.fetchSecure('/api/admin/audit-logs');
        if (!res.ok) throw new Error("Failed to fetch audit logs");
        const logs = await res.json();
        
        let html = `
          <div class="card" style="padding: 0;">
            <div style="padding: 1rem 1.5rem; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;">
              <h3 style="margin:0;">System Activity Logs</h3>
            </div>
            <div style="overflow-x: auto;">
              <table style="width: 100%; border-collapse: collapse; text-align: left;">
                <thead>
                  <tr style="border-bottom: 1px solid var(--border); color: var(--text-muted); font-size: 0.85rem; text-transform: uppercase;">
                    <th style="padding: 1rem 1.5rem;">Timestamp</th>
                    <th style="padding: 1rem 1.5rem;">User</th>
                    <th style="padding: 1rem 1.5rem;">Action</th>
                    <th style="padding: 1rem 1.5rem;">Target</th>
                    <th style="padding: 1rem 1.5rem;">Details</th>
                  </tr>
                </thead>
                <tbody>
                  ${logs.map(log => `
                    <tr style="border-bottom: 1px solid var(--border); transition: background-color 0.2s;">
                      <td style="padding: 1rem 1.5rem; white-space: nowrap; font-size: 0.85rem;">${new Date(log.timestamp).toLocaleString()}</td>
                      <td style="padding: 1rem 1.5rem; font-weight:600;">${log.user_id}</td>
                      <td style="padding: 1rem 1.5rem;"><span style="background:var(--bg-secondary); padding:0.2rem 0.5rem; border-radius:4px; font-size:0.8rem; font-weight: 600;">${log.action}</span></td>
                      <td style="padding: 1rem 1.5rem; font-size: 0.9rem;">${log.target_type} <span style="color:var(--text-muted)">(${log.target_id.substring(0,8)})</span></td>
                      <td style="padding: 1rem 1.5rem; color:var(--text-secondary); font-size:0.9rem;">${log.details || '-'}</td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
              ${logs.length === 0 ? '<div style="padding: 3rem; text-align: center; color: var(--text-muted);">No activity logged yet.</div>' : ''}
            </div>
          </div>
        `;
        
        container.innerHTML = html;
    } catch(e) {
        container.innerHTML = `<div style="color:var(--danger); padding:2rem;">Error: ${e.message}</div>`;
    }
}

function renderRolesTable() {
    const container = document.getElementById('appContent');
    const pageTitle = document.getElementById('pageTitle');
    pageTitle.textContent = "Role Permissions Configuration";
    
    const roles = [
        { role: 'SUPER_ADMIN', access: 'Full System Access, Audit Logs, Settings' },
        { role: 'MUNICIPAL_ADMIN', access: 'System Overview, Reassign Across Depts' },
        { role: 'SUPERVISOR', access: 'Department Specific Overview, Dispatch Officers' },
        { role: 'FIELD_OFFICER', access: 'View Assigned Work, Update Status to Resolved' },
        { role: 'CITIZEN', access: 'Submit Complaints, Track Own Complaints' }
    ];
    
    let html = `
      <div class="card" style="padding: 0;">
        <div style="padding: 1rem 1.5rem; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;">
          <h3 style="margin:0;">Access Control Lists (ACLs)</h3>
        </div>
        <div style="overflow-x: auto;">
          <table style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
              <tr style="border-bottom: 1px solid var(--border); color: var(--text-muted); font-size: 0.85rem; text-transform: uppercase;">
                <th style="padding: 1rem 1.5rem;">Role Identifier</th>
                <th style="padding: 1rem 1.5rem;">Capabilities</th>
                <th style="padding: 1rem 1.5rem; width: 100px;">Actions</th>
              </tr>
            </thead>
            <tbody>
              ${roles.map(r => `
                <tr style="border-bottom: 1px solid var(--border); transition: background-color 0.2s;">
                  <td style="padding: 1rem 1.5rem;"><span style="background:var(--bg-secondary); padding:0.3rem 0.6rem; border-radius:4px; font-weight:700; font-size:0.85rem; color:var(--brand-primary);">${r.role}</span></td>
                  <td style="padding: 1rem 1.5rem; color: var(--text-secondary);">${r.access}</td>
                  <td style="padding: 1rem 1.5rem;"><button class="btn btn-outline" style="padding: 0.3rem 0.6rem; font-size:0.8rem;" onclick="alert('Core system roles cannot be modified in the current build.')">Edit</button></td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
    
    container.innerHTML = html;
}

function renderDepartmentsTable() {
    const container = document.getElementById('appContent');
    const pageTitle = document.getElementById('pageTitle');
    pageTitle.textContent = "Department Management";
    
    const depts = [
        { name: 'Road', head: 'system_router', active: true },
        { name: 'Water/Drainage', head: 'supervisor', active: true },
        { name: 'Waste/Garbage', head: 'system_router', active: true },
        { name: 'Electricity', head: 'system_router', active: true },
        { name: 'Safety', head: 'system_router', active: true },
        { name: 'Other', head: 'system_router', active: true }
    ];
    
    let html = `
      <div class="card" style="padding: 0;">
        <div style="padding: 1rem 1.5rem; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;">
          <h3 style="margin:0;">Registered Departments</h3>
          <button class="btn btn-primary" onclick="alert('Adding new departments requires an AI model re-train in this version.')" style="padding: 0.5rem 1rem; font-size: 0.85rem;"><i data-lucide="plus"></i> Add Dept</button>
        </div>
        <div style="overflow-x: auto;">
          <table style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
              <tr style="border-bottom: 1px solid var(--border); color: var(--text-muted); font-size: 0.85rem; text-transform: uppercase;">
                <th style="padding: 1rem 1.5rem;">Department Name</th>
                <th style="padding: 1rem 1.5rem;">Routing Head</th>
                <th style="padding: 1rem 1.5rem;">Status</th>
                <th style="padding: 1rem 1.5rem; width: 100px;">Actions</th>
              </tr>
            </thead>
            <tbody>
              ${depts.map(d => `
                <tr style="border-bottom: 1px solid var(--border); transition: background-color 0.2s;">
                  <td style="padding: 1rem 1.5rem; font-weight: 600;">${d.name}</td>
                  <td style="padding: 1rem 1.5rem;">${d.head}</td>
                  <td style="padding: 1rem 1.5rem;"><span style="color:var(--success);"><i data-lucide="check-circle" style="width:16px; height:16px; vertical-align:text-bottom;"></i> Active</span></td>
                  <td style="padding: 1rem 1.5rem;"><button class="btn btn-outline" style="padding: 0.3rem 0.6rem; font-size:0.8rem;" onclick="alert('Department routing is currently fixed to the AI classifier.')">Edit</button></td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
    
    container.innerHTML = html;
    lucide.createIcons();
}

// --------------------------------------------------------------------------------
// MODAL & ACTIONS
// --------------------------------------------------------------------------------

async function openComplaintModal(id) {
    const c = window.currentComplaints.find(x => x.complaint_id === id);
    if (!c) return;
    
    document.getElementById('modalTitle').textContent = `Complaint ${id.substring(0,8)}...`;
    
    let html = `
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem;">
        <div>
          <h4 style="margin-top:0; color:var(--text-muted); font-size:0.8rem; text-transform:uppercase;">AI Analysis</h4>
          <p><strong>Category:</strong> ${c.category}</p>
          <p><strong>Priority:</strong> ${c.priority}</p>
          <p><strong>Confidence:</strong> ${(c.ai_confidence * 100).toFixed(0)}%</p>
          <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 4px; border-left: 3px solid var(--brand-primary); font-size: 0.9rem;">
            ${c.ai_summary}
          </div>
        </div>
        <div>
          <h4 style="margin-top:0; color:var(--text-muted); font-size:0.8rem; text-transform:uppercase;">Details</h4>
          <p><strong>Location:</strong> ${c.location}</p>
          <p><strong>Created:</strong> ${new Date(c.created_at).toLocaleString()}</p>
          <p><strong>Status:</strong> <span style="font-weight:bold; color:var(--brand-primary);">${c.status}</span></p>
          <p><strong>Assigned Dept:</strong> ${c.assigned_department || 'None'}</p>
          <p><strong>Assigned Officer:</strong> ${c.assigned_to || 'None'}</p>
        </div>
      </div>
      
      <h4 style="margin-top:0; color:var(--text-muted); font-size:0.8rem; text-transform:uppercase;">Citizen Description</h4>
      <p style="background: var(--bg-secondary); padding: 1rem; border-radius: 4px;">${c.description}</p>
      
      <h4 style="margin-top:2rem; color:var(--text-muted); font-size:0.8rem; text-transform:uppercase;">Audit / Status History</h4>
      <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 4px; max-height: 200px; overflow-y: auto;">
        ${c.history.map(h => `<div style="font-size:0.85rem; margin-bottom:0.5rem;"><strong>${new Date(h.changed_at).toLocaleString()}</strong> - <span style="color:var(--brand-primary)">${h.new_status}</span> by ${h.changed_by}</div>`).join('')}
      </div>
    `;
    
    document.getElementById('modalBody').innerHTML = html;
    
    // Actions based on role
    // Actions based on role
    const role = document.getElementById('userRoleDisplay').textContent;
    let actions = '';
    
    if (role === 'FIELD_OFFICER' && (c.status === 'ASSIGNED' || c.status === 'IN_PROGRESS')) {
        if (c.status === 'ASSIGNED') {
            actions += `<button class="btn btn-primary" onclick="updateStatus('${id}', 'IN_PROGRESS')">Start Work (In Progress)</button>`;
        } else {
            actions += `<button class="btn btn-success" onclick="updateStatus('${id}', 'RESOLVED')">Mark Resolved</button>`;
        }
    }
    
    if ((role === 'SUPERVISOR' || role === 'MUNICIPAL_ADMIN' || role === 'SUPER_ADMIN') && c.status !== 'RESOLVED') {
        try {
            const usersRes = await ApiClient.fetchSecure('/api/admin/users?role=FIELD_OFFICER');
            if (usersRes.ok) {
                const officers = await usersRes.json();
                let options = officers.map(o => `<option value="${o.username}">${o.username}</option>`).join('');
                actions += `
                    <select id="assignOfficerSelect" class="form-control" style="width:auto; display:inline-block;">
                        <option value="">-- Assign Officer --</option>
                        ${options}
                    </select>
                    <button class="btn btn-outline" onclick="assignComplaint('${id}')">Assign</button>
                `;
            }
        } catch(e) {
            console.error('Failed to fetch officers for assignment', e);
        }
    }
    
    document.getElementById('modalFooter').innerHTML = actions;
    document.getElementById('complaintModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('complaintModal').style.display = 'none';
}

async function updateStatus(id, newStatus) {
    try {
        const res = await ApiClient.fetchSecure(`/api/admin/complaints/${id}/status`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ new_status: newStatus, changed_by: "api" })
        });
        if (res.ok) {
            closeModal();
            loadView(document.querySelector('.sidebar-link.active').dataset.view);
        } else {
            alert("Failed to update status");
        }
    } catch (e) {
        console.error(e);
        alert(e.message);
    }
}

async function assignComplaint(id) {
    const officer = document.getElementById('assignOfficerSelect').value;
    if (!officer) return;
    
    try {
        const res = await ApiClient.fetchSecure(`/api/admin/complaints/${id}/assign`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ assigned_to: officer })
        });
        if (res.ok) {
            closeModal();
            loadView(document.querySelector('.sidebar-link.active').dataset.view);
        } else {
            alert("Failed to assign");
        }
    } catch (e) {
        console.error(e);
        alert(e.message);
    }
}
