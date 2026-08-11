import glob
import re

MOBILE_TOGGLE = '\n      <button class="theme-toggle-btn mobile-theme-toggle" aria-label="Toggle Night Mode">\n        <i data-lucide="moon" class="theme-icon"></i>\n      </button>'
DESKTOP_TOGGLE = '\n        <button class="theme-toggle-btn desktop-theme-toggle" aria-label="Toggle Night Mode" style="background: none; border: none; cursor: pointer; color: var(--text-primary); display: flex; align-items: center; padding: 0.4rem;">\n          <i data-lucide="moon" class="theme-icon"></i>\n        </button>\n        '

for filepath in glob.glob(r"d:\SMIT PROJECT\frontend\*.html"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already modified
    if 'desktop-theme-toggle' in content:
        continue

    # Remove existing theme toggles (using ID)
    content = re.sub(
        r'<button id="theme-toggle" class="theme-toggle-btn"[^>]*>\s*<i data-lucide="moon" id="theme-icon"></i>\s*</button>', 
        '', 
        content, 
        flags=re.IGNORECASE
    )
    
    # Also remove any leftover toggle without ID in case
    content = re.sub(
        r'<button id="theme-toggle"[^>]*>\s*<i data-lucide="moon"[^>]*></i>\s*</button>',
        '',
        content,
        flags=re.IGNORECASE
    )

    # Insert mobile toggle after <div class="container">
    content = re.sub(
        r'(<div class="container"[^>]*>)',
        r'\1' + MOBILE_TOGGLE,
        content,
        count=1 # Only the header container
    )

    # Insert desktop toggle before the Sign In / Admin button
    content = re.sub(
        r'(<a href="[^"]*" class="btn btn-outline"[^>]*>.*?</a>\s*</div>)',
        DESKTOP_TOGGLE + r'\1',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("HTML files updated with responsive theme toggles.")
