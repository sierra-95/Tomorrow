const innerCircle = document.querySelector('.inner-oppose');

function updateAcceleration(value) {
    innerCircle.innerHTML = `<span class="acceleration-value">${value}</span>`;
}

// Update acceleration every 1.5 seconds (1500 milliseconds)
let currentAcceleration = 0;

setInterval(() => {
    currentAcceleration = (currentAcceleration + 1) % 101; // Increment acceleration in sequence
    updateAcceleration(currentAcceleration);
}, 1500);

// Initial update
updateAcceleration(currentAcceleration);
