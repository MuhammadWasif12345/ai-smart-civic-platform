// js/theme.js
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) { lucide.createIcons(); }

    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');

    if (!themeToggleBtn || !themeIcon) return;

    // Initialize icon based on current theme set in <head>
    if (document.documentElement.getAttribute('data-theme') === 'light') {
        themeIcon.setAttribute('data-lucide', 'moon');
    } else {
        themeIcon.setAttribute('data-lucide', 'sun');
    }
    if (window.lucide) { lucide.createIcons(); }

    themeToggleBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        // By default, it's dark. If data-theme is light, switch to dark.
        if (currentTheme === 'light') {
            document.documentElement.removeAttribute('data-theme');
            localStorage.setItem('theme', 'dark');
            themeIcon.setAttribute('data-lucide', 'sun');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
            themeIcon.setAttribute('data-lucide', 'moon');
        }
        if (window.lucide) { lucide.createIcons(); }
    });
});
