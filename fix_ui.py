import os
import re

# 1. Fix mobile logo & header stickiness
base_css_path = 'frontend/css/base.css'
with open(base_css_path, 'r') as f:
    base_css = f.read()

# Fix sticky header
base_css = base_css.replace('z-index: 100;', 'z-index: 9999;\n  top: 0;\n  -webkit-sticky: sticky;')

# Fix mobile logo stacking
if '.logo-container' not in base_css:
    mobile_logo_css = """
  header .logo {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;
    font-size: 1rem;
    line-height: 1.1;
  }
  header .logo span {
    margin-left: 0 !important;
    font-size: 0.6rem !important;
  }
  header .logo i {
    display: none;
  }
"""
    # Insert right before the last closing brace of the media query or just append to the media query
    base_css = base_css.replace('header .nav-links.active {', mobile_logo_css + '  header .nav-links.active {')
    with open(base_css_path, 'w') as f:
        f.write(base_css)

# 2. Fix Chatbot Send Icon
index_path = 'frontend/index.html'
with open(index_path, 'r') as f:
    index_html = f.read()

# Add flex-shrink: 0 to the send button to prevent squishing
index_html = index_html.replace('justify-content: center; transition: opacity 0.2s;">', 'justify-content: center; transition: opacity 0.2s; flex-shrink: 0; min-width: 40px;">')
with open(index_path, 'w') as f:
    f.write(index_html)

# 3. Fix Settings Page (Remove KPI and Charts)
settings_path = 'frontend/admin-settings.html'
with open(settings_path, 'r') as f:
    settings_html = f.read()

# Use regex to strip out the KPI grid and the charts grid
settings_html = re.sub(r'<div class="kpi-grid">.*?</div>\s*<div class="charts-grid">.*?</div>', '', settings_html, flags=re.DOTALL)
settings_html = re.sub(r'<!-- KPI Cards -->.*?<!-- Charts -->.*?(?=<div class="settings-card")', '', settings_html, flags=re.DOTALL)

with open(settings_path, 'w') as f:
    f.write(settings_html)

print("UI fixes applied successfully.")
