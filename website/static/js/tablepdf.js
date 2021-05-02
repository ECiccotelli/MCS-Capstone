function getObjectData() {
    console.log('test');
    var object = document.getElementById("pdf_objec");
    object.onload = function() {
        var data = object.contentDocument.body.childNodes[0].innerHTML;
        // use the data
    console.log(data);
};