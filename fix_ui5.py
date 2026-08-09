import os

var_path = 'frontend/css/variables.css'
with open(var_path, 'r') as f:
    var_css = f.read()

# Replace current dark mode colors with True Black premium theme
var_css = var_css.replace('--bg-primary: #09090b;', '--bg-primary: #000000;')
var_css = var_css.replace('--bg-secondary: #18181b;', '--bg-secondary: #0a0a0a;')
var_css = var_css.replace('--bg-card: #18181b;', '--bg-card: #0a0a0a;')
var_css = var_css.replace('--bg-input: #27272a;', '--bg-input: #171717;')
var_css = var_css.replace('--border: #334155;', '--border: #262626;') # Dark mode border

with open(var_path, 'w') as f:
    f.write(var_css)

print("Dark mode updated to Pure Black.")
