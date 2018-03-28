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
``` HTML
function initBar(config) {
    var svgContainer = d3.select("#nobel-bar");

    // Create an object to export our methods on the config
    config.bar = {};

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

15. Update the bar js to scale to the width of the containing element and get our
country data sorted and ready to use to make a graph.

16. Create arrays of country names and country winner counts to use for our scales.

17. Generate scales for the data and draw the bar graph using the variables we have
created to dynamically position them.

18. This is nice but we have no way of knowing what values are represented. Lets
add an axis on the left displaying the value range of the bars.

19. To do this we first need to make room on the left side of the graph so we will
add a left margin.

20. Now that we have a left margin we can draw an axis on the left to show our
winner count values.

21. In order to avoid cutting off the top and bottom of the axis labels we need
to create margins on the top and bottom. Change our variable to an object
and update the positioning of the graph to include the margin offsets.

Now we can create an axis on the bottom with our country names.

23. The positioning is not correct even though we specified a bottom axis. This
is because that just adjusts the orientation of the labels. We still need to
position the axis on the bottom of the graph. We'll also need to increase our
bottom margin so it is visible.

24. he country names are too long to read so instead of using the country names
for our data lets use our country alpha codes.

25. The alpha codes are nice but they are still too close together so let's rotate
them so they are readable.

26. They are rotated around their center point so they over lap with the bars. In
order to fix that we change the text anchor point to the end and move them down
using the relative coordinate attributes (dx & dy).

27. We can clean up the visual complexity of the x axis by turning off the end ticks
using the tickSizeOuter param and setting it to zero.

Now run server and test out!
```
docker run -v $PWD:/opt/project -it -p 8000:8000 nobel-app ./env/bin/python3 nobel/manage.py runserver 0.0.0.0:8000
```
