// Toggle password hidden or visible.


const passwordField = document.querySelector('.password__field');
const eyeButton = document.querySelector('.eye__button');

const togglePasswordVisible = () => {
    if (passwordField.type === 'password') {
        document.getElementById('eye__closed_icon').style.display = 'none';
        document.getElementById('eye__opened_icon').style.display = 'block';
        document.querySelector('.password__field').type = 'text';
        eyeButton.setAttribute('aria-label', 'Hide password');
        return;
    } else {
        document.getElementById('eye__closed_icon').style.display = 'block';
        document.getElementById('eye__opened_icon').style.display = 'none';
        document.querySelector('.password__field').type = 'password';
        eyeButton.setAttribute('aria-label', 'Make password visible');
        return;
    }
} 

eyeButton.addEventListener('click', togglePasswordVisible);
