function drawGraph(data, startTime, endTime) {
    /* 
    
    A picture of the data:
    [
        {
          "average": 339857, 
          "numPoints": 5, 
          "timestamp": 1377493200000
        }, 
        {
          "average": 339857, 
          "numPoints": 5, 
          "timestamp": 1377493500000
        }, 
        {
          "average": 339857, 
          "numPoints": 5, 
          "timestamp": 1377493800000
        }
    ]
    
    startTime and endTime should come in as Date objects
    */
    var m = [80, 80, 80, 80];
    var w = 850 - m[1] - m[3];
    var h = 400 - m[0] - m[2];
    var timeStep = data[1].timestamp - data[0].timestamp;
    //var timeStep = 300000; // calculate this from data later.
    
    var x = d3.time.scale().domain([startTime, endTime]).range([0, w]);
    x.tickFormat(d3.time.format("%Y-%m-%d"));
    
    var y = d3.scale.linear().domain([0, d3.max(data, function(d) { return d.average; })]).range([h, 0]);
    
    
    // create a line function that can convert data[] into x and y points
    var line1 = d3.svg.line()
        .x(function(d,i) { return x(startTime.getTime() + (timeStep*i)); }) // this looks a little suspect
        .y(function(d) { return y(d.average); });
        
    // add an svg element with desired dimensions and margin
    var graph = d3.select("#graph")
        .append("svg:svg")
            .attr("width", w + m[1] + m[3])
            .attr("height", h + m[0] + m[2])
        .append("svg:g")
            .attr("transform", "translate(" + m[3] + "," + m[0] + ")");
            
    // create x axis
    var xAxis = d3.svg.axis().scale(x).tickSize(-h).tickSubdivide(1);
    
    // add the x axis
    graph.append("svg:g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + h + ")")
        .call(xAxis);
        
    // create y axis
    var yAxisLeft = d3.svg.axis().scale(y).ticks(6).orient("left");
    
    // add y axis
    graph.append("svg:g")
        .attr("class", "y axis")
        .attr("transform", "translate(-10, 0)")
        .call(yAxisLeft);
        
    // add the line bro
    graph.append("svg:path")
        .attr("d", line1(data))
        .attr("class", "data1");
}

function getMetrics(entityid, checkid, metricname, params) {
    $.ajax({
        url: "/metrics/" + entityid + "/" + checkid + "/" + metricname,
        dataType: "json",
        data: params,
        cache: false,
        success: function(data) {
            /*var template = $('#rawmetrics').html();
            $('#rawmetricsTarget').html(Mustache.to_html(template, data));*/
            drawGraph(data.values, new Date(params.starttime), new Date(params.endtime));
        }
    });   
}