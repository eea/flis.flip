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

    $('body').on('click', '.launch-modal', function () {
        var url = $(this).data('action');
        var title = $(this).data('title');
        $('#modal-submit').show();
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                $('.modal-body').html(data);
                $('h4.modal-title').html(title)
                $('#modal-submit').data('action', url)
            },
            error: function (data) {
                alert('Error launching the modal')
            }
        })
    });

    $('body').on('click', '#modal-submit', function () {
        var form = $('#study-modal-form');
        var url = $(this).data('action');
        var outcomes_url = $('#outcomes').attr('outcomes-url');
        var formdata = false;
        if (window.FormData){
            formdata = new FormData(form[0]);
        }
        $.ajax({
            type: "POST",
            url: url,
            data: formdata ? formdata : form.serialize(),
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                $('.modal-body').html(data);
                if (data.indexOf('text-danger') == -1)
                    $('#modal-submit').hide();
                $.ajax({
                    type: "GET",
                    url: outcomes_url,
                    success: function(data) {
                        $('#outcomes').html(data);
                    }
                })
            },
            error: function (data) {
                alert('Error saving the data')
            }
        });
    });

});
