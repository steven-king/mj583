function initDots(config) {
    // Create a color scale that we can pull colors from.
    // https://github.com/d3/d3-scale-chromatic
    var colorScale = d3.scaleOrdinal(d3.schemeCategory10);
    
    // Grab our root container
    var svgContainer = d3.select("#nobel-dot");

    // Create an object to export our methods on the config
    config.dots = {};

    // Start building our svg bar chart
    var svg = svgContainer.append("svg");
    var chart = svg.append("g");

    // Configure our SVG element to be the full width and 200px tall
    svg.attr('width', '100%')
        .attr('height', 200);
    
    // Get the width and height of the element containing our svg element
    var boundingRect = svgContainer.node().getBoundingClientRect();
    
    // Add margins so there is room to draw our axis
    var margin = {'left': 0, 'right': 0, 'top': 10, 'bottom': 40};

    // Hang on to the width and height values to use when generating the graph
    var width = boundingRect.width - (margin.left + margin.right);
    var height = boundingRect.height - (margin.top + margin.bottom);

    // Position the chart with the margin accounted for
    chart.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    // Render re-renders the bar chart
    config.dots.render = function () {
        // Reset the chart
        chart.selectAll("g").remove();
        
        // Create a graph group
        var graph = chart.append("g");

        // Year data
        var maxYear = 2014 // d3.max(config.data.winners.map(function(d) {return d.year}));
        var minYear = 1901 // d3.min(config.data.winners.map(function(d) {return d.year}));

        // Create a year scale
        var yearScale = d3.scaleBand()
            .domain(d3.range(minYear - 1, maxYear + 1))
            .range([0, width])
            .paddingInner(0.2);
        
        // Create the X axis from the year scale
        var xAxis = d3.axisBottom(yearScale)
            .tickValues(
                yearScale.domain().filter(function (v) {
                    return (v % 10 === 0)
                })
            )
            .tickSizeOuter(0); // This removes the ending tick marks

        // Add the X axis
        graph.append('g')
            .classed("x axis", true)
            .call(xAxis)
            .attr("transform", "translate(0, " + height + " )")
            .selectAll("text")
            .attr('transform', 'rotate(-90)')
            .style('text-anchor', 'end')
            .attr('dx', '-.95em')
            .attr('dy', '-.55em');

        // Grab the bandwidth and divide it for the circle radius
        var bandwidth = Math.min(yearScale.bandwidth(), 15);
        var circleSize = bandwidth / 2;

        // Find categories from the dataset
        var cats = [];
        var catsSet = {};
        config.data.winners.forEach(function (d) {
            var c = catsSet[d.category]
            if (c === undefined) {
                cats.push(d.category);
                catsSet[d.category] = true;
            }
        });

        // Draw the legend
        // Add a group to contain all the labels
        var legend = graph.append("g")
            .classed("legend", true)
            .attr("transform", "translate(10,0)");
        
        // Add groups to put the circles and text within
        var labels = legend.selectAll("g")
            .data(cats)
            .enter()
            .append("g")
            .attr("transform", function (d, i) {
                var yval = i * bandwidth;
                if (i > 0) {
                    yval = yval + (5 * i);
                }
                return "translate(0," + yval + ")"
            });

        // Append a circle to each label with a matching color
        labels.append("circle")
            .attr("r", circleSize)
            .style("fill", function (d) {
                return colorScale(d);
            });
        
        // Append the text of each category and postion it
        labels.append("text")
            .text(function (d) {return d})
            .attr("dx", ".4em")
            .attr("dy", ".4em")
            .style("font-size", ".8em");

        // Create a group for all the dots
        var dots = graph.append("g")
            .classed("dots", true);
        
        // Keep track of the number of dots (categories) seen in each year
        var yearsSeen = {};
        
        // Draw a dot for each category of winner for each year
        dots.selectAll("circle")
            .data(config.data.winners)
            .enter()
            .append("circle")
            .attr("r", circleSize)
            .attr("transform", function (d) {
                // Move the dot along the X axis based on the year
                var xval = yearScale(d.year) || 0;
                // Look up the number of times we've seen categories for this year
                var yrCnt = yearsSeen[d.year] || 0;
                // Move the dot away from the axis by the amount we've seen
                var yval = height - (yrCnt * bandwidth);
                // Increment and track that we've seen another category for this year
                yrCnt++;
                yearsSeen[d.year] = yrCnt;
                // Return the translate value
                return "translate(" + xval + "," + yval + ")"
            })
            .attr("cx", circleSize)  // offset for circles positioned in the center
            .attr("cy", (circleSize * -1) - 5)  // inverted y offset with padding
            .style("fill", function (d) {
                return colorScale(d.category);
            });
    }
}