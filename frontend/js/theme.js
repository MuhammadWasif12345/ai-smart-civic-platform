// js/theme.js
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) { lucide.createIcons(); }

    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');

    if (!themeToggleBtn || !themeIcon) return;

    // Initialize icon based on current theme
    if (document.documentElement.getAttribute('data-theme') === 'dark') {
        themeIcon.setAttribute('data-lucide', 'sun');
    } else {
        themeIcon.setAttribute('data-lucide', 'moon');
    }
    if (window.lucide) { lucide.createIcons(); }

    themeToggleBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        // By default, it's light. If data-theme is dark, switch to light.
        if (currentTheme === 'dark') {
            document.documentElement.removeAttribute('data-theme');
            localStorage.setItem('theme', 'light');
            themeIcon.setAttribute('data-lucide', 'moon');
        } else {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            themeIcon.setAttribute('data-lucide', 'sun');
        }
        if (window.lucide) { lucide.createIcons(); }
    });
});
