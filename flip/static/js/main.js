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

    var fixHelper = function(e, ui) {
        ui.children().each(function() {
            $(this).width($(this).width());
        });
        return ui;
    };

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var update = function (e, ui) {
        var data = $(this).sortable('serialize');
        var url = $(this).parents('table').data('url');
        $.post(url, data);
    };

    $('.sortable tbody').sortable({
        handle: ".handler",
        axis: "y",
        placeholder: "ui-state-highlight",
        update: update,
        helper: fixHelper
    });

    $('body').on('click', '.launch-modal', function () {
        var url = $(this).data('action');
        var title = $(this).data('title');
        var message = $(this).data('message');
        $('#modal-submit').show();
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                $('.modal-body').html(data);
                $('h4.modal-title').html(title);
                if (message) {
                    $('#confirmation-msg')[0].innerHTML = message;
                    $('#confirmation-msg').removeClass("hidden");
                }
                $('#modal-submit').data('action', url);
                $('#modal-submit-create').data('action', url);
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
                if (data.indexOf('text-danger') == -1) {
                    $('#modal-submit').hide();
                    $('#modal-submit-create').hide();
                }
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

    $('body').on('click', '#modal-submit-create', function () {
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
                form[0].reset();
                $('#confirmation-msg')[0].innerHTML =
                    "The output was successfully added.";
                $('#confirmation-msg').removeClass("hidden");
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
