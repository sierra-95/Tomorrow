function updateTaskState(eventId) {
    fetch(`/update_task_state/${eventId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            isDone: document.getElementById(`myCheckbox${eventId}`).checked,
        }),
    })
    .then(response => {
        if (response.ok) {
            console.log('Task state updated successfully.');
        } else {
            console.error('Error updating task state.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
