import os

index_path = 'frontend/index.html'
with open(index_path, 'r') as f:
    html = f.read()

# Fix grid-3
html = html.replace('grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));', 'grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));')

# Fix charts-grid-home
html = html.replace('grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));', 'grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr));')

# Make sure it centers properly
html = html.replace('margin: 0 auto;\n    }', 'margin: 0 auto;\n      justify-items: center;\n    }')
# Wait, justify-items: center will center the content inside the cell. We want the cell to fill 1fr (which it does), so the card itself centers.
# Actually, 1fr makes the card stretch to fill the available space. If it stretches, it fills the container. 
# The issue on mobile was the overflow caused by 400px > 390px (screen width). This caused a scrollbar and visual left-alignment.

# We will just write the replacements directly to be safe
html = html.replace('.grid-3 {\n      display: grid;\n      grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));\n      gap: 2rem;\n      max-width: 1100px;\n      margin: 0 auto;\n    }', '.grid-3 {\n      display: grid;\n      grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr));\n      gap: 2rem;\n      max-width: 1100px;\n      margin: 0 auto;\n    }')

with open(index_path, 'w') as f:
    f.write(html)

print("Grid CSS updated for centering and overflow prevention.")
