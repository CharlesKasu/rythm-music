let singupBtn = document.getElementById("singupBtn");
let singinBtn = document.getElementById("singinBtn");
let nameField = document.getElementById("nameField");
let title = document.getElementById("title");
let lostPassword = document.getElementById("lostPassword");
let csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

document.addEventListener('DOMContentLoaded', function () {
    let registerFormBox = document.getElementById("register-form-box");
    let loginFormBox = document.getElementById("login-form-box");

    let showRegister = document.getElementById("show-register");
    let showLogin = document.getElementById("show-login");

        const loginForm = document.getElementById('login-form');

loginForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;
    const errorsContainer = document.getElementById('errors');

fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ email: email, password: password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        if (data.status) {
            window.location.href = '/';
        } else {
            // Wyświetlanie błędów na stronie
            errorsContainer.innerText = data.errors.join('\n');
            errorsContainer.classList.add('error-active');
        }
    })
    .catch(error => {
        // Obsługa innych błędów, np. problemów z siecią, błędów serwera
        console.error('There was a problem with the fetch operation:', error);
        // Wyświetlanie błędów na stronie
        errorsContainer.innerText = 'Error: ' + error.message;
        errorsContainer.classList.add('error-active');
    });
});



 // Funkcja do pobierania wartości cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

    // Funkcja do pokazywania formularza rejestracji
    function showRegisterForm() {
        registerFormBox.classList.add("active");
        loginFormBox.classList.remove("active");
        document.getElementById('errors').classList.remove('error-active'); // Usuń klasę error-active
    }

    // Funkcja do pokazywania formularza logowania
    function showLoginForm() {
        loginFormBox.classList.add("active");
        registerFormBox.classList.remove("active");
        document.getElementById('errors').classList.remove('error-active'); // Usuń klasę error-active
    }

    // Nasłuchiwanie kliknięć
    showRegister.addEventListener('click', function (e) {
        e.preventDefault();
        showRegisterForm();
    });

    showLogin.addEventListener('click', function (e) {
        e.preventDefault();
        showLoginForm();
    });

    // Domyślne ustawienie (np. pokazanie formularza logowania)
    showLoginForm();
});



const registerForm = document.getElementById('register-form');

registerForm.addEventListener('submit', function(e) {
    console.log("TEST")
    e.preventDefault();
        console.log("TEST")


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




    //--------------
        const formData = {
        name: document.querySelector('input[name="name"]').value,
        email: document.querySelector('input[name="regemail"]').value,
        password1: document.querySelector('input[name="password1"]').value,
        password2: document.querySelector('input[name="password2"]').value,
    };

        const errorsContainer = document.getElementById("registerError")

            console.log(JSON.stringify(formData)); // Wyświetl dane przed wysłaniem, aby upewnić się, że są poprawne

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(formData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        if (data.status) {
            window.location.href = '/';
        } else {
            // Wyświetlanie błędów na stronie
            errorsContainer.innerText = data.errors.join('\n');
            errorsContainer.classList.add('error-active');
        }
    })
    .catch(error => {
        // Obsługa innych błędów, np. problemów z siecią, błędów serwera
        console.error('There was a problem with the fetch operation:', error);
        // Wyświetlanie błędów na stronie
        errorsContainer.innerText = 'Error: ' + error.message;
        errorsContainer.classList.add('error-active');
    });
});

