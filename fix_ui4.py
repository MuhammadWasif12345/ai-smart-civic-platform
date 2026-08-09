import os

base_path = 'frontend/css/base.css'
with open(base_path, 'r') as f:
    base_css = f.read()

# Make sure html has the proper background and overflow settings
if 'background-color: var(--bg-primary);' not in base_css.split('html {')[1].split('}')[0]:
    base_css = base_css.replace('html {\n  scroll-behavior: smooth;\n}', 'html {\n  scroll-behavior: smooth;\n  overflow-x: hidden;\n  width: 100%;\n  max-width: 100%;\n  background-color: var(--bg-primary);\n}')
    
    with open(base_path, 'w') as f:
        f.write(base_css)

print("HTML tag updated.")
