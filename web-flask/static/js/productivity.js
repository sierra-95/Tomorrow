function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function updateScales() {
    const scales = ['TaskCompletionRate', 'TimeManagement', 'TaskResponseTime', 'ProductivitySummary'];

    scales.forEach(scaleId => {
        const scaleElement = document.getElementById(scaleId);
        const valuesElement = document.getElementById(`${scaleId}Values`);
        const randomValue = getRandomInt(0, 100);
        valuesElement.innerHTML = `<p>${randomValue}%</p>`;
    });
}

updateScales();
setInterval(updateScales, 10000);