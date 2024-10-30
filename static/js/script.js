document.getElementById('inputForm').addEventListener('submit', function (e) {
    e.preventDefault();

    // Collect form data
    const formData = new FormData(this);

    // Send the form data to the Flask server via POST
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())  // Parse the JSON response
    .then(data => {
        // Display the result or error message
        if (data.output && data.predicted_area) {
            document.getElementById('result').innerHTML = 
                `Predicted Crop Yield: ${data.output.toFixed(2)} tons/hectar <br> Area Of Crop: ${data.predicted_area.toFixed(2)} sq.cm`;
        } else if (data.error) {
            document.getElementById('result').innerText = `Error: ${data.error}`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'An error occurred while processing your request.';
    });
});
