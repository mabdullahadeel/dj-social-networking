
$(document).ready(function () {
    console.log("Hello From Main")
    $('#modal-btn').click(function () {
        $('.ui.modal')
            .modal('show');
    });

    $('.ui.dropdown').dropdown()
})