document.addEventListener('DOMContentLoaded', function() {
    const menuButton = document.getElementById('menu-button');
    const navbarToggle = document.getElementById('navbarToggle');

    menuButton.addEventListener('click', function() {
        // Toggle the menu visibility
        navbarToggle.classList.toggle('hidden');

        // Rotate the menu icon
        this.classList.toggle('rotate-90');
    });
});
