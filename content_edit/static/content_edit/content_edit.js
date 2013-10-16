function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function save_cms_content(e, content_name) {
    var data = $(e).html();
    var csrf_token = getCookie('csrftoken');
    $.post(
        '/content_edit/ajax_save_content/',
        {
            content: data, 
            content_name: content_name,
            csrfmiddlewaretoken: csrf_token
        },
        function(data) {
            if (data == "SUCCESS") {
            }
        }
    );
}

CKEDITOR.disableAutoInline = true;
$( document ).ready(function() {
    editables = $("div[contenteditable='true']");
    $(editables).each( function() {
    CKEDITOR.inline( this, {
        filebrowserUploadUrl: "/ckeditor/upload/",
        filebrowserBrowseUrl: "/ckeditor/browse/"
    } );
    });
    CKEDITOR.disableAutoInline = false;
});
