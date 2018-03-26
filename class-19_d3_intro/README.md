# Learning D3.js #

Everything you really need to know can be found here: https://github.com/d3/d3/wiki


1. Pull all the files in this directory and open in Atom.

## Basics of D3. Concepts.

2. 
### Uses the DOM
D3 allows you to bind arbitrary data to a Document Object Model (DOM), and then apply data-driven transformations to the document. For example, you can use D3 to generate an HTML table from an array of numbers. Or, use the same data to create an interactive SVG bar chart with smooth transitions and interaction.

3. 
### Selects like jQuery or other libraries.
D3 employs a declarative approach, operating on arbitrary sets of nodes called selections. For example, you can rewrite the above loop as:

```JavaScript


d3.selectAll("p").style("color", "white");

d3.select("body").style("background-color", "black");
```
4. 
### Enter and Exit slection functions.
You can create new nodes for incoming data and remove outgoing nodes that are no longer needed.
When data is bound to a selection, each element in the data array is paired with the corresponding node in the selection. If there are fewer nodes than data, the extra data elements form the enter selection, which you can instantiate by appending to the enter selection. For example:

```JavaScript
d3.select("body")
  .selectAll("p")
  .data([4, 8, 15, 16, 23, 42])
  .enter().append("p")
    .text(function(d) { return "I’m number " + d + "!"; });
```

5.
### Transformation, not Representation
D3 does not introduce a new visual representation. Unlike Processing or Protovis, D3’s vocabulary of graphical marks comes directly from web standards: HTML, SVG, and CSS. For example, you can create SVG elements using D3 and style them with external stylesheets. IMPORTANT FOR BROWSER COMPABILITITY!

6.
### Transistions
D3’s focus on transformation extends naturally to animated transitions. Transitions gradually interpolate styles and attributes over time. Tweening can be controlled via easing functions such as “elastic”, “cubic-in-out” and “linear”.

```JavaScript
d3.select("body").transition()
    .style("background-color", "black");

```

## Making our first D3 Bar Chart
7.
```JavaScript
//js
var data = [30, 86, 168, 281, 303, 365];

d3.select(".chart")
  .selectAll("div")
  .data(data)
    .enter()
    .append("div")
    .style("width", function(d) { return d + "px"; })
    .text(function(d) { return d; });
```

```html
<!-- html -->
<div class="chart"></div>
```

```css
//css
.chart div {
  font: 10px sans-serif;
  background-color: steelblue;
  text-align: right;
  padding: 3px;
  margin: 1px;
  color: white;
}
```
Explained: The data is loaded as Data
d3 selects the class of chart
It selects all interior ```divs``` but because there are none there it inserts some blank ```<div>``` nodes.
It styles those divs by making them a specific size based on the value in the data.
Note: this is an nice loop over the data without having to write it. This came from the .data() function.
The text is added based on the data.

8.
Here is a little more to it.

```JavaScript
d3.select(".chart")
  .selectAll("div")
  .data(data)
    .enter()
    .append("div")
    .style("width", function(d) { return d * 2 + "px"; })
    .text(function(d) { return '$ ' + d; });

```
We are changing the size and the text. 

### New concept, Method Chaining
9.
Another convenience of selections is method chaining: selection methods, such as selection.attr, return the current selection. This lets you easily apply multiple operations to the same elements. To set the text color and background color of the body without method chaining. For eample. 
``` JavaScript
var body = d3.select("body");
body.style("color", "black");
body.style("background-color", "white");

 //or without using a var
 
 d3.select("body")
    .style("color", "black")
    .style("background-color", "white");
```

10. What is the problem? Sizing!
### Scaling to Fit
D3’s scales specify a mapping from data space (domain) to display space (range):

```JavaScript
var x = d3.scale.linear()
    .domain([0, d3.max(data)])
    .range([0, 420]);


d3.select(".chart")
  .selectAll("div")
    .data(data)
  .enter().append("div")
    .style("width", function(d) { return x(d) + "px"; })
    .text(function(d) { return d; });
    
```

### SVG Verson
11.
```JavaScript

// SVG Version
var width = 420,
    barHeight = 20;

var x = d3.scaleLinear()
    .domain([0, d3.max(data)])
    .range([0, width]);

var chart2 = d3.select(".chart2")
    .attr("width", width)
    .attr("height", barHeight * data.length);

var bar = chart2.selectAll("g")
    .data(data)
  .enter().append("g")
    .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });

bar.append("rect")
    .attr("width", x)
    .attr("height", barHeight - 1);

bar.append("text")
    .attr("x", function(d) { return x(d) - 3; })
    .attr("y", barHeight / 2)
    .attr("dy", ".35em")
    .text(function(d) { return d; });

}
```


```css 

.chart2 rect {
  fill: steelblue; 
}

.chart2 text {
  fill: white;
  font: 10px sans-serif;
  text-anchor: end;
}


```

```html
<h3>SVG Verson </h3>
<svg class="chart2"></svg>

```
