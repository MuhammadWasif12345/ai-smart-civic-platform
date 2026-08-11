import os
import glob
import re

SCRIPT_REPLACE = """  <script>
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
    }
  </script>"""

toggle_regex = r'(\s*<button id="theme-toggle" class="theme-toggle-btn" aria-label="Toggle Night Mode"[^>]*>\s*<i data-lucide="moon" id="theme-icon"></i>\s*</button>)'
new_toggle = '\n      <button id="theme-toggle" class="theme-toggle-btn" aria-label="Toggle Night Mode">\n        <i data-lucide="moon" id="theme-icon"></i>\n      </button>\n      '

for filepath in glob.glob(r"d:\SMIT PROJECT\frontend\*.html"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace the theme persistence script in <head>
    content = re.sub(
        r'<script>\s*const savedTheme = localStorage\.getItem\(\'theme\'\);.*?</script>', 
        SCRIPT_REPLACE.strip(), 
        content, 
        flags=re.DOTALL
    )

    # 2. Extract theme-toggle from wherever it is and place it before nav-links
    if 'id="theme-toggle"' in content and 'nav-links' in content:
        match = re.search(toggle_regex, content)
        if match:
            toggle_str = match.group(1)
            # Make sure we don't accidentally do this if it's already BEFORE nav-links in the exact right way
            # But just safe to remove and re-add
            content = content.replace(toggle_str, '')
            content = content.replace('<div class="nav-links">', new_toggle + '<div class="nav-links">')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Updated all HTML files successfully.")
