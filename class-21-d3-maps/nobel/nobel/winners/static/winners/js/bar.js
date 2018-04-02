function initBar(config) {
    var svgContainer = d3.select("#nobel-bar");

    // Create an object to export our methods on the config
    config.bar = {};

    // Start building our svg bar chart
    var svg = svgContainer.append("svg");
    var chart = svg.append("g");

    // Render re-renders the bar chart
    config.bar.render = function () {

    }
}
