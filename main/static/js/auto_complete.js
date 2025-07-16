search_element = document.getElementById('search')
suggestionBox = document.getElementById('suggestionBox')
//implementar of empty style = hidden
search_element.addEventListener('input', function(event){
    const valor = event.target.value
    const csfr_token = document.querySelector('meta[name="csrf_token"]').getAttribute('content')

    fetch('http://127.0.0.1:8000/auto_complete', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csfr_token
    },
    body: JSON.stringify({
        value: valor,
    })
}).then(response => response.json()).then(res => {
    
        suggestionBox.innerHTML = '';

        res.query.forEach(produto => {
            const item = document.createElement('li');
            item.textContent = produto.name;
            item.addEventListener('click', () => {
                search_element.value = produto.name;
                suggestionBox.innerHTML = '';
            })

            suggestionBox.appendChild(item);
        })
    })
})