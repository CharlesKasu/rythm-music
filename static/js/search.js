function search(name) {
    console.log(name)

/*fetch('/login', {

        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ name: })
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
    });*/
}