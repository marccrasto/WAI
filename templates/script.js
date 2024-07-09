const saveFile = async() => {
    let formData = new FormData();
    formData.append("file", fileUpload.files[0]);
    await fetch('/upload.php', {method: "POST", body: formData});
    alert('The file has been uploaded!')
};