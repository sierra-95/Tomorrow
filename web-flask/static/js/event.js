document.addEventListener('DOMContentLoaded', function () {
    const calendarDays = document.querySelectorAll('.calendar-days div');
    const eventPopup = document.querySelector('.event-popup');
    const closeBtn = document.querySelector('.close-btn');
    const saveBtn = document.getElementById('save-btn');
    const eventDescriptionInput = document.getElementById('event-description');

    let selectedDate = ''; // Variable to store the selected date

    calendarDays.forEach(day => {
        day.addEventListener('click', () => {
            selectedDate = day.textContent; // Store the selected date
            openEventPopup();
        });
    });

    function openEventPopup() {
        const dateLabel = document.querySelector('.event-popup label');
        dateLabel.textContent = `Event for ${selectedDate}`;
        eventPopup.classList.add('active');
    }

    closeBtn.addEventListener('click', closeEventPopup);

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
        let eventDescription = eventDescriptionInput.value;
    
        // Assuming selectedDate is in the format 'DD', for example, '14'
        let selectedMonth = document.querySelector('#month-picker').textContent;
        let selectedYear = document.querySelector('#year').textContent;
    
        // Construct the full date string in the format 'YYYY-MM-DD'
        let eventDate = `${selectedYear}-${selectedMonth.padStart(2, '0')}-${selectedDate.padStart(2, '0')}`.trim();


    
        console.log('Event name:', eventName);
        console.log('Event description:', eventDescription);
        console.log('Event date:', eventDate);
    
        // Send the event details to the server using AJAX or fetch
        sendEventToServer(eventName, eventDescription, eventDate);
    }
    

    function sendEventToServer(eventName, eventDescription, eventDate) {
        fetch('/save_event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ eventName: eventName, eventDescription: eventDescription, eventDate: eventDate, }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Server response:', data);
            window.location.href = '/dashboard';
        })
        .catch(error => {
            console.error('Error sending event to server:', error);
        });
    }
});
