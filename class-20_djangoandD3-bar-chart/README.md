## Getting the API ready

1. Run the dev server to make sure everything is working. (note the port flag used in the docker run command):

```
docker run -v $PWD:/opt/project -it -p 8000:8000 nobel-app ./env/bin/python3 nobel/manage.py runserver 0.0.0.0:8000
```

--------------------------------------------------------------------------------


2. Download the country data from the example repo

```
curl https://raw.githubusercontent.com/Kyrand/dataviz-with-python-and-js/master/nobel_viz/static/data/winning_country_data.json > country_data.json
curl https://raw.githubusercontent.com/Kyrand/dataviz-with-python-and-js/master/nobel_viz/static/data/world-country-names-nobel.csv > country_ids.csv
```

3. Add new fields to our country model based on the data we gathered:

```python
#inside the country model of models.py
alpha_code = models.CharField(max_length=3, blank=True, null=True)
numeric_code = models.CharField(max_length=3, blank=True, null=True)
lat = models.CharField(max_length=10, blank=True, null=True)
lng = models.CharField(max_length=10, blank=True, null=True)
```

3. Create migrations:
This will add the models and keep the old data.

```
docker run --rm -v $PWD:/opt/project -it nobel-app ./env/bin/python3 nobel/manage.py makemigrations winners
```

Migrate

```
docker run --rm -v $PWD:/opt/project -it nobel-app ./env/bin/python3 nobel/manage.py migrate
```

4. Add a management command to load our data and update our countries. I have created this file but we need to walk through it to understand it. Open

``` nobel/nobel/winners/managment/commands/add_country_data
```
4.1 Import the python Django modules

```python
import csv
import datetime
from decimal import Decimal
import json

from django.core.management.base import BaseCommand, CommandError
from nobel.winners.models import Country

```

4.2 Needs to take two arguments for two files.
```python
class Command(BaseCommand):
    help = 'Load country data'

    def add_arguments(self, parser):
        parser.add_argument('country_data_json', type=str)
        parser.add_argument('country_id_csv', type=str)

```

4.3 Load the data from the input ( add below but inside the class)
```python
def handle(self, *args, **options):
      json_path = options['country_data_json']
      csv_path = options['country_id_csv']

      csvreader = csv.reader(open(csv_path, encoding="utf-8"))
      # Cut off the header the make a list of id / name pairs
      country_ids = list(csvreader)[1:]

      # Convert to dictionary by name
      country_ids = {x[1]: x[0] for x in country_ids}

      by_country = json.load(open(json_path, encoding="utf-8"))

```

4.4 Loop through the data, save to database and send into to terminal.
```python
for c in Country.objects.all():
        data = by_country.get(c.name)
        cid = country_ids.get(c.name)
        if not data:
            self.stderr.write(self.style.ERROR("Could not find data for {}".format(c.name)))
            continue

        if not cid:
            self.stderr.write(self.style.ERROR("Could not find id for {}".format(c.name)))
            continue

        c.alpha_code = data["alpha3Code"]  # AFG
        c.numeric_code = '{:03d}'.format(int(cid))  # "4" -> "004"
        c.lat = str(Decimal(data["latlng"][0]))[:10]
        c.lng = str(Decimal(data["latlng"][1]))[:10]
        c.save()
        self.stdout.write(self.style.SUCCESS("Added data for {}".format(c.name)))


```

5. Run it using:

```
docker run --rm -v $PWD:/opt/project -it nobel-app ./env/bin/python3 nobel/manage.py add_country_data country_data.json country_ids.csv
```

6. Update our country model to have a to_json method and update our API view to
return the full country data in place of the name.

Old output:

```
{
  "winners": [
    {
      "gender": "male",
      "year": 1984,
      "name": "César Milstein",
      "country": "Argentina",
      "category": "Physiology or Medicine"
    },
```

New output:

```
{
  "winners": [
    {
      "name": "César Milstein",
      "country": {
        "name": "Argentina",
        "lat": "-34",
        "lng": "-64",
        "alpha_code": "ARG",
        "numeric_code": "032"
      },
      "category": "Physiology or Medicine",
      "year": 1984,
      "gender": "male"
    },
```

7. Now we have the data we need to build our graphs.

For our bar graph we want to display the country's alpha code under a bar that
represents the count of winners. For this we first need to get the data out of
the database that will count the number of winners per country.

8. Add a new query to our API view using annotations so our result set returns a
new additional object under the key `countries` with a `winners` property
in the format:

```
{
    {
    "winners": [
        ...
    ],
    "countries": [
        {
            "name": "Argentina",
            "lat": "-34",
            "lng": "-64",
            "alpha_code": "ARG",
            "numeric_code": "032",
            "winners": 10
        },
    ]
}
```

9. See comments on the ``` nobble/noebel/winners/views.py ```

## Now, D3!

Now we can start working on our bar chart!

10.Add a container for the chart to the home page:

```html
<div class="row">
    <div class="col-12">
        <div id="nobel-bar"></div>
    </div>
</div>
```

11. And add and include a new js file for our bar graph code.
```html
{% block script %}
    <script src="{% static "winners/js/bar.js" %}"></script>
    <script src="{% static "winners/js/home.js" %}"></script>
{% endblock %}

```


12. Add the d3.js source to our base template.
```html
  <script src="https://d3js.org/d3.v5.min.js"></script>
```

13. Add an init function to bar.js and call it when our home.js loads up.


```html
function initBar(config) {
    var svgContainer = d3.select("#nobel-bar");

    // Create an object to export our methods on the config
    config.bar = {};

```


```javaScript
// Global container for our winner data
window.winners = {
  params: {}
};

```

14. Also stub out a render function on the global config in a namespace object
and call it whenever our data updates.
```javaScript
//static/winners/js/home.js
function fetchData() {
    $.get("/api/?" + $.param(window.winners.params))
        .done(function(data) {
            $('#raw-json').text(JSON.stringify(data, null, '  '));
            // Add data to global container
            window.winners.data = data;
            // Re-render the bar chart
            window.winners.bar.render();
        })
        .fail(function(){
            console.log("Could not load data");
            alert("Could not load data");
        });
}
```

15. Update the bar js to scale to the width of the containing element and get our
country data sorted and ready to use to make a graph. Also, make sure the HTML is ready to receive the graph.
```javaScript
//static/winners/js/bar.js
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
```

```html
<!-- templates/winners/home.html -->
 <div id="nobel-bar"></div>
```

16. Create arrays of country names and country winner counts to use for our scales.


Some basic SVG stuff we need to draw.
```javaScript
//static/winners/js/bar.js
////### after line 9, var chart = svg.append("g");

// Configure our SVG element to be the full width and 200px tall
  svg.attr('width', '100%')
      .attr('height', 200);

  // Get the width and height of the element containing our svg element
  var boundingRect = svgContainer.node().getBoundingClientRect();

  // Hang on to the width and height values to use when generating the graph
  var width = boundingRect.width;
  var height = boundingRect.height;
```

```javaScript
  //static/winners/js/bar.js
  ////### update the re-redner function

  // Render re-renders the bar chart
    config.bar.render = function () {
        // Get the updated countries data sorted by the number of winners
        var countries = config.data.countries.sort(function(a, b) {
            return d3.descending(a.winners, b.winners);
        });

        console.log(countries);
    }
```
See comments on file for details.
```javaScript
///### replace the console.log(countries) line with below.

// Create lists of country names and the winner counts so we can generate
       // d3 scales from the data.
       // We'll use the country names to create a band scale and the winner
       // counts to create a linear band.
       // https://github.com/d3/d3-scale
       // https://github.com/d3/d3-scale#band-scales
       // https://github.com/d3/d3-scale#linear-scales
       var cnames = countries.map(function(x) {return x.name});
       var winners = countries.map(function(x) {return x.winners});

       // Create our country name scale
       var nameScale = d3.scaleBand() // band scale
           .domain(cnames)            // of country names
           .range([0, width])         // ranging from 0 to the width of our container
           .paddingInner(0.1);        // with padding between the bands

       // Get the highest value from the winners data
       var maxWinner = d3.max(winners);

       // Create our winner count scale
       var winnerScale = d3.scaleLinear() // linear scale
           .domain([0, maxWinner])        // of a domain
           .range([height, 0])            // ranging from the height down to 0
           .nice();                       // rounding to a nice even number

       // Get the width of the bands from the scale
       var bandwidth = nameScale.bandwidth();

       // Remove the graph if it exists
       chart.selectAll("g").remove();

       // Create a group to hold our graph
       var graph = chart.append("g");

       // Create a group for our bars
       var bars = graph.append("g")
           .classed("bars", true);

       // Draw the bars
       bars.selectAll('rect.bar')
           .data(countries)
           .enter()
           .append('rect')
           .classed('bar', true)
           .attr('width', bandwidth)
           .attr('height', function(d) {
               return height - winnerScale(d.winners);
           })
           .attr('x', function(d) {
               return nameScale(d.name);
           })
           .attr('y', function(d) {
               return winnerScale(d.winners);
           });

```


17. Generate scales for the data and draw the bar graph using the variables we have
created to dynamically position them. DONE in code above

18. This is nice but we have no way of knowing what values are represented. Lets
add an axis on the left displaying the value range of the bars.

```javaScript
//bars.js
///### line 18
// Add margins so there is room to draw our axis
    var marginLeft = 40;

///### line 22 change the width
var width = boundingRect.width - marginLeft;

///### line 25

// Position the chart with the margin accounted for
    chart.attr('transform', 'translate(' + marginLeft + ',0)');

```
19. To do this we first need to make room on the left side of the graph so we will
add a left margin.

```javaScript
///### Line 90 at the end and outside of the bar.selectAll function but inside the render function

// Create a Y axis on the left side from our winner scale
        // If the largest value is greater than 10 only draw 10 tick marks
        // but if the value is less than 10, e.g. 3, only draw 3 tick marks
        var yAxis = d3.axisLeft(winnerScale)
            .ticks(Math.min(10, maxWinner));

        graph.append("g")
            .classed("y axis", true)
            .call(yAxis);

```


20. Now that we have a left margin we can draw an axis on the left to show our
winner count values.

```javaScript
//### line 18
// Add margins so there is room to draw our axis
    var margin = {'left': 40, 'right': 0, 'top': 10, 'bottom': 10};

//### lines 21-23
// Hang on to the width and height values to use when generating the graph
    var width = boundingRect.width - (margin.left + margin.right);
    var height = boundingRect.height - (margin.top + margin.bottom);

//### line 26
// Position the chart with the margin accounted for
    chart.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

```

21. In order to avoid cutting off the top and bottom of the axis labels we need
to create margins on the top and bottom. Change our variable to an object
and update the positioning of the graph to include the margin offsets.

Now we can create an axis on the bottom with our country names.

```javaScript
///### below append(g)
// Create an X axis on the bottom to show the country names
        var xAxis = d3.axisBottom(nameScale);

        graph.append("g")
            .classed("x axis", true)
            .call(xAxis);


```

23. The positioning is not correct even though we specified a bottom axis. This
is because that just adjusts the orientation of the labels. We still need to
position the axis on the bottom of the graph. We'll also need to increase our
bottom margin so it is visible.

```javaScript
///### line 18/19
// Add margins so there is room to draw our axis
    var margin = {'left': 40, 'right': 0, 'top': 10, 'bottom': 20};


///### add to the append(g) line 105
.attr('transform', 'translate(0,' + height + ')');

///so the function looks like this
graph.append("g")
            .classed("x axis", true)
            .call(xAxis)
            .attr('transform', 'translate(0,' + height + ')');
    }



```

24. The country names are too long to read so instead of using the country names
for our data lets use our country alpha codes.
```javaScript
///### change the attribute x at line 83
return nameScale(d.alpha_code);
```


25. The alpha codes are nice but they are still too close together so let's rotate
them so they are readable.
```javaScript
//### change the alpha code atribute tranform line 106
.selectAll("text")
.attr('transform', 'rotate(-65)');
```

26. They are rotated around their center point so they over lap with the bars. In
order to fix that we change the text anchor point to the end and move them down
using the relative coordinate attributes (dx & dy).

```javaScript
//### line 19 update
var margin = {'left': 40, 'right': 0, 'top': 10, 'bottom': 40};


///### line 108 add
.style('text-anchor', 'end')
            .attr('dx', '-.8em')
            .attr('dy', '.15em');


```
27. We can clean up the visual complexity of the x axis by turning off the end ticks
using the tickSizeOuter param and setting it to zero.

```javaScript
///### line 101

.tickSizeOuter(0);


///### should look like this   
// Create an X axis on the bottom to show the country names
        var xAxis = d3.axisBottom(nameScale)
            .tickSizeOuter(0);

```

Now run server and test out!
```
docker run -v $PWD:/opt/project -it -p 8000:8000 nobel-app ./env/bin/python3 nobel/manage.py runserver 0.0.0.0:8000
```
