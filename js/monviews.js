function getCookie(name) {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        cookie = cookies[i].split('=');
        thisName = cookie[0];
        thisValue = cookie[1];
        if (thisName.substring(0, 1) == ' ') {
            thisName = thisName.substring(1, thisName.length);
        }
        if (name == thisName) {
            return thisValue
        }
    }
    // nothing found
    return null
}


function loadOverview() {
    // http://docs.rackspace.com/cm/api/v1.0/cm-devguide/content/service-views.html
    
    $.ajax({
        url: getCookie('maasEndpoint') + "/views/overview",
        dataType: "json",
        cache: false,
        headers: { "X-Auth-Token": getCookie('authToken') },
        success: function(data) {
            data.values.sort(function(a, b) {
                                var textA = a.entity.label.toUpperCase();
                                var textB = b.entity.label.toUpperCase();
                                return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
                            });

            var template = $('#entries').html();
            $('#table').html(Mustache.to_html(template, data.values));
        },
        statusCode: {
            401: function() {
                alert("token not valid");
            }            
        }
    });
}


function getAuthToken(username, password) {
    // http://docs.rackspace.com/auth/api/v2.0/auth-client-devguide/content/POST_authenticate_v2.0_tokens_.html
    var globalAuthUrl = 'https://identity.api.rackspacecloud.com/v2.0';
    
    $.ajax({
        type: "POST",
        url: globalAuthUrl + "/tokens",
        dataType: "json",
        cache: false,
        contentType: "application/json",
        data: { "auth": { "passwordCredentials": { "username": username, "password": password } } },
        success: function(data) {
            // http://www.w3schools.com/js/js_cookies.asp
            var exdate = new Date();
            exdate.setDate(exdate.getDate() + 1);
            document.cookie = "authToken=" + data.access.token.id + "; expires=" + exdate.toUTCString();
            
            // parse the damn service catalog -_-
            /*for (var e in data.access.serviceCatalog) {
                if (data.access.serviceCatalog[e].name == "cloudMonitoring") {
                    document.cookie = "maasEndpoint=" + data.access.serviceCatalog[e].endpoints[0].publicURL;
                }
            }*/
        },
        statusCode: {
            401: function() {
                alert("not valid");
            }            
        },
        error: function(jqXHR, textStatus, errorThrown) { 
            alert(textStatus + ": " + errorThrown);
        }
    });   
}