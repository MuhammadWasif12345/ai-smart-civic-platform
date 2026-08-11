import glob
import re

# 1. Update theme.js
with open(r'd:\SMIT PROJECT\frontend\js\theme.js', 'r', encoding='utf-8') as f:
    theme_js = f.read()

theme_js = theme_js.replace("'moon-star'", "'moon'")
theme_js = theme_js.replace("'sun-medium'", "'sun'")

with open(r'd:\SMIT PROJECT\frontend\js\theme.js', 'w', encoding='utf-8') as f:
    f.write(theme_js)

# 2. Update HTML files
for filepath in glob.glob(r'd:\SMIT PROJECT\frontend\*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = html.replace('data-lucide="moon-star"', 'data-lucide="moon"')
    html = html.replace('data-lucide="sun-medium"', 'data-lucide="sun"')
    
    # Cache bust theme.js from v=5 to v=6
    html = html.replace('theme.js?v=5', 'theme.js?v=6')
    html = html.replace('theme.js?v=6', 'theme.js?v=7')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
