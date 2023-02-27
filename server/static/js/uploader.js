function handleDrop(e) {
e.preventDefault();
const files = e.dataTransfer.files;
uploadFiles(files);
}

function handleDragOver(event) {
event.preventDefault();
event.dataTransfer.dropEffect = "copy";
event.target.classList.add("drag-over");
}

function uploadFiles(files) {
const formData = new FormData();
for (let i = 0; i < files.length; i++) {
    formData.append("file", files[i]);
}

const xhr = new XMLHttpRequest();
xhr.open("POST", "/upload", true);
xhr.send(formData);
}