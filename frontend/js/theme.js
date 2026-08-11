// js/theme.js
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) { lucide.createIcons(); }

    const themeToggleBtns = document.querySelectorAll('.theme-toggle-btn');
    const themeIcons = document.querySelectorAll('.theme-icon');

    if (themeToggleBtns.length > 0) {
        // Initialize icons based on current theme
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        themeIcons.forEach(icon => {
            icon.setAttribute('data-lucide', isDark ? 'sun' : 'moon');
        });
        if (window.lucide) { lucide.createIcons(); }

        themeToggleBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const currentTheme = document.documentElement.getAttribute('data-theme');
                const willBeDark = currentTheme !== 'dark';
                
                if (!willBeDark) {
                    document.documentElement.setAttribute('data-theme', 'light');
                    localStorage.setItem('theme', 'light');
                    themeIcons.forEach(icon => icon.setAttribute('data-lucide', 'moon'));
                } else {
                    document.documentElement.setAttribute('data-theme', 'dark');
                    localStorage.setItem('theme', 'dark');
                    themeIcons.forEach(icon => icon.setAttribute('data-lucide', 'sun'));
                }
                if (window.lucide) { lucide.createIcons(); }
            });
        });
    }

    // Mobile menu toggle
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    if (mobileBtn && navLinks) {
        mobileBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }
});
