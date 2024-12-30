// take the note Id passed and send a POST request to delete-note endpoint
// once it gets a response from endpoint reload window and refresh the page
function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId})
    }).then((_res) => {
        window.location.href = "/";
    })  
}