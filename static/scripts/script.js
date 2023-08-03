//Select2

//Style the select-2 input with Bootstrap.
$(document).ready(function() {
    $('#accounts_dropdown').select2({ 
        theme:'bootstrap-5'   
        });
    });

    $("#accounts_dropdown").on("select2:select", function (e) {
        open(e.params.data.id,'_self');
    });

    $('#id_spirit').select2({ 
        theme:'bootstrap-5'   
        });

    $('#id_category').select2({ 
        theme:'bootstrap-5'   
        });