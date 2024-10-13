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