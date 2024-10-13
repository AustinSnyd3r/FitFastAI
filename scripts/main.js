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
    const url = `http://127.0.0.1:5000/generate_workout?name=${encodeURIComponent(name)}&bio=${encodeURIComponent(bio)}`;
    // Sending a POST request with query parameters
    fetch(url, {
        method: 'POST',  
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data && data.workout_plan && Array.isArray(data.workout_plan)) {
            let formattedPlan = '';
            data.workout_plan.forEach((day, index) => {
                formattedPlan += `Day ${index + 1}:\n`;
                if (day.exercises) {
                    formattedPlan += `Exercises: ${day.exercises.replace(/\*\*/g, '').trim()}\n`;
                }
                if (day.duration) {
                    formattedPlan += `Duration: ${day.duration.replace(/\*\*/g, '').trim()}\n`;
                }
                if (day.recommendations) {
                    formattedPlan += `Recommendations: ${day.recommendations.replace(/\*\*/g, '').split('\n\n')[0].trim()}\n`;
                }
                formattedPlan += '\n';
            });
            
            // Add general recommendations if available
            if (data.workout_plan[4] && data.workout_plan[4].recommendations) {
                const generalRecs = data.workout_plan[4].recommendations.split('General Recommendations for the Week:')[1];
                if (generalRecs) {
                    formattedPlan += 'General Recommendations for the Week:\n' + generalRecs.trim();
                }
            }
            
            document.getElementById('response').innerText = formattedPlan;
        } else {
            document.getElementById('response').innerText = 'No valid workout plan received.';
        }
    })
    .catch(error => {
        console.error('Error in js:', error);
        document.getElementById('response').innerText = 'An error occurred while fetching the workout plan.';
    });
});