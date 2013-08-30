function drawGraph(title, data, start, end) {
    /* 
    
    A picture of the data:
    [ (all metrics chosen)
        [{
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
        }], (line 1 or first metric drawn)
        ...
    ]

    startTime and endTime should come in as Date objects
    */
    startTime = new Date(start);
    endTime = new Date(end);
    var m = [80, 80, 80, 80];
    var w = 850 - m[1] - m[3];
    var h = 450 - m[0] - m[2];
    var t1 = data[0][1].timestamp, t2 = data[0][0].timestamp; // should get all the same windows i hope
    var timeStep = t1 - t2; 
    
    var x = d3.time.scale().domain([startTime, endTime]).range([0, w]);
    x.tickFormat(d3.time.format("%Y-%m-%d"));
    
    //var y = d3.scale.linear().domain([0, d3.max(data, function(d, i) { return d[i].average; })]).range([h, 0]);
    var ymax = d3.max(data, function(d) {
        return d3.max(d, function(dd) {
            return dd.average;
        });
    });
    var y = d3.scale.linear().domain([0, ymax]).range([h, 0]);
    
    
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
        
    for (var n = 0; n < data.length; n++) {
        // add the lines
        graph.append("svg:path")
            .attr("d", line1(data[n]))
            .attr("class", "data" + (n + 1))
            
        // try adding a label
        graph.append("svg:text")
            .attr("x", n * 120)
            .attr("y", h + 30)
            .attr("height", 1)
            .attr("width", 1)
            .attr("class", "data" + (n + 1))
            .text(data[n].metricname);
    }
        

    /*
    // how many points did we show?
    graph.append("svg:text")
        .attr("x", w + 5)
        .attr("y", 12)
        .attr("height", 1)
        .attr("width", 1)
        .attr("fill", "gray")
        .text(data.length + " points"); */
}

function drawPlane() {
    var m = [80, 80, 80, 80];
    var w = 850 - m[1] - m[3];
    var h = 400 - m[0] - m[2];
    
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
    
}

function getMetrics(entityid, checkid, metricname, params) {
    var vals = null;
    $.ajax({
        url: "/metrics/" + entityid + "/" + checkid + "/" + metricname,
        async: false,
        dataType: "json",
        data: params,
        cache: false,
        success: function(data) {
            //drawGraph(metricname, data.values, new Date(params.starttime), new Date(params.endtime));
            vals = data.values;
            vals.metricname = metricname;
        }
    });
    return vals;
}