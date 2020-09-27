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
