function getMetrics(entityid, checkid, metricname, params) {
    $.ajax({
        url: "/metrics/" + entityid + "/" + checkid + "/" + metricname,
        dataType: "json",
        data: params,
        cache: false,
        success: function(data) {
            var template = $('#rawmetrics').html();
            $('#rawmetricsTarget').html(Mustache.to_html(template, data));
        }
    });   
}