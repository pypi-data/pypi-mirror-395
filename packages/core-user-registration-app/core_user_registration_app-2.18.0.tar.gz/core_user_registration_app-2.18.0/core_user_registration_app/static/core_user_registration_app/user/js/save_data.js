$(document).ready(function(){
    $('.btn.save-to-repo').on('click', saveToRepositoryRegistry);
});


/**
 * Saves the data.
 */
var saveToRepositoryRegistry = function(){
   var objectID = $("#curate_data_structure_id").html();
   var accountID = $("#account_request_id").html();
   $.ajax({
        url : '/save-data',
        type: 'POST',
        data: {
          'id': objectID,
          'metadata' : accountID,
        },
        dataType: 'json',
        success : function(data) {

        window.location = "/";
        },
        error: function(data){
            XMLDataSavedError(data.responseText);
        }
    });
};

var XMLDataSavedError = function(errors)
{
    var $saved_error_modal = $("#save-error-modal");
    $("#saveErrorMessage").html(errors);
    $saved_error_modal.modal("show");
};


var displaySaveForm = function(){
    $("#save-form-registry-modal").modal({
            show: true,
    		backdrop: 'static',
    		keyboard: false
		});
    $(".close").hide();
    $("#save-form-registry-modal").modal("show");
};
