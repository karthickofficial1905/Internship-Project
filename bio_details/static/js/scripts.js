const menuBar = document.querySelector('.menu-bar');
const menuBar2 = document.querySelector('.menu-bar2');
const svg1 = document.querySelector('.svg1');
const svg3 = document.querySelector('.svg3');
const footer = document.querySelector('.footer-box');
const footers = document.querySelector('.footer-box-2');
const header = document.querySelector('.header-poit');
const headers = document.querySelector('.header-text');
const section = document.querySelector('.content');



svg1.addEventListener('click', () => {
    menuBar2.classList.remove('active');
    footer.classList.remove('shifted');
    footers.classList.remove('shifted');
    header.classList.remove('shifteds');
    headers.classList.remove('shifteds');
    section.classList.remove('shifteds');
});

svg3.addEventListener('click', () => {
    menuBar2.classList.add('active');
    footer.classList.add('shifted');
    footers.classList.add('shifted');
    header.classList.add('shifteds');
    headers.classList.add('shifteds');
    section.classList.add('shifteds');
});








const mobileMenu = document.querySelector('.mobile-menu');
const menuBar1 = document.querySelector('.menu-bar1');
const closeBtn = document.querySelector('.svg4');

mobileMenu.addEventListener('click', () => {
    menuBar1.classList.add('active');
});

closeBtn.addEventListener('click', () => {
    menuBar1.classList.remove('active');
});





const profilePicInput = document.getElementById('profilePic');
const removeFileBtn = document.getElementById('removeFileBtn');
const filePreview = document.getElementById('filePreview');
const previewImage = document.getElementById('previewImage');

if(profilePicInput && filePreview && previewImage){
    profilePicInput.addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
            const file = this.files[0];
            const reader = new FileReader();
            
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                filePreview.style.display = 'block';
            }
            
            reader.readAsDataURL(file);
        }
    });
}

const emailInput = document.querySelector('input[name="email"]');
const emailError = document.getElementById('emailError');

if(emailInput && emailError){
    emailInput.addEventListener('input', function() {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (this.value && !emailPattern.test(this.value)) {
            emailError.style.display = 'block';
            this.style.borderColor = 'red';
        } else {
            emailError.style.display = 'none';
            this.style.borderColor = '';
        }
    });
}

const phoneInput = document.querySelector('input[name="phone"]');
const phoneError = document.getElementById('phoneError');

if(phoneInput && phoneError){
    phoneInput.addEventListener('input', function() {
        if (this.value.length > 0 && this.value.length < 10) {
            phoneError.style.display = 'block';
            this.style.borderColor = 'red';
        } else {
            phoneError.style.display = 'none';
            this.style.borderColor = '';
        }
    });
}


