document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('lineChart').getContext('2d');

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Productivity status',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                data: [],
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    ticks: {
                        color: 'white', // Set x-axis label color
                    }
                },
                y: {
                    max: 100,
                    min: 0,
                    grid: {
                        color: '#ddd',
                    },
                    ticks: {
                        color: 'white', // Set y-axis label color
                    }
                }
            }
        }
    });

    function generateData() {
        const data = chart.data.datasets[0].data;
        const labels = chart.data.labels;

        const newValue = Math.random() * 100;
        data.push(newValue);
        labels.push(labels.length);

        chart.update();

        // Clear canvas and restart after 20 seconds
        if (labels.length > 20) {
            clearCanvas();
        }
    }
    function clearCanvas() {
        chart.data.labels = [];
        chart.data.datasets[0].data = [];
        chart.update();
    }

    // Update data every second
    setInterval(generateData, 1000);
});
