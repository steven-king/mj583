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


