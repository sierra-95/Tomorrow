document.addEventListener('DOMContentLoaded', function () {
    const calendarDays = document.querySelectorAll('.calendar-days div');
    const eventPopup = document.querySelector('.event-popup');
    const closeBtn = document.querySelector('.close-btn');
    const saveBtn = document.getElementById('save-btn');
    const eventDescriptionInput = document.getElementById('event-description'); // Add this line

    calendarDays.forEach(day => {
        day.addEventListener('click', () => {
            const selectedDate = day.textContent;
            openEventPopup(selectedDate);
        });
    });

    function openEventPopup(date) {
        const dateLabel = document.querySelector('.event-popup label');
        dateLabel.textContent = `Event for ${date}`;
        eventPopup.classList.add('active');
    }

    closeBtn.addEventListener('click', closeEventPopup);

    // Combine the event listeners into one
    saveBtn.addEventListener('click', function () {
        saveEvent();
        closeEventPopup();
    });

    function closeEventPopup() {
        eventPopup.classList.remove('active');
        console.log('Event pop-up closed.');
    }

    function saveEvent() {
        let eventName = document.getElementById('event-input').value;
        let eventDescription = eventDescriptionInput.value; // Add this line

        // Get other event details like date if available
        console.log('Event name:', eventName);
        console.log('Event description:', eventDescription);

        // Send the event details to the server using AJAX or fetch
        sendEventToServer(eventName, eventDescription); // Modify this line
    }

    function sendEventToServer(eventName, eventDescription) {
        // Use fetch to send the event details to the server
        // For simplicity, I'll use fetch in this example
        fetch('/save_event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ eventName: eventName, eventDescription: eventDescription }), // Modify this line
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response if needed
            console.log('Server response:', data);
        })
        .catch(error => {
            console.error('Error sending event to server:', error);
        });
    }
});
