
openViewRecord = function() {
    objectID = $(this).parent().parent().attr("metadata").trim()
    window.location = viewRecordUrl + '?id=' + objectID ;
};

$(".btn-view-metadata").on('click', openViewRecord);
