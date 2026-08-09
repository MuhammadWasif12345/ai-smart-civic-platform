import os

# 1. Update variables.css for elegant dark mode
var_path = 'frontend/css/variables.css'
with open(var_path, 'r') as f:
    var_css = f.read()

# Replace dark mode colors
var_css = var_css.replace('--bg-primary: #0b1120;', '--bg-primary: #09090b;')
var_css = var_css.replace('--bg-secondary: #111827;', '--bg-secondary: #18181b;')
var_css = var_css.replace('--bg-card: #151e2f;', '--bg-card: #18181b;')
var_css = var_css.replace('--bg-input: #1e293b;', '--bg-input: #27272a;')

with open(var_path, 'w') as f:
    f.write(var_css)


# 2. Add overflow-x: hidden to body to fix mobile cut off
base_path = 'frontend/css/base.css'
with open(base_path, 'r') as f:
    base_css = f.read()

if 'overflow-x: hidden;' not in base_css:
    base_css = base_css.replace('min-height: 100vh;', 'min-height: 100vh;\n  overflow-x: hidden;\n  width: 100vw;')
    
# Clean up the previous logo hack
base_css = base_css.replace("""  header .logo {
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
  }""", "")

with open(base_path, 'w') as f:
    f.write(base_css)


# 3. Update the logo HTML in all public pages to stack perfectly
public_pages = ['frontend/index.html', 'frontend/submit-complaint.html', 'frontend/track-complaint.html', 'frontend/about.html', 'frontend/admin-login.html']

old_logo = """      <a href="index.html" class="logo">
        <i data-lucide="shield-check"></i>
        AI Smart Civic <span style="font-size:0.6rem; margin-left:0.5rem; background:var(--brand-primary); color:white; padding:0.2rem 0.4rem; border-radius:4px;">AI Powered</span>
      </a>"""

new_logo = """      <a href="index.html" class="logo" style="display:flex; flex-direction:column; align-items:center; gap:2px; text-decoration:none;">
        <div style="display:flex; align-items:center; gap:0.5rem; white-space:nowrap; font-size:1.1rem; line-height:1;">
            <i data-lucide="shield-check" style="width:20px;"></i> AI Smart Civic
        </div>
        <span style="font-size:0.6rem; background:var(--brand-primary); color:white; padding:0.1rem 0.4rem; border-radius:4px; line-height:1;">AI Powered</span>
      </a>"""

for page in public_pages:
    with open(page, 'r') as f:
        content = f.read()
    
    if old_logo in content:
        content = content.replace(old_logo, new_logo)
    
    with open(page, 'w') as f:
        f.write(content)

print("Dark mode and logo fixes applied.")
