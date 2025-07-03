document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const moveLeftFast = document.getElementById('moveLeftFast');
    const moveLeftSlow = document.getElementById('moveLeftSlow');
    const moveRightSlow = document.getElementById('moveRightSlow');
    const moveRightFast = document.getElementById('moveRightFast');

    // Start button
    startBtn.addEventListener('click', () => {
        const angle = document.getElementById('angle').value;
        const timeH = document.getElementById('time_h').value;
        const timeM = document.getElementById('time_m').value;
        const moveCount = document.getElementById('move_count').value;
        fetch('/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ angle, time_h: timeH, time_m: timeM, move_count: moveCount })
        }).then(() => pollStatus());
        startBtn.disabled = true;
        stopBtn.disabled = false;
    });

    // Stop button
    stopBtn.addEventListener('click', () => {
        fetch('/stop', { method: 'POST' }).then(() => {
            startBtn.disabled = false;
            stopBtn.disabled = true;
        });
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
                if (data.status === 'running') setTimeout(pollStatus, 1000);
                else {
                    startBtn.disabled = false;
                    stopBtn.disabled = true;
                }
            });
    }
});
