function decorate_form(type) {
    if (type == 'evaluation') {
        $('[data-show-if=evaluation]').removeClass('hide');
        $('[data-show-if=activity]').addClass('hide');
        $('[data-show-if=type-selected]').removeClass('hide');
    }
    else if (type == 'activity') {
        $('[data-show-if=activity]').removeClass('hide');
        $('[data-show-if=evaluation]').addClass('hide');
        $('[data-show-if=type-selected]').removeClass('hide');
    }
    else {
        $('[data-show-if=type-selected]').addClass('hide');
    }
}

$(function () {
    $('#id_blossom').on('change',function () {
        $('[data-show-if=blossom]')
            .toggleClass('hide', $(this).val() != '1');
    }).change();
    $('#id_start_date').datetimepicker({pickTime: false});
    $('#id_end_date').datetimepicker({pickTime: false});

    var title_original = $('#id_title_original');
    var title = $('#id_title');

    $('#study-languages').on('change', 'select', function () {
        if ($(this).val() == 'en') {
            var title_original = (
                $(this).parents('.row').first().find('input[type=text]')
            );
            var title = $('#id_title');
            if ($.trim(title_original)) {
                title_original.val(title.val());
            }
        }
    });

    var study_languages = $('#study-languages');
    $('#study-languages-add').on('click', function () {
    var max_forms = $('#id_studylanguage_set-MAX_NUM_FORMS').val();
    var nr_forms = study_languages.find('.form-group').length;
    var total_forms = $('#id_studylanguage_set-TOTAL_FORMS');

    if (nr_forms < max_forms) {

        var html = $($('#study-languages-empty-form').html());
        html.find('label').each(function () {
            var attr = $(this).attr('for');
            $(this).attr('for', attr.replace('__prefix__', nr_forms));
        });

        html.find('select, input').each(function () {
            var attr_id = $(this).attr('id');
            var attr_name = $(this).attr('name');
            $(this).attr('id', attr_id.replace('__prefix__', nr_forms));
            $(this).attr('name', attr_name.replace('__prefix__', nr_forms));
        });

        $('#study-languages-add').before(html);
        total_forms.val(parseInt(total_forms.val()) + 1);
    }

    if (nr_forms == (max_forms - 1)) {
        $(this).hide();
    }

    });

    $('#study-languages')
        .on('click', '.language-remove a', function () {

        var total_forms = $('#id_studylanguage_set-TOTAL_FORMS');
        var can_delete = $(this).parents('.language-remove')
            .find('.delete');
        $(this).parents('.form-group').fadeOut('fast', function () {
            $('#study-languages-add').show();
            if (can_delete.length == 0) {
                $(this).remove();
                total_forms.val(parseInt(total_forms.val()) - 1);
            } else {
                can_delete.prop('checked', true);
            }
        });
      });

    $('[name="study_type"]').on('change', function () {
        decorate_form($(this).val());
    }).change();

    $('#id_geographical_scope').on('change', function () {
        var require_country_option = $.inArray(
            $(this).val(), $(this).parent().data('extra')) < 0;
        $('[data-show-if=geographical_scope]').toggleClass(
            'hide', require_country_option);
        if (require_country_option) {
            $('#id_countries option').removeAttr('selected');
        };
    }).change();
});