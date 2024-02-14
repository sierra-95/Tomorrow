function startCountdown() {
    var count = 5; // Countdown time in seconds
    var tempMessage = document.getElementById('temp-message');

    function updateMessage() {
        tempMessage.textContent = `You will be logged in in ${count} seconds...`;
        count--;

        if (count < 0) {
            // Redirect to the dashboard after the countdown
            window.location.href = '/dashboard';
        } else {
            setTimeout(updateMessage, 1000);
        }
    }
    updateMessage();
}

window.onload = startCountdown;