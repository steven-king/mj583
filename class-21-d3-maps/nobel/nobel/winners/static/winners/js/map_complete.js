// initMap handles setting up our map
function initMap(config) {
    var mapContainer = d3.select('#nobel-map');
    var svg = mapContainer.append('svg');
    var proj = d3.geoEquirectangular(); // or d3.geoMercator();

    svg.attr("width", "100%");
    svg.attr("height", 600);

    var boundingRect = mapContainer.node().getBoundingClientRect();
    var width = boundingRect.width,
        height = boundingRect.height;



        // Adjust projection to fill width / height of the container div
  proj.translate([width / 2, height / 2])
      .scale(width / (2 * Math.PI));

  // Add graticule lines via a path generator
  var pathGenerator = d3.geoPath()
      .projection(proj);

  var graticule = d3.geoGraticule()
      .step([10, 10]);

  var lines = svg.selectAll('path.graticule')
      .data([graticule()])
      .enter()
      .append('path')
      .classed('graticule', true)
      .attr('d', pathGenerator);

      

    d3.json("/static/winners/data/world-110m.json").then(function (world){
        var obj = topojson.feature(world, world.objects.countries);
        var countries = obj.features;
        window.mapCountries = countries;
        proj.fitSize([width, height], obj);
        svg.append("path")
            .datum(obj)
            .attr("d", d3.geoPath().projection(proj));
        config.mapReady = true;
        config.render();
    });

    function getProjPoint(d) {
        if (d.name === 'United States') {
            return proj(["-98.585522", "39.8333333"])
        }
        return proj([d.lng, d.lat])
    }

    config.render = function () {
        if (!config.data) return
        svg.selectAll("circle").remove();
        var circle = svg.selectAll("circle").data(config.data.countries);

        circle.enter()
            .append("circle")
            .attr("cx", function(d) {return getProjPoint(d)[0]})
            .attr("cy", function(d) {return getProjPoint(d)[1]})
            .attr("r", function(d) {return Math.max(3, Math.min(d.winners * 1, 30))})
            .attr('fill-opacity', 0.6);
    }
}
