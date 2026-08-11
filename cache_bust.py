import glob
import re

for filepath in glob.glob(r"d:\SMIT PROJECT\frontend\*.html"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Cache bust css
    content = re.sub(r'href="css/(.*?\.css)(\?v=\d+)?"', r'href="css/\1?v=4"', content)
    
    # Cache bust js
    content = re.sub(r'src="js/(.*?\.js)(\?v=\d+)?"', r'src="js/\1?v=4"', content)

    # In admin-login.html, make the form submission absolutely bulletproof
    if "admin-login.html" in filepath:
        # Change form to use onsubmit
        content = content.replace('<form id="loginForm">', '<form id="loginForm" onsubmit="return handleLogin(event)">')
        
        # Replace the event listener with handleLogin function
        old_listener = "document.getElementById('loginForm').addEventListener('submit', async (e) => {"
        new_function = "async function handleLogin(e) {\n      e.preventDefault();"
        content = content.replace(old_listener, new_function)
        
        # Find the closing bracket of the listener and replace it (very carefully)
        # It ends with:
        #       } finally {
        #         btn.disabled = false;
        #         btn.innerHTML = 'Sign In &rarr;';
        #         if (window.lucide) lucide.createIcons();
        #       }
        #     });
        # We need to change `});` to `}`
        content = content.replace("      }\n    });", "      }\n      return false;\n    }")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Cache busting and admin login fix applied.")
