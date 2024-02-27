        let stopwatch = document.getElementById('stopwatch');
        let seconds = 0;
        let minutes = 0;
        let hours = 0;
        let stopwatchInterval;

        function updateStopwatch() {
            seconds++;

            if (seconds === 60) {
                seconds = 0;
                minutes++;

                if (minutes === 60) {
                    minutes = 0;
                    hours++;
                }
            }

            stopwatch.textContent = `${hours < 10 ? '0' + hours : hours}:${minutes < 10 ? '0' + minutes : minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
        }

        function startStopwatch() {
            stopwatchInterval = setInterval(updateStopwatch, 1000);
        }

        function stopStopwatch() {
            clearInterval(stopwatchInterval);
        }

        function resetStopwatch() {
            clearInterval(stopwatchInterval);
            seconds = 0;
            minutes = 0;
            hours = 0;
            stopwatch.textContent = '00:00:00';
        }