document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const moveLeftFast = document.getElementById('moveLeftFast');
    const moveLeftSlow = document.getElementById('moveLeftSlow');
    const moveRightSlow = document.getElementById('moveRightSlow');
    const moveRightFast = document.getElementById('moveRightFast');
    pollStatus();

    // Start button
    startBtn.addEventListener('click', () => {
        const angle = parseInt(document.getElementById('angle').value);
        const timeH = parseInt(document.getElementById('time_h').value);
        const timeM = parseInt(document.getElementById('time_m').value);
        const moveCount = parseInt(document.getElementById('move_count').value);
        const totalTimeMinutes = (timeH * 60 + timeM) * moveCount;
        const rotationSpeed = totalTimeMinutes > 0 ? (Math.abs(angle) * moveCount) / totalTimeMinutes : 0;

        if (minRotationSpeed <= rotationSpeed && rotationSpeed <= maxRotationSpeed) {
            if (confirm('Would you like to start the operation?')) {
                fetch('/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ angle, time_h: timeH, time_m: timeM, move_count: moveCount })
                }).then(() => pollStatus());
                startBtn.disabled = true;
                stopBtn.disabled = false;
            }
        } else {
            alert(`Rotation speed is out of the allowable range.\nMax rotation speed: ${maxRotationSpeed} degree/min\nMin rotation speed: ${minRotationSpeed} degree/min\nRotation speed: ${rotationSpeed.toFixed(2)} degree/min`);
        }
    });

    // Stop button
    stopBtn.addEventListener('click', () => {
        if (confirm('Would you like to stop the operation?')) {
            fetch('/stop', { method: 'POST' }).then(() => pollStatus());
        }
    });

    // Position adjust buttons
    [moveLeftFast, moveLeftSlow, moveRightSlow, moveRightFast].forEach(btn => {
        btn.addEventListener('mousedown', () => {
            const speed = btn === moveLeftFast || btn === moveRightFast ? 'fast' : 'slow';
            const direction = btn.id.includes('Left') ? 'L' : 'R';
            fetch('/move_start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ speed, direction })
            });
        });
        btn.addEventListener('mouseup', () => fetch('/move_stop', { method: 'POST' }));
        btn.addEventListener('touchstart', (e) => {
            e.preventDefault();
            const speed = btn === moveLeftFast || btn === moveRightFast ? 'fast' : 'slow';
            const direction = btn.id.includes('Left') ? 'L' : 'R';
            fetch('/move_start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ speed, direction })
            });
        });
        btn.addEventListener('touchend', () => fetch('/move_stop', { method: 'POST' }));
    });

    // Polling
    function pollStatus() {
        fetch('/status')
            .then(response => response.json())
            .then(data => {
                document.getElementById('started').textContent = data.started || '-';
                document.getElementById('finish').textContent = data.finish || '-';
                document.getElementById('progress_angle').textContent = data.progress_angle || '-';
                document.getElementById('progress_angle_bar').value = data.progress_angle_percent || 0;
                document.getElementById('progress_count').textContent = data.progress_count || '-';
                document.getElementById('progress_count_bar').value = data.progress_count_percent || 0;
                document.getElementById('status').textContent = data.status.toUpperCase() || '-';
                if (data.status === 'running') {
                    startBtn.disabled = true;
                    stopBtn.disabled = false;
                } else {
                    startBtn.disabled = false;
                    stopBtn.disabled = true;
                }
                setTimeout(pollStatus, 1000);
            });
    }
});