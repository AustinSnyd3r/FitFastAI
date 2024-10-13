// This links to the home page
function openModal(title, body) {
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalBody').textContent = body;
    document.getElementById('modal').style.display = 'block';
}

document.getElementById('closeModal').onclick = function() {
    document.getElementById('modal').style.display = 'none';
}

// Close the modal when clicking outside of the modal content
window.onclick = function(event) {
    if (event.target === document.getElementById('modal')) {
        document.getElementById('modal').style.display = 'none';
    }
}


document.getElementById('promptButton').addEventListener('click', () => {
    const bio = document.getElementById('bio').value;
    const name = document.getElementById('name').value;

    // Construct the URL with query parameters
    const url = `http://127.0.0.1:5000/generate_workout?name=${name}&bio=${bio}`;
    console.log(url);
    // Sending a GET request with query parameters
    fetch(url, {
        method: 'POST',  
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').innerText = data.message;
    })
    .catch(error => {
        console.error('Error in js:', error);
    });
});