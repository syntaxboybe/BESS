// Dark Mode Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Get the toggle switch element
    const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');

    // Function to set the theme preference in localStorage
    function setTheme(isDarkMode) {
        localStorage.setItem('darkMode', isDarkMode);
    }

    // Function to toggle between dark and light mode with smooth transition
    function switchTheme(e) {
        // Add transition class to body for smooth color changes
        document.body.classList.add('theme-transition');

        // Set a timeout to remove the transition class after the transition is complete
        setTimeout(() => {
            document.body.classList.remove('theme-transition');
        }, 1000);

        if (e.target.checked) {
            document.body.classList.add('dark-mode');
            setTheme(true);

            // Ensure navbar is properly styled in dark mode with fixed layout
            if (document.body.classList.contains('fixed-navbar-layout')) {
                const navbar = document.querySelector('.nav-bottom');
                if (navbar) {
                    navbar.style.backgroundColor = '#0d1a2f';
                }
            }
        } else {
            document.body.classList.remove('dark-mode');
            setTheme(false);

            // Reset navbar style when switching back to light mode
            if (document.body.classList.contains('fixed-navbar-layout')) {
                const navbar = document.querySelector('.nav-bottom');
                if (navbar) {
                    navbar.style.backgroundColor = '#f8f9fa';
                }
            }
        }
    }

    // Exclude specific pages from dark mode
    const currentPath = window.location.pathname;
    const excludedPages = [
        '/home',
        '/about',
        '/contact',
        '/announcement'
    ];

    // Check if current page is in the excluded list
    const isExcludedPage = excludedPages.some(page => currentPath.includes(page));

    // If current page is excluded, hide the toggle switch and don't apply dark mode
    if (isExcludedPage) {
        const themeSwitch = document.querySelector('.theme-switch-wrapper');
        if (themeSwitch) {
            themeSwitch.style.display = 'none';
        }
        // Remove dark mode if it's applied
        document.body.classList.remove('dark-mode');
        return; // Exit early to prevent further execution
    }

    // For non-excluded pages, continue with dark mode functionality
    if (toggleSwitch) {
        // Add event listener to the toggle switch
        toggleSwitch.addEventListener('change', switchTheme, false);

        // Check for saved user preference, if any, on load of the website
        const currentTheme = localStorage.getItem('darkMode');

        if (currentTheme === 'true') {
            toggleSwitch.checked = true;
            document.body.classList.add('dark-mode');

            // Ensure navbar is properly styled in dark mode with fixed layout on page load
            if (document.body.classList.contains('fixed-navbar-layout')) {
                const navbar = document.querySelector('.nav-bottom');
                if (navbar) {
                    navbar.style.backgroundColor = '#0d1a2f';
                }
            }
        }

        // Add tooltip functionality if Bootstrap's tooltip is available
        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    }
});
