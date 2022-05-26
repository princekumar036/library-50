// Hide flash messages after 1 sec
setTimeout(function() {
    document.querySelector('.flashes').style.heigt = '0';
}, 1000);

// Feedback on fileupload
let file = document.getElementById('file')
file.addEventListener('change', (e) => {
    const [file] = e.target.files
    const {name: fileName, size} = file
    const fileSize = (size / 1000).toFixed(2)
    document.getElementById('file-subtext').innerText = `Uploaded file: ${fileName} (${fileSize})`
})

// Hide flash messages after some time
