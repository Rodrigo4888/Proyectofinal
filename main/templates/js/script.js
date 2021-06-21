function alCargarDocumento() {
    $("#btnmodal").click(function() {
        console.log("band");
        $("#exampleModalCenter").modal("show");
    });
}
//EVENTOS
window.addEventListener("load", alCargarDocumento);