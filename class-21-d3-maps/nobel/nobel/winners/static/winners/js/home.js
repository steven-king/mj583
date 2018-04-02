// fetchData
function fetchData(cb) {
    $.get("/api/?" + $.param(window.nobel.params))
        .done(cb)
        .fail(function(){
            console.log("Could not load data");
            alert("Could not load data");
        });
}

function handleDataLoaded(data) {
    window.nobel.data = data
    $('#raw-json').text(JSON.stringify(data, null, '  '));
    if (window.nobel.mapReady) {
        window.nobel.render();
    }
    if (window.nobel.barReady) {
        window.nobel.renderBar();
    }
}

// watchSelections adds event handlers to track changes users make to selections
// on the page and fetch new data.
function watchSelections() {
    var countrySel = $('#sel-country');
    var categorySel = $('#sel-category');
    var genderSel = $('#sel-gender');

    function updateSelections() {
        var params = window.nobel.params || {};
        params.country = countrySel.val();
        params.category = categorySel.val();
        params.gender = genderSel.val();
        window.nobel.params = params;
        fetchData(handleDataLoaded);
    }

    countrySel.on('change', updateSelections);
    categorySel.on('change', updateSelections);
    genderSel.on('change', updateSelections);
    updateSelections();
}

$(function() {
    // Create a global var to hold our data & state
    window.nobel = {};

    // Update our data based on what's selected
    watchSelections();

    // initMap is from map.js
    initMap(window.nobel);

    // initBar is from bar.js
    initBar(window.nobel);
})
