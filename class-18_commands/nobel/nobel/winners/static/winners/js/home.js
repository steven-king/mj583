// Global container for our winner data
window.winners = {
    params: {},
    data: {},
};

// fetchData
function fetchData() {
    $.get("/api/?" + $.param(window.winners.params))
        .done(function(data) {
            $('#raw-json').text(JSON.stringify(data, null, '  '));
        })
        .fail(function(){
            console.log("Could not load data");
            alert("Could not load data");
        });
}

function setupMapData(){
    var q = d3.queue()
        .defer(d3.json, "static/winners/data/world-110m.json")
        .defer(d3.csv, "static/winners/data/world-country-names-nobel.csv")
        .defer(d3.json, "static/winners/data/winning_country_data.json");
    
    q.await(ready);

    function ready(error, worldMap, countryNames, countryData) {
        // LOG ANY ERROR TO CONSOLE 
        if(error){
            return console.warn(error);
        }
        // STORE OUR COUNTRY-DATA DATASET
        window.winners.data.countryData = countryData;
        // // MAKE OUR FILTER AND ITS DIMENSIONS
        // nbviz.makeFilterAndDimensions(winnersData);
        // INITIALIZE MENU AND MAP
        // nbviz.initMenu();
        window.winners.initMap(worldMap, countryNames);
        // TRIGGER UPDATE WITH FULL WINNERS' DATASET
        // nbviz.onDataChange();
    }
}

// init wires up watchers on selections and fetches new data
function init(){
    var countrySel = $('#sel-country');
    var categorySel = $('#sel-category');
    var genderSel = $('#sel-gender');

    function updateSelections() {
        var params = window.winners.params || {};
        params.country = countrySel.val();
        params.category = categorySel.val();
        params.gender = genderSel.val();
        fetchData();
    }

    countrySel.on('change', updateSelections);
    categorySel.on('change', updateSelections);
    genderSel.on('change', updateSelections);
    updateSelections();
    setupMapData();
}

// Call init on DOMReady
$(init);