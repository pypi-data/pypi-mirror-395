$(document).ready(function(){
    if (username != "" ){
    getUsername(username);
    }
    if (email != "" ){
    getEmail(email);
    }
});

/**
Put the value of title into the resourceName field
@param dataElements jquery_selector of the resourceName
**/
var getUsername = function(dataElements) {
    resourceName = $(dataElements)
    resourceName = $(resourceName.children().filter(":input"))
    title = $("#data_username").html();
    resourceName.val(title.trim());
    saveElement(resourceName);
};

var getEmail = function(dataElements) {
    resourceName = $(dataElements)
    resourceName = $(resourceName.children().filter(":input"))
    title = $("#data_email").html();
    resourceName.val(title.trim());
    saveElement(resourceName);
};
