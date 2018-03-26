//Learning JS
var data = [4, 8, 15, 16, 23, 42];


//var url = "student.json";
//var data =[];

window.onload = function() {
 // executes when complete page is fully loaded, including all frames, objects and images
 //loadData();
 makeCharts();
};




function loadData(){

  var promise = $.get(url);
  console.log("promise", promise);

  promise.then(function(data) {
    data = promise.responseJSON.students
  	console.log(data.length);
  }).then(function() {
    data = promise.responseJSON.students
  	console.log("another success");
    console.log(data.length);
    console.log(data);
    makeCharts();
    //console.log(promise.responseJSON.students.length)
  }).catch(function(data){
  	console.log("it failed");

  }).then(function(){
  	console.log("always happen when promise complete");
    console.log(data.length);
    console.log(data[0].value);

  })

  }

function makeCharts(){


//DOM version
var x = d3.scaleLinear()
    .domain([0, d3.max(data)])
    .range([0, 420]);


d3.select(".chart")
  .selectAll("div")
    .data(data)
  .enter().append("div")
    .style("width", function(d) { return x(d) + "px"; })
    .text(function(d) { return d; });

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
