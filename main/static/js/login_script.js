document.getElementById('submit').addEventListener('click', () =>{
    const username = document.getElementById('username').value
    const password = document.getElementById('password').value

    const csfr_token = document.querySelector('meta[name="csrf_token"]').getAttribute('content')

    fetch('http://127.0.0.1:8000/login_request', {
        method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csfr_token,
    },
    body: JSON.stringify({
        username: username,
        password: password
    })

    }).then(response => response.json())
    .then(data => {
    console.log(data);
    })
    .catch(error => {
    console.error('Erro:', error);
    });
})