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
