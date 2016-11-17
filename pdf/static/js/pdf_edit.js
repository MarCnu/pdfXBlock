/* Javascript for pdfXBlock. */
function pdfXBlockInitEdit(runtime, element) {

    var $element = $(element);

    $(element).find('.action-cancel').bind('click', function () {
        runtime.notify('cancel', {});
    });

    $(element).find('.action-save').bind('click', function () {
        var data = new FormData();

        data.append('usage_id', $element.data('usage-id'));
        data.append('display_name', $element.find('#pdf_edit_display_name').val());
        data.append('display_description', $element.find('pdf_edit_display_description').val());
        data.append('thumbnail', $element.find('input[name=thumbnail]')[0].files[0]);

        runtime.notify('save', {state: 'start'});

        var handlerUrl = runtime.handlerUrl(element, 'save_pdf');
        $.ajax({
            url: handlerUrl,
            type: 'POST',
            data: data,
            cache: false,
            dataType: 'json',
            processData: false,
            contentType: false
        }).done(function (response) {
            if (response.result === 'success') {
                runtime.notify('save', {state: 'end'});
                // Reload the whole page :
                // window.location.reload(false);
            } else {
                runtime.notify('error', {msg: response.message})
            }
        });
    });
}