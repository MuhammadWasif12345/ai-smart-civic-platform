import os

# 1. Add Chatbot Capability to index.html
index_path = 'frontend/index.html'
with open(index_path, 'r') as f:
    index_html = f.read()

new_card = """          <div class="feature-card">
            <i data-lucide="message-square"></i>
            <h3>Intelligent Civic Chatbot</h3>
            <p>An interactive AI assistant capable of answering any type of civic sense query and guiding users through the reporting process in real-time.</p>
          </div>
        </div>"""

# Replace the closing div of the grid-3 container with the new card and the closing div
if 'Intelligent Civic Chatbot' not in index_html:
    index_html = index_html.replace('          </div>\n        </div>', '          </div>\n' + new_card)
    
    with open(index_path, 'w') as f:
        f.write(index_html)


# 2. Fix the 100vw issue causing cut-offs in base.css
base_path = 'frontend/css/base.css'
with open(base_path, 'r') as f:
    base_css = f.read()

# Replace width: 100vw with width: 100%
if 'width: 100vw;' in base_css:
    base_css = base_css.replace('width: 100vw;', 'width: 100%;\n  max-width: 100%;')
    with open(base_path, 'w') as f:
        f.write(base_css)

print("Fixes applied.")
