
/**
 * Utility function for transforming a value from one coordinate scale to another
 */
function map(value, start1, stop1, start2, stop2) {
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))
}

/**
 * This function takes the location of a mouse click within a graph, and returns the
 *  in-graph y-coordinate of that mouse click
 */
function getValueY(e, chart){
    const helpers = Chart.helpers;
    var pos = helpers.getRelativePosition(e, chart);
    var chartArea = chart.chartArea;
    var yAxis = chart.scales['y-axis-0'];
    return map(pos.y, chartArea.bottom, chartArea.top, yAxis.min, yAxis.max);
}

/**
 * This function creates a table based on a dataset
 */
function datasetAsHTable(dataset, interactable, graphName){
    var html = '<div class="table_container">';
    html += '<div class="table_row_header">';
    html += '<table class="table_tag">';
    count = dataset.labels.length;
    if (interactable){
        html += '<tr> <th><input onkeydown="resizeSetupGraph(this)" class="table_size input" value="'+count+'" /></th> </tr>';
    } else {
        html += '<tr> <th>['+count+']</th> </tr>';
    }

    for (var item of dataset.datasets){
        html += '<tr style="background-color: '+item.backgroundColor+'" class="table_row"><td class="table_rowHeader">'+item.label+'</td></tr>'; // row header
    }
    html += '</table>';
    html += '</div>';

    html += '<div class="table_data_container">';
    html += '<table class="table_tag">';

    var columnCount = 0;
    for (var item of dataset.labels){
        html += '<th class="table_colHeader">'+item+'</th>'; // column header
        columnCount += 1;
    }

    var idx = 0;
    for (var item of dataset.datasets){
        html += '<tr style="background-color: '+item.backgroundColor+'" class="table_row">'; // row header
//        console.log("new row")
        console.log(dataset.datasets[idx])
        for (i=0; i<columnCount; i++){
            value = dataset.datasets[idx].data[i]
//            console.log(" new val")
//            console.log(value)
            if (interactable){
                html += '<td class="table_valueContainer"><input class="table_value input" onkeydown="changeValue(this)" type="text" dataset="'+idx+'" index="'+i+'" graphName="'+graphName+'" value="'+value.toFixed(3)+'"></td>';
            } else {
                html += '<td class="table_valueContainer"><div class="table_value fixed" dataset="'+idx+'" index="'+i+'">'+value.toFixed(3)+'</div></td>';
            }

        }
        html += '</tr>';
        idx += 1;
    }

    html += '</tr>';
    html += '</table>';
    html += '</div>';
    html += '</div>';
    return html;
}

/**
 * This function updates the dataset within an already existing table
 */
function updateDatasetAsHTable(table, dataset, interactable){
    var values = $(table).find(".table_value");
    for (var value of values){
        dIndex = value.getAttribute('dataset');
        vIndex = value.getAttribute('index');
        oldValue = value.value;
        newValue = dataset.datasets[dIndex].data[vIndex].toFixed(3);
        if (oldValue != newValue){
            value.value = newValue;
            value.scrollIntoView({block: 'nearest', inline: 'center', behavior: 'smooth'});
            $(value).css("background-color", "rgba(255, 255, 0, 1)");
            value.setAttribute('fadebackground', '1');
        }

    }
}

/**
 * This function executes when you change the numbers directly in the top table
 * Such a change results in the top graph updating
 */
function changeValue(ele){
    if (event.key === 'Enter' || event.key === 'Tab'){
        datasetIndex = ele.getAttribute("dataset");
        valueIndex = ele.getAttribute("index");
        graphName = ele.getAttribute("graphName");
        var chart = null;
        if (graphName == 'market') chart = marketChart;
        if (graphName == 'beta') chart = betaChart;
        if (graphName == 'curves') chart = curvesChart;
        var data = chart.data;
        data.datasets[datasetIndex].data[valueIndex] = parseFloat(ele.value);
        chart.update();
    }
}

var marketChart = null;
var betaChart = null;
var curvesChart = null;

var marketTable = null;
var betaTable = null;
var curvesTable = null;

/**
 * This function executes when you change the number in the size field of the table
 * It will resize the horizontal size of that table to that size
 */
function resizeSetupGraph(ele){
    if (event.key === 'Enter' || event.key === 'Tab'){
        count = ele.value;

        var marketData = marketChart.data;
        var betaData = betaChart.data;
        var curvesData = curvesChart.data;

        marketData.labels.length = count;
        betaData.labels.length = count;
        curvesData.labels.length = count;


        for (var d=0; d<marketData.datasets.length; d++){
            marketData.datasets[d].data.length = count
        }

        for (var d=0; d<betaData.datasets.length; d++){
            betaData.datasets[d].data.length = count
        }

        for (var d=0; d<curvesData.datasets.length; d++){
            curvesData.datasets[d].data.length = count
        }

        for (var i=0; i<count; i++){
            marketData.labels[i] = (i+1);
            betaData.labels[i] = (i+1);
            curvesData.labels[i] = (i+1);

            for (var d=0; d<marketData.datasets.length; d++){
                var value = marketData.datasets[d].data[i];
                if (value == undefined){
                    marketData.datasets[d].data[i] = 0;
                }
            }

            for (var d=0; d<betaData.datasets.length; d++){
                var value = betaData.datasets[d].data[i];
                if (value == undefined){
                    betaData.datasets[d].data[i] = 0;
                }
            }

            for (var d=0; d<curvesData.datasets.length; d++){
                var value = curvesData.datasets[d].data[i];
                if (value == undefined){
                    curvesData.datasets[d].data[i] = 0;
                }
            }
        }

        marketTable.innerHTML = datasetAsHTable(marketData, true);
        marketChart.update();

        betaTable.innerHTML = datasetAsHTable(betaData, true);
        betaChart.update();

        curvesTable.innerHTML = datasetAsHTable(curvesData, true);
        curvesChart.update();
    }
}

/**
 * This function generates the top graph with some random predetermined values
 */
function createSetupChartAndTable(){
    var marketCanvas = document.getElementById('marketChart');
    var betaCanvas = document.getElementById('betaChart');
    var curvesCanvas = document.getElementById('curvesChart');

    var marketCtx = marketCanvas.getContext('2d');
    var betaCtx = betaCanvas.getContext('2d');
    var curvesCtx = curvesCanvas.getContext('2d');

    marketTable = document.getElementById('marketTable');
    betaTable = document.getElementById('betaTable');
    curvesTable = document.getElementById('curvesTable');


    data = {
        labels: loaddata['x'],
        datasets: []
    };

    data1 = {
        labels: loaddata['x'],
        datasets: []
    };

    data2 = {
        labels: loaddata['x'],
        datasets: []
    };


    for (let stat in loaddata['stats']){
        dataset = {label: stat, data: loaddata['stats'][stat]['y']};
        dataset['backgroundColor'] = [loaddata['stats'][stat]['color_fill']];
        dataset['borderColor'] = [loaddata['stats'][stat]['color_line']];
        dataset['borderWidth'] = 1
        if (loaddata['stats_controlled'].includes(stat)){
            data['datasets'].push(dataset);
        }

        if (loaddata['stats_beta'].includes(stat)){
            data1['datasets'].push(dataset);
        }

        if (loaddata['stats_curves'].includes(stat)){
            data2['datasets'].push(dataset);
        }

    };


    marketChart = new Chart(marketCtx, {
        type: 'line',
        data: data,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    betaChart = new Chart(betaCtx, {
        type: 'line',
        data: data1,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    curvesChart = new Chart(curvesCtx, {
        type: 'line',
        data: data2,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });


    dIndex = -1;
    cIndex = -1;

    marketCanvas.onmousedown = function(e){
        ele = marketChart.getElementAtEvent(e);
        if (ele.length > 0){
            dIndex = ele[0]._datasetIndex;
            cIndex = ele[0]._index;
        }
    }

    betaCanvas.onmousedown = function(e){
        ele = betaChart.getElementAtEvent(e);
        if (ele.length > 0){
            dIndex = ele[0]._datasetIndex;
            cIndex = ele[0]._index;
        }
    }

    curvesCanvas.onmousedown = function(e){
        ele = curvesChart.getElementAtEvent(e);
        if (ele.length > 0){
            dIndex = ele[0]._datasetIndex;
            cIndex = ele[0]._index;
        }
    }

    marketCanvas.onmouseup = function(e){
        var yValue = getValueY(e, marketChart)
        if (dIndex > -1){
            var data = marketChart.data;
            data.datasets[dIndex].data[cIndex] = yValue;
            marketChart.update();
            updateDatasetAsHTable(marketTable, marketChart.data, true);
            dIndex = -1;
        }
    }

    betaCanvas.onmouseup = function(e){
        var yValue = getValueY(e, betaChart)
        if (dIndex > -1){
            var data = betaChart.data;
            data.datasets[dIndex].data[cIndex] = yValue;
            betaChart.update();
            updateDatasetAsHTable(betaTable, betaChart.data, true);
            dIndex = -1;
        }
    }

    curvesCanvas.onmouseup = function(e){
        var yValue = getValueY(e, curvesChart)
        if (dIndex > -1){
            var data = curvesChart.data;
            data.datasets[dIndex].data[cIndex] = yValue;
            curvesChart.update();
            updateDatasetAsHTable(curvesTable, curvesChart.data, true);
            dIndex = -1;
        }
    }

    marketTable.innerHTML = datasetAsHTable(marketChart.data, true, "market");
    betaTable.innerHTML = datasetAsHTable(betaChart.data, true, "beta");
    curvesTable.innerHTML = datasetAsHTable(curvesChart.data, true, "curves");
}


var calcChart = null;
var calcchartdiv = null;

/**
 * This function generates the bottom graph with default (all 0) values
 */
function createCalcChartAndTable(){
    var calcCanvas = document.getElementById('calcChart');
    var calcCtx = calcCanvas.getContext('2d');
    calcchartdiv = document.getElementById('calcTable');
    data = {
        labels: loaddata['x'],
        datasets: []
    };
    for (let stat in loaddata['stats']){
        if (loaddata['stats_calculated'].includes(stat)){
            dataset = {label: stat, data: loaddata['stats'][stat]['y']};
            dataset['backgroundColor'] = [loaddata['stats'][stat]['color_fill']];
            dataset['borderColor'] = [loaddata['stats'][stat]['color_line']];
            dataset['borderWidth'] = 1
            data['datasets'].push(dataset);
        }
    };
    calcChart = new Chart(calcCtx, {
        type: 'line',
        data: data,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    calcchartdiv.innerHTML = datasetAsHTable(calcChart.data, false);
}

/**
 * This function updates the bottom graph with the given dataset values
 */
function updateCalcGraph(ds){
    calcChart.data.labels = ds['x'];
    calcChart.data.datasets = [];
    for (let stat in ds['stats']){
        dataset = {label: stat, data: ds['stats'][stat]['y']};
        dataset['backgroundColor'] = [ds['stats'][stat]['color_fill']];
        dataset['borderColor'] = [ds['stats'][stat]['color_line']];
        dataset['borderWidth'] = 1
        calcChart.data.datasets.push(dataset);
    };

    calcChart.update();
}

/**
 * This function is executed by the "Calculate" button.
 * It takes the data from the top table, and sends it to the server
 * The server then responds with calculated data, which is applied to the bottom chart
 */
function calcGraph(){
    body = {fund: loaddata['fund'], x: marketChart.data.labels, stats:{}};

    for (var i=0; i<marketChart.data.datasets.length; i++){
        body['stats'][marketChart.data.datasets[i].label] = {
            y: marketChart.data.datasets[i].data
        }
    };

    for (var i=0; i<betaChart.data.datasets.length; i++){
        body['stats'][betaChart.data.datasets[i].label] = {
            y: betaChart.data.datasets[i].data
        }
    };

    for (var i=0; i<curvesChart.data.datasets.length; i++){
        body['stats'][curvesChart.data.datasets[i].label] = {
            y: curvesChart.data.datasets[i].data
        }
    };

    $.ajax({
        url: "/fund/calc",
        type: "POST",
        data: JSON.stringify(body),
        contentType: 'application/json',
        success: function(response){
            updateCalcGraph(response);
            calcchartdiv.innerHTML = datasetAsHTable(calcChart.data, false);
        }
    });

}

/**
 * This function is executed by the "Commit" button.
 * It takes the data from both tables, and sends it to the server
 * the server will save these values to the database, when the page refresh the data will be retained
 */
function commitGraph(){
    body = {fund: loaddata['fund'], x: marketChart.data.labels, stats:{}};
    for (var i=0; i<marketChart.data.datasets.length; i++){
        body['stats'][marketChart.data.datasets[i].label] = {
            y: marketChart.data.datasets[i].data
        }
    }
    for (var i=0; i<betaChart.data.datasets.length; i++){
        body['stats'][betaChart.data.datasets[i].label] = {
            y: betaChart.data.datasets[i].data
        }
    }

    for (var i=0; i<curvesChart.data.datasets.length; i++){
        body['stats'][curvesChart.data.datasets[i].label] = {
            y: curvesChart.data.datasets[i].data
        }
    }

    for (var i=0; i<calcChart.data.datasets.length; i++){
        body['stats'][calcChart.data.datasets[i].label] = {
            y: calcChart.data.datasets[i].data
        }
    }

    $.ajax({
        url: "/fund/commit",
        type: "POST",
        data: JSON.stringify(body),
        contentType: 'application/json',
        success: function(response){

        }
    })
}

// Runs when the page is fully loaded
window.addEventListener('load', function(){

    // Generates the top chart
    createSetupChartAndTable();

    // Generates the bottom chart
    createCalcChartAndTable();

    // Interval: creates the fading highlight effect on recently updated cells
    window.setInterval(function(){
        var fadecells = $(".table_value[fadebackground]");
        //console.log('fade');
        for (var cell of fadecells){
            //console.log('a cell in fade');
            var alpha = parseFloat(cell.getAttribute('fadebackground'));
            alpha -= 0.1;
            if (alpha < 0) alpha = 0;
            $(cell).css("background-color", "rgba(255, 255, 0, "+alpha+")");
            if (alpha == 0){
                cell.removeAttribute('fadebackground');
            } else {
                cell.setAttribute('fadebackground', alpha);
            }
        }
    }, 200);

})
