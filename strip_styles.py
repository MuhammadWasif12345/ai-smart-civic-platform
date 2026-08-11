import glob
import re

for filepath in glob.glob(r'd:\SMIT PROJECT\frontend\*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the desktop toggle and remove the style attribute entirely
    content = re.sub(
        r'<button class="theme-toggle-btn desktop-theme-toggle" aria-label="Toggle Night Mode" style="[^"]+">',
        r'<button class="theme-toggle-btn desktop-theme-toggle" aria-label="Toggle Night Mode">',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Removed inline styles from toggles")
