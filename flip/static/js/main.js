$(function () {
    var alertOnExit = function () {
        if(!window.onbeforeunload) {
            window.onbeforeunload = function () {
                return "You have unsaved changes. "
            }
        }
    }

    $('[data-toggle=popover]').popover();

    $('[data-edit-form]').on('keyup change', 'input, textarea', function () {
        alertOnExit();
    });
    $('[data-edit-form]').on('click', 'button[type=submit]', function () {
        window.onbeforeunload = null;
    });

    $('#id_foresight_approaches').select2({
        placeholder: "All foresight approaches"
    });
});
