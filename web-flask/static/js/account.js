function saveDetails() {
    var editedData = {
        first_name: document.getElementById('first-name').innerText.trim(),
        last_name: document.getElementById('last-name').innerText.trim(),
        username: document.getElementById('username').innerText.trim(),
        email: document.getElementById('email').innerText.trim(),
        dob: document.getElementById('date-of-birth').innerText.trim()
    };

    // Filter out null or undefined values (unchanged fields)
    var updatedData = Object.fromEntries(
        Object.entries(editedData).filter(([_, value]) => value != null)
    );

    // Print values for debugging
    console.log('Edited Values:');
    console.log(updatedData);

    $.ajax({
        type: 'POST',
        url: '/update_user_details',
        contentType: 'application/json',
        data: JSON.stringify(updatedData),
        success: function(response) {
            console.log('Server Response:', response);
            alert('Details saved successfully!');
        },
        error: function(error) {
            console.error('Error:', error);
            alert('Error saving details.');
        }
    });
}
