// application/static/js/script.js

"use strict";


// Dark/Light theme toggle.

let darktheme = localStorage.getItem('darktheme');

const themeToggleButton = document.querySelector('.toggle-theme');

const enableDarkTheme = () => {
    document.body.classList.add('dark-theme');
    localStorage.setItem('darktheme', 'enabled');
    themeToggleButton.textContent = 'light theme';
}

const disableDarkTheme = () => {
    document.body.classList.remove('dark-theme');
    localStorage.setItem('darktheme', 'disabled');
    themeToggleButton.textContent = 'dark theme';
}

if (darktheme === 'enabled') {
    enableDarkTheme();
}

if (themeToggleButton) {
    themeToggleButton.addEventListener('click', () => {
        darktheme = localStorage.getItem('darktheme');
        if (darktheme === 'disabled') {
            enableDarkTheme();
        } else {
            disableDarkTheme();
        }
    });
}


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
                                                                                
if (eyeButton) {                                                                
    eyeButton.addEventListener('click', togglePasswordVisible);                 
}                                                                               
                                                                                

// Close flash messages.

const closeMessageButton = document.querySelector('.close');

if (closeMessageButton) {
    closeMessageButton.addEventListener('click', () => {
        document.querySelector('.message').remove();
    });
}


// Open comment form.

const openCommentButton = document.querySelectorAll('.reply');
const commentForm = document.querySelector('.comment__form');

if (openCommentButton) {
    for (let i = 0; i < openCommentButton.length; i++) {
        openCommentButton[i].addEventListener('click', () => {
            commentForm.style.display = 'block';
            commentForm.scrollIntoView(false);
        });
    }
}
