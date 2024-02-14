function deleteEvent(eventId) {
    fetch(`/delete_event/${eventId}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error deleting event:', error);
    });
}