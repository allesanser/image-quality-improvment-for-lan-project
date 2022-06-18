let video = document.querySelector("#videoElement");
let inputFile = document.querySelector("#upload-file");
let submitButton = document.querySelector("#submit-file");
let inputFileText = document.querySelector('#upload-file-text');
let inputFileButton = document.querySelector('#upload-file-button');

inputFile.addEventListener("change", uploadFile, false);
submitButton.addEventListener("click", processingFile, false);
inputFileButton.addEventListener("mouseover", function() {
    if (inputFileButton.className === 'selected-file') inputFileText.textContent = 'Изменить файл'}, false);
inputFileButton.addEventListener("mouseout", function() {
    if (inputFileButton.className === 'selected-file') inputFileText.textContent = 'Файл выбран'}, false);

function uploadFile(e) {
    if (this.files && this.files.length === 1) {
        submitButton.className = 'active';
        submitButton.disabled = false;
        document.querySelector('#upload-file-text').textContent = 'Файл выбран';
        document.querySelector('#upload-file-button').className ='selected-file';
    } else {
        submitButton.className = 'inactive';
        submitButton.disabled = true;
        document.querySelector('#upload-file-text').textContent = 'Выбрать файл';
        document.querySelector('#upload-file-button').className = 'unselected-file';
    }
}

function processingFile(e) {
    submitButton.className = 'inactive';
    submitButton.value = 'Обработка';
    document.querySelector('#upload-file-text').textContent = 'Выбрать файл';
    document.querySelector('#upload-file-button').className = 'unselected-file';
}