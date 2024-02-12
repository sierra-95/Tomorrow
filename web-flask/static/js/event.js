// In events.js
document.addEventListener('DOMContentLoaded', function () {
    const calendarDays = document.querySelectorAll('.calendar-days div');
    const eventPopup = document.querySelector('.event-popup');
    const closeBtn = document.querySelector('.close-btn');
    const saveBtn = document.getElementById('save-btn'); // Update this line

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
    
    saveBtn.addEventListener('click', function () {
        saveEvent();
        closeEventPopup(); // Close the popup after saving
    });

    function closeEventPopup() {
        eventPopup.classList.remove('active');
    }

    function saveEvent() {
        // Your existing saveEvent logic...
    }
});



//Save button
let saveBtn = document.getElementById('save-btn');

saveBtn.addEventListener('click', function () {
    saveEvent();
    closeEventPopup();
});

function saveEvent() {
    let eventName = document.getElementById('event-input').value;
    // Get other event details like date and description if available

    // Send the event details to the server using AJAX or fetch
    sendEventToServer(eventName);
}

function sendEventToServer(eventName) {
    // Use AJAX or fetch to send the event details to the server
    // For simplicity, I'll use fetch in this example
    fetch('/save_event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ eventName: eventName }),
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response if needed
        console.log('Event saved:', data);
    })
    .catch(error => {
        console.error('Error saving event:', error);
    });
}
