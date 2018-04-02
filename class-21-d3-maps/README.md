## D3.js Maps and Django

This picks up with where we left off with the bar chart and assumes the API is working correctly.

1. To test you API:

Run the server:
```
docker run -v $PWD:/opt/project -it -p 8000:8000 nobel-app ./env/bin/python3 nobel/manage.py runserver 0.0.0.0:8000

```
Go to this url and you should see this output:
http://localhost:8000/api/?category=Literature&country=Mexico



### Create a map of winning countries
2. In order to create a map view to display data we need to draw the countries. The easiest way to do that is using a TopoJSON file containing the shapes / paths of the country borders.

Got to: https://github.com/topojson/topojson and https://github.com/topojson/world-atlas

Copy the script tag for topojson.
Per the instructions at https://github.com/topojson/topojson we will include the source in our base template.

```html
<script src="https://unpkg.com/topojson@3"></script>

```
The library itself doesn't provide any data. To draw the paths we need a JSON file with all the information so we will download the TopoJSON for the world atlas from https://github.com/topojson/world-atlas

```
curl -o world-110m.json https://unpkg.com/world-atlas@1.1.4/world/110m.json
mkdir -p nobel/nobel/winners/static/winners/data
mv world-110m.json nobel/nobel/winners/static/winners/data/world-110m.json
```

3. With the data in place for the map we can now start fleshing out our map by loading the world-110m JSON and displaying it using D3. We call our map init function from our home JS and add a call to render just like we did with the bar chart.

```javaScript
//map.js

// Add our map namespace object to the config with a bool to mark whether
    // the map data has been loaded
    config.map = {loaded: false};

    var svgContainer = d3.select("#nobel-map");

    // Start building our svg map
    var proj = d3.geoEquirectangular();
    var svg = svgContainer.append("svg");
    var chart = svg.append("g");

    // Configure our SVG element to be the full width and 200px tall
    svg.attr('width', '100%')
        .attr('height', 400);

    // Get the width and height of the element containing our svg element
    var boundingRect = svgContainer.node().getBoundingClientRect();

    // Hang on to the width and height values to use when generating the map
    var width = boundingRect.width;
    var height = boundingRect.height;

    // Load the topojson
    d3.json("/static/winners/data/world-110m.json").then(function (jsonData){
        var world = topojson.feature(jsonData, jsonData.objects.countries);
        proj.fitSize([width, height], world);
        svg.append("path")
            .datum(world)
            .attr("d", d3.geoPath().projection(proj));
        config.map.loaded = true;
        config.map.render();
    });


    // Add a render method back to the config object
    config.map.render = function() {
        // If the map isn't loaded return early
        if (!config.map.loaded) return
    }
}

```

4. Make sure you call the map.js in the init function of home.js
```javaScript
//home.js around line 41 below init bar
// Initalize map
    initMap(window.winners);
```

5. Our map isn't very interesting or detailed since it is only showing the land masses and ocean in black and white. With some simple CSS we can color the background blue and the land off-white and make it look more like the maps we're used to seeing.

```CSS
#nobel-map{
  background: lightblue;
}

#nobel-map path {
    stroke: gray;
    stroke-width: 1px;
    fill: white;

}

```

6. Maps also have graticules which are the lines representing the meridians and parallels. D3 makes it easy to add graticules using a path generator tied to the projection we're using (which is how it's drawing the country border paths as well). All this is handled under the hood we just need to adjust our projections scale and translate it so it is centered in our container correctly.

```javaScript
//map.js above the topojson around line 24


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

```

We also need to make sure the css is added to the template.
Be sure to include static

```html
<!-- base.html -->
{% load static %}

...

<link rel="stylesheet" href="{% static "winners/css/map.css" %}">
```

7. The map isn't useful in-and-of itself so let's begin adding data to our map. We will start by adding a point to the map for each country represented in our resulting dataset in the render function.

```javaScript

//replace lines 54-57 on map.js

// Helper function to turn lat/lng into a point in x/y coords
   function getProjPoint(data) {
       return proj([data.lng, data.lat])
   }

// Add a render method back to the config object
  config.map.render = function() {
      // If the map isn't loaded or we don't have data return early
      if (!config.map.loaded || !config.data) return

      var data = config.data

      // Add circles to the map for winning countries
      svg.selectAll("circle").remove();
      var circle = svg.selectAll("circle").data(config.data.countries);

      circle.enter()
          .append("circle")
          .attr("r", 5) // radius of 5px
          .attr("cx", function(d) {return getProjPoint(d)[0]}) // x position from our projection point
          .attr("cy", function(d) {return getProjPoint(d)[1]}); // y position from our projection point
  }
}


```

8. Once again it's not very visually appealling so we will scale the the dots based on the number of winners in the country. We'll also adjust the transparency so overlappig circles are visible. The color and transparency can be set using CSS.

```CSS
...
#nobel-map circle.winners {
    fill: crimson;
    fill-opacity: .6;
}

```

```javaScript
// replace the svg circle size around line 67 and 68

svg.selectAll("circle.winners").remove();
       var circle = svg.selectAll("circle.winners").data(config.data.countries);

       // Create a scale of winner counts so that our map shows consistent
       // circle sizes for the country with the most results and the country
       // with the least results.
       // Get an array of all the winner counts
       var winnerCounts = data.countries.map(function (d) {return d.winners});
       // Get the largest value from the counts
       var maxWinner = d3.max(winnerCounts);
       // Create a linear scale using the smallest and largest values
       // mapping them to values from 3-30 (the pixel ranges for our circle radius)
       var winnerScale = d3.scaleLinear()
           .domain([0, maxWinner])
           .range([3, 30]);

...


// update circle. enter to this:
circle.enter()
            .append("circle")
            .classed("winners", true)
            .attr("r", function(d) {return winnerScale(d.winners)}) // dynamic radius from winner count scale
            .attr("cx", function(d) {return getProjPoint(d)[0]}) // x position from our projection point
            .attr("cy", function(d) {return getProjPoint(d)[1]}); // y position from our projection point


```
