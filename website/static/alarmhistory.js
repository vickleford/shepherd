function discoverHistory(entityid, alarmid) {
    $.ajax({
        url: "/history/" + entityid + "/" + alarmid,
        dataType: "json",
        cache: false,
        success: function(data) {
            var template = $('#discover').html();
            $('#discoverTarget').html(Mustache.to_html(template, data));
        }
    });
}


function listHistory(entityid, alarmid, checkid) {
    $.ajax({
        url: "/history/" + entityid + "/" + alarmid + "/" + checkid,
        dataType: "json",
        cache: false,
        success: function(data) {
            for (var i = 0; i < data['values'].length; i++) {
                ts = data['values'][i]['timestamp']
                data['values'][i]['timestamp'] = new Date(ts).toUTCString();
            }
            var template = $('#historylist').html();
            $('#historylistTarget').html(Mustache.to_html(template, data));
        }
    });
}


function getHistory(entityid, alarmid, checkid, uuid) {
    $.ajax({
        url: "/history/" + entityid + "/" + alarmid + "/" + checkid + "/" + uuid,
        dataType: "json",
        cache: false,
        success: function(data) {
            var template = $('#historydetails').html();
            $('#historydetailsTarget').html(Mustache.to_html(template, data));
        }
    });
}


/* patrick's sort filter 
data.values.sort(function(a, b) {
                    var textA = a.entity.label.toUpperCase();
                    var textB = b.entity.label.toUpperCase();
                    return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
                });
*/