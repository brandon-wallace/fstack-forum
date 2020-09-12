// application/static/js/script.js


"use strict";


const confirmDelete = () => {
    document.querySelector('modal').style.display = 'flex';
}


// Dark/Light theme toggle.

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

/*
themeToggleButton.addEventListener('click', () => {
    darktheme = localStorage.getItem('darktheme');
    if (darktheme === 'disabled') {
        enableDarkTheme();
    } else {
        disableDarkTheme();
    }
});
*/


// Toggle password hidden or visible.

const passwordText = document.querySelector('.password__field');
const eyeButton = document.querySelector('.eye__button');
let passwordVisible = false;

const togglePasswordVisible = () => {
    if (passwordVisible === false) {
        document.getElementById('eye__closed_icon').style.display = 'none';
        document.getElementById('eye__opened_icon').style.display = 'block';
        document.querySelector('.password__field').type = 'text';
        passwordVisible = true;
        return;
    } else {
        document.getElementById('eye__closed_icon').style.display = 'block';
        document.getElementById('eye__opened_icon').style.display = 'none';
        document.querySelector('.password__field').type = 'password';
        passwordVisible = false;
        return;
    }
} 

eyeButton.addEventListener('click', togglePasswordVisible);
