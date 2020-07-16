// application/static/js/script.js

const confirmDelete = () => {
    document.querySelector('modal').style.display = 'flex';
}


// THEME TOGGLE

let darktheme = localStorage.getItem('darktheme');

const themeToggleButton = document.querySelector('.toggle-theme');

const enableDarkTheme = () => {
    document.body.classList.add('dark-theme');
    localStorage.setItem('darktheme', 'enabled');
    themeToggleButton.textContent = 'light';
}

const disableDarkTheme = () => {
    document.body.classList.remove('dark-theme');
    localStorage.setItem('darktheme', 'disabled');
    themeToggleButton.textContent = 'dark';
}

if (darktheme === 'enabled') {
    enableDarkTheme();
}

themeToggleButton.addEventListener('click', () => {
    darktheme = localStorage.getItem('darktheme');
    if (darktheme === 'disabled') {
        enableDarkTheme();
    } else {
        disableDarkTheme();
    }
});
