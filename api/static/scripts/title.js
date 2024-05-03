function select_difficulty(mode){
    fetch('/select_difficulty', { 
        method: 'POST', 
        headers: { 
            'Content-Type': 'application/json'
        }, 
        body: JSON.stringify({mode: mode}) 
    }) 
    .then(response => response.text()) 
    .then(result => { 
        console.log(result); 
    }) 
    .catch(error => { 
        console.error('Error:', error); 
    }); 
    return;
}