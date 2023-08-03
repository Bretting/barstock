//Select2
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


    