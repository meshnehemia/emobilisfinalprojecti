let imagedropArea = document.getElementById('imageDropArea');
let imageInput = document.querySelector(`input[name="${'image'}"]`);
let filedropArea = document.getElementById('bookDropArea');
let bookInput = document.querySelector(`input[name="${'book'}"]`);
let selectedImage = '';

function handleFiles(files, type) {
    if (files.length > 0) {
        if (type === 'image') {
            selectedImage = files[0];
            imageInput.files = files;
            imagedropArea.style.backgroundImage = `url('${URL.createObjectURL(selectedImage)}')`;
            if (bookInput.files && bookInput.files.length > 0) {
                filedropArea.style.backgroundImage = `url('${URL.createObjectURL(selectedImage)}')`;
            }
        } else {
            // Check if the selected file is a PDF
            let bookFile = files[0];
            if (bookFile.type !== 'application/pdf') {
                alert('Please upload a PDF file for the book.');
                return;
            }

            bookInput.files = files;
            if (imageInput.files && imageInput.files.length > 0) {
                imagedropArea.style.backgroundImage = `url('${URL.createObjectURL(imageInput.files[0])}')`;
                filedropArea.style.backgroundImage = `url('${URL.createObjectURL(imageInput.files[0])}')`;
            }
        }
    }
}

function setupDropArea(area, file, type) {
    area.addEventListener('dragenter', function (e) {
        e.preventDefault();
        area.classList.add('drag-over');
    });

    area.addEventListener('dragover', function (e) {
        e.preventDefault();
    });

    area.addEventListener('dragleave', function () {
        area.classList.remove('drag-over');
    });

    area.addEventListener('drop', function (e) {
        e.preventDefault();
        area.classList.remove('drag-over');
        let files = e.dataTransfer.files;
        handleFiles(files, type);
    });

    area.addEventListener('click', function () {
        file.click();
    });

    file.addEventListener('change', function () {
        let files = file.files;
        handleFiles(files, type);
    });
}

setupDropArea(imagedropArea, imageInput, 'image');
setupDropArea(filedropArea, bookInput, 'file');

// Add event listener for form submission
document.getElementById('uploadForm').addEventListener('submit', function (e) {
    e.preventDefault();
    let formData = new FormData(this);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/library/uploadfile/', true);
    xhr.upload.onprogress = function (e) {
        if (e.lengthComputable) {
            let percentComplete = (e.loaded / e.total) * 100;
            document.getElementById('fileUploadProgress').value = percentComplete;
        }
    };

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // Successful response
                let jsonResponse = JSON.parse(xhr.responseText);
                if (jsonResponse.success === 'success') {
                    alert("successfully uploaded file");
                    window.location.href = '/library/';
                } else {
                    alert("Failed to upload file: " + jsonResponse.error);
                    window.location.href = '/library/';
                }
            } else {
                // Handle non-200 status (e.g., server error)
                alert("Failed to upload file. Server returned status: " + xhr.status);
                window.location.href = '/library/';
            }
        }
    };

    // Send the form data
    xhr.send(formData);
});
