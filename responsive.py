import os
import glob
import re

# 1. Update base.css
base_css_path = 'frontend/css/base.css'
with open(base_css_path, 'r') as f:
    base_css = f.read()

responsive_css = """
/* Mobile Navigation */
.hamburger {
  display: none;
  background: transparent;
  border: none;
  color: var(--text-primary);
  cursor: pointer;
  padding: 0.5rem;
}
@media (max-width: 768px) {
  header .container {
    padding: 0 1rem;
    position: relative;
  }
  .hamburger {
    display: flex;
    order: 1;
  }
  header .logo {
    order: 2;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    font-size: 1rem;
  }
  .theme-toggle-btn {
    order: 3;
    margin-left: auto;
  }
  header .nav-links {
    display: none;
    flex-direction: column;
    position: absolute;
    top: 70px;
    left: 0;
    width: 100%;
    background: var(--bg-card);
    border-bottom: 1px solid var(--border);
    padding: 1rem;
    box-shadow: var(--shadow);
    gap: 1rem;
    z-index: 999;
  }
  header .nav-links.active {
    display: flex;
  }
  header .nav-links a {
    width: 100%;
    text-align: center;
    padding: 0.75rem 0;
  }
}
"""

if '.hamburger {' not in base_css:
    with open(base_css_path, 'a') as f:
        f.write(responsive_css)

# 2. Update Public Pages
public_pages = ['frontend/index.html', 'frontend/submit-complaint.html', 'frontend/track-complaint.html', 'frontend/about.html', 'frontend/admin-login.html']

for page in public_pages:
    with open(page, 'r') as f:
        content = f.read()
    
    if '<button id="mobile-menu-btn"' not in content:
        # Move theme-toggle out of nav-links and add hamburger
        # Find theme toggle
        theme_toggle_str = """        <button id="theme-toggle" class="theme-toggle-btn" aria-label="Toggle Night Mode">
          <i data-lucide="moon" id="theme-icon"></i>
        </button>"""
        
        # Remove from old position
        content = content.replace(theme_toggle_str, '')
        
        # Insert hamburger, logo, and theme toggle in container
        # Find logo
        logo_match = re.search(r'(<a href="index\.html" class="logo">.*?</a>)', content, re.DOTALL)
        if logo_match:
            logo_full = logo_match.group(1)
            new_header = f"""
      <button id="mobile-menu-btn" class="hamburger">
        <i data-lucide="menu"></i>
      </button>
      {logo_full}
{theme_toggle_str}"""
            content = content.replace(logo_full, new_header)
            
        with open(page, 'w') as f:
            f.write(content)

# 3. Update theme.js to handle mobile menu
theme_js_path = 'frontend/js/theme.js'
with open(theme_js_path, 'r') as f:
    theme_js = f.read()

if 'mobile-menu-btn' not in theme_js:
    mobile_js = """
    // Mobile menu toggle
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    if (mobileBtn && navLinks) {
        mobileBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }
"""
    theme_js = theme_js.replace('});', mobile_js + '});')
    with open(theme_js_path, 'w') as f:
        f.write(theme_js)

# 4. Update Admin Pages
admin_pages = ['frontend/admin-dashboard.html', 'frontend/admin-analytics.html', 'frontend/admin-settings.html', 'frontend/admin-complaints.html', 'frontend/admin-complaint-detail.html']

admin_css = """
    /* Mobile Admin CSS */
    .admin-hamburger {
      display: none;
      background: transparent;
      border: none;
      color: var(--text-primary);
      cursor: pointer;
      padding: 0.5rem;
      margin-right: 1rem;
    }
    @media (max-width: 768px) {
      .sidebar {
        position: fixed;
        left: -260px;
        top: 0;
        bottom: 0;
        box-shadow: var(--shadow);
      }
      .sidebar.open {
        left: 0;
      }
      .admin-hamburger {
        display: block;
      }
      .topbar {
        padding: 0 1rem;
      }
      .topbar h2 {
        font-size: 1.25rem;
      }
      .kpi-grid {
        grid-template-columns: 1fr;
      }
      .content-area {
        padding: 1rem;
      }
    }
"""

for page in admin_pages:
    with open(page, 'r') as f:
        content = f.read()
    
    if '.admin-hamburger {' not in content:
        # Add CSS
        content = content.replace('</style>', admin_css + '</style>')
        
        # Add Hamburger to topbar
        # <div class="topbar">
        #   <h2>Dashboard Overview</h2>
        # or similar
        topbar_match = re.search(r'(<header class="topbar">\s*<h2>.*?</h2>)', content, re.DOTALL)
        if topbar_match:
            topbar_full = topbar_match.group(1)
            title = re.search(r'<h2>(.*?)</h2>', topbar_full).group(1)
            
            new_topbar = f"""<header class="topbar">
      <div style="display:flex; align-items:center;">
        <button id="admin-menu-btn" class="admin-hamburger">
          <i data-lucide="menu"></i>
        </button>
        <h2>{title}</h2>
      </div>"""
            content = content.replace(topbar_full, new_topbar)
        
        # Add JS to toggle
        admin_js = """
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const adminBtn = document.getElementById('admin-menu-btn');
      const sidebar = document.getElementById('sidebar');
      if(adminBtn && sidebar) {
        adminBtn.addEventListener('click', () => {
          sidebar.classList.toggle('open');
        });
      }
    });
  </script>
</body>"""
        content = content.replace('</body>', admin_js)
        
        with open(page, 'w') as f:
            f.write(content)

print("Responsive fixes applied.")
