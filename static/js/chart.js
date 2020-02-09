
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
function datasetAsHTable(dataset, interactable){
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
        for (i=0; i<columnCount; i++){
            value = dataset.datasets[idx].data[i]
            if (interactable){
                html += '<td class="table_valueContainer"><input class="table_value input" onkeydown="changeValue(this)" type="text" dataset="'+idx+'" index="'+i+'" value="'+value.toFixed(3)+'"></td>';
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
            value.scrollIntoView();
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
        var data = setupChart.data;
        datasetIndex = ele.getAttribute("dataset");
        valueIndex = ele.getAttribute("index");
        data.datasets[datasetIndex].data[valueIndex] = parseFloat(ele.value);
        setupChart.update();
        // chartdiv.innerHTML = datasetAsHTable(setupChart.data);
    }
}

var setupChart = null;
var chartdiv = null;

/**
 * This function executes when you change the number in the size field of the table
 * It will resize the horizontal size of that table to that size
 */
function resizeSetupGraph(ele){
    if (event.key === 'Enter' || event.key === 'Tab'){
        var data = setupChart.data;
        count = ele.value;
        data.labels.length = count;
        for (var d=0; d<data.datasets.length; d++){
            data.datasets[d].data.length = count
        }
        for (var i=0; i<count; i++){
            data.labels[i] = (i+1);
            for (var d=0; d<data.datasets.length; d++){
                var value = data.datasets[d].data[i];
                if (value == undefined){
                    data.datasets[d].data[i] = 0;
                }
            }
        }
//        alert(data.labels);
//        alert(data.datasets[0].data);

        chartdiv.innerHTML = datasetAsHTable(data, true);
        setupChart.update();
    }
}

/**
 * This function generates the top graph with some random predetermined values
 */
function createSetupChartAndTable(){
    var setupCanvas = document.getElementById('setupChart');
    var setupCtx = setupCanvas.getContext('2d');
    chartdiv = document.getElementById('setupTable');
    setupChart = new Chart(setupCtx, {
        type: 'line',
        data: {
            labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            datasets: [{
                label: 'Red',
                data: [1.5,2,4,8,6,2,5,6,7,6,4,2,1.5,2],
                backgroundColor: ['rgba(255, 99, 132, 0.2)'],
                borderColor: ['rgba(255, 99, 132, 1)'],
                borderWidth: 1
            },
            {
                label: 'Blue',
                data: [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                backgroundColor: ['rgba(99, 99, 255, 0.2)'],
                borderColor: ['rgba(99, 99, 255, 1)'],
                borderWidth: 1
            }]
        },
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
    setupCanvas.onmousedown = function(e){
        ele = setupChart.getElementAtEvent(e);
        if (ele.length > 0){
            dIndex = ele[0]._datasetIndex;
            cIndex = ele[0]._index;
        }
    }

    setupCanvas.onmouseup = function(e){
        var yValue = getValueY(e, setupChart)
        if (dIndex > -1){
            var data = setupChart.data;
            data.datasets[dIndex].data[cIndex] = yValue;
            setupChart.update();
            //chartdiv.innerHTML = datasetAsHTable(setupChart.data, true);
            updateDatasetAsHTable(chartdiv, setupChart.data, true);
            dIndex = -1;
        }
    }

    chartdiv.innerHTML = datasetAsHTable(setupChart.data, true);
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
    calcChart = new Chart(calcCtx, {
        type: 'line',
        data: {
            labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            datasets: [{
                label: 'Red',
                data: [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                backgroundColor: ['rgba(255, 99, 132, 0.2)'],
                borderColor: ['rgba(255, 99, 132, 1)'],
                borderWidth: 1
            },
            {
                label: 'Blue',
                data: [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                backgroundColor: ['rgba(99, 99, 255, 0.2)'],
                borderColor: ['rgba(99, 99, 255, 1)'],
                borderWidth: 1
            },
            {
                label: 'Cyan',
                data: [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                backgroundColor: ['rgba(99, 255, 255, 0.2)'],
                borderColor: ['rgba(99, 255, 255, 1)'],
                borderWidth: 1
            }]
        },
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
function updateCalcGraph(dataset){
    calcChart.data.labels.length = dataset[0].length;
    for (var i=0; i<count; i++){
        calcChart.data.labels[i] = (i+1);
    }
    for (var d=0; d<dataset.length; d++){
        calcChart.data.datasets[d].data = dataset[d];
    }

    calcChart.update();
}

/**
 * This function is executed by the "Calculate" button.
 * It takes the data from the top table, and sends it to the server
 * The server then responds with calculated data, which is applied to the bottom chart
 */
function calcGraph(){
    body = [];
    for (var i=0; i<setupChart.data.datasets.length; i++){
        body.push(setupChart.data.datasets[i].data);
    }

    $.ajax({
        url: "/fund/calc",
        type: "POST",
        data: JSON.stringify(body),
        contentType: 'application/json',
        success: function(response){
            updateCalcGraph(response);
            calcchartdiv.innerHTML = datasetAsHTable(calcChart.data, false);
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
