function fetchanddisplay(url){
    fetch(url)
        .then(response => response.text())
        .then(data => {
            const filecontent = document.getElementById('file-content');
            filecontent.textContent = data;
        })
        .catch(error => {
            console.error('Error fetching file:', error);
            const filecontent = document.getElementById('file-content');
            filecontent.textContent = 'Error loading file content.';
        })
}
fetchanddisplay('examplepy.txt');
