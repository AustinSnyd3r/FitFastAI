// Declare dayMappings in a broader scope
let dayMappings = {};

// Function to open the modal with the correct day data
// Function to open the modal with the correct day data
function openModal(title) {
    document.getElementById('modalTitle').textContent = title;

    // Determine the index based on the title
    const dayIndex = title === "Monday" ? 0 :
                     title === "Tuesday" ? 1 :
                     title === "Wednesday" ? 2 :
                     title === "Thursday" ? 3 :
                     title === "Friday" ? 4 : -1; // Default to -1 if not found

    if (dayIndex !== -1) {
        const dayData = dayMappings[dayIndex];
        let modalBodyContent = `<strong>Exercises:</strong><ul>`; // Start with the exercises heading and an unordered list

        // Split the exercises by line and create list items
        const exercisesList = dayData.exercises.split('\n').map(exercise => `<li>${exercise.trim()}</li>`).join('');
        modalBodyContent += exercisesList; // Add list items
        modalBodyContent += `</ul>`; // Close the unordered list

        // Add Duration
        modalBodyContent += `<strong>Duration:</strong> ${dayData.duration || 'Not specified'}<br><br>`; // Add duration

        // Add Recommendations only if they exist
        if (dayData.recommendations && dayData.recommendations.trim() !== 'None') {
            modalBodyContent += `<strong>Recommendations:</strong><ul>`; // Start the recommendations list
            const recommendationsList = dayData.recommendations.split('\n').map(recommendation => `<li>${recommendation.trim()}</li>`).join('');
            modalBodyContent += recommendationsList; // Add list items
            modalBodyContent += `</ul>`; // Close the recommendations unordered list
        } else {
            modalBodyContent += `<strong>Recommendations:</strong> None`; // If no recommendations
        }

        document.getElementById('modalBody').innerHTML = modalBodyContent; // Set modal body content with HTML
    } else {
        document.getElementById('modalBody').textContent = 'No data available for this day.'; // Fallback message
    }

    document.getElementById('modal').style.display = 'block'; // Show modal
}


// Close the modal when clicking the close button
document.getElementById('closeModal').onclick = function() {
    document.getElementById('modal').style.display = 'none';
}

// Close the modal when clicking outside of the modal content
window.onclick = function(event) {
    if (event.target === document.getElementById('modal')) {
        document.getElementById('modal').style.display = 'none';
    }
}

// Fetch workout data on button click
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

            // Parse and structure the workout data
            const structuredWorkoutData = parseWorkoutData(formattedPlan);
            dayMappings = {}; // Reset dayMappings
            structuredWorkoutData.forEach((dayData, index) => {
                dayMappings[index] = dayData; // Map day index to workout data
            });
        } else {
            document.getElementById('response').innerText = 'No valid workout plan received.';
        }
    })
    .catch(error => {
        console.error('Error in js:', error);
        document.getElementById('response').innerText = 'An error occurred while fetching the workout plan.';
    });
});

// Function to parse the workout data
// Function to parse the workout data
// Function to parse the workout data
function parseWorkoutData(data) {
    const days = [];
    const entries = data.trim().split("\n\n"); // Split by double newline

    entries.forEach((entry) => {
        const lines = entry.split("\n").map(line => line.trim());

        // Extract day title (e.g., "Day 1")
        const dayTitle = lines[0];
        const exercises = [];
        let duration = 'Not specified'; // Default value
        let recommendations = 'None'; // Default value

        // Iterate through lines to extract exercises, duration, and recommendations
        for (let i = 1; i < lines.length; i++) {
            if (lines[i].toLowerCase().startsWith("duration:")) {
                duration = lines[i].substring(9).trim(); // Extract duration
            } else if (lines[i].toLowerCase().startsWith("recommendations:")) {
                recommendations = lines[i].substring(16).trim(); // Extract recommendations
                // Gather all following recommendation lines until an empty line
                for (let j = i + 1; j < lines.length; j++) {
                    if (lines[j].trim() === "") break; // Stop at empty line
                    recommendations += `\n${lines[j].trim()}`;
                }
                break; // Exit loop since we processed recommendations
            } else if (lines[i] && !lines[i].toLowerCase().startsWith("exercises:")) { // Skip "Exercises:" header
                exercises.push(lines[i]); // Collect exercises
            }
        }

        // Create an object for each day
        days.push({
            day: dayTitle,
            exercises: exercises.join('\n'), // Join exercises into a single string
            duration: duration,
            recommendations: recommendations
        });
    });

    return days;
}