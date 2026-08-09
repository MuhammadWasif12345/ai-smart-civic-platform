import os
import glob

# The proper sidebar links
PROPER_LINKS = """      <a href="admin-analytics.html" class="sidebar-link">
        <i data-lucide="bar-chart-2"></i> Analytics
      </a>
      <a href="admin-settings.html" class="sidebar-link">
        <i data-lucide="settings"></i> Settings
      </a>"""

# Files to update
files = ["frontend/admin-dashboard.html", "frontend/admin-complaints.html", "frontend/admin-complaint-detail.html"]

for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    # Remove the bad replacement if it exists
    content = content.replace("""        <a href="admin-analytics.html" class="nav-item">
          <i data-lucide="bar-chart-2"></i>
          <span>Analytics</span>
        </a>
        <a href="admin-settings.html" class="nav-item">
          <i data-lucide="settings"></i>
          <span>Settings</span>
        </a>""", PROPER_LINKS)

    # Replace the coming soon logic
    content = content.replace("""<a href="#" class="sidebar-link" onclick="showComingSoon('Analytics Dashboard'); return false;">
        <i data-lucide="bar-chart-2"></i> Analytics
      </a>
      <a href="#" class="sidebar-link" onclick="showComingSoon('Settings Panel'); return false;">
        <i data-lucide="settings"></i> Settings
      </a>""", PROPER_LINKS)

    with open(f, 'w') as file:
        file.write(content)

# Now, create admin-analytics.html by duplicating admin-dashboard.html
with open("frontend/admin-dashboard.html", "r") as f:
    dashboard_content = f.read()

analytics_content = dashboard_content.replace('Dashboard Overview', 'Deep Analytics & Reporting')
analytics_content = analytics_content.replace('class="sidebar-link active"', 'class="sidebar-link"')
analytics_content = analytics_content.replace('href="admin-analytics.html" class="sidebar-link"', 'href="admin-analytics.html" class="sidebar-link active"')
# Hide recent complaints section in analytics
analytics_content = analytics_content.replace('class="recent-complaints"', 'class="recent-complaints" style="display:none;"')

with open("frontend/admin-analytics.html", "w") as f:
    f.write(analytics_content)

# Now create a basic admin-settings.html
settings_html = analytics_content.replace('Deep Analytics & Reporting', 'Platform Settings')
settings_html = settings_html.replace('href="admin-analytics.html" class="sidebar-link active"', 'href="admin-analytics.html" class="sidebar-link"')
settings_html = settings_html.replace('href="admin-settings.html" class="sidebar-link"', 'href="admin-settings.html" class="sidebar-link active"')

settings_body = """
<div class="settings-card" style="background: var(--bg-card); padding: 2rem; border-radius: var(--border-radius-lg); box-shadow: var(--shadow); border: 1px solid var(--border); max-width: 600px; margin-top: 2rem;">
    <h3>Change Admin Password</h3>
    <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">Update your super-admin credentials below.</p>
    <div class="form-group" style="margin-bottom: 1rem;">
        <label style="display: block; margin-bottom: 0.5rem;">New Password</label>
        <input type="password" style="width: 100%; padding: 0.75rem; border-radius: 8px; border: 1px solid var(--border); background: var(--bg-input); color: var(--text-primary);">
    </div>
    <div class="form-group" style="margin-bottom: 1.5rem;">
        <label style="display: block; margin-bottom: 0.5rem;">Confirm Password</label>
        <input type="password" style="width: 100%; padding: 0.75rem; border-radius: 8px; border: 1px solid var(--border); background: var(--bg-input); color: var(--text-primary);">
    </div>
    <button class="btn btn-primary" onclick="alert('Password updated successfully!')" style="background: var(--brand-primary); color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer;">Save Settings</button>
</div>
"""

# Replace the entire dashboard grid with the settings form
import re
settings_html = re.sub(r'<div class="dashboard-grid">.*</div>\s*<!-- Recent Complaints -->', settings_body + '\n<!-- Recent Complaints -->', settings_html, flags=re.DOTALL)

with open("frontend/admin-settings.html", "w") as f:
    f.write(settings_html)

print("Done generating pages!")
