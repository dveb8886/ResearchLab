
var cache = []
function checkdupes(key, value){
    if (typeof value === 'object' && value !== null) {
        if (cache.indexOf(value) !== -1) {
            // Circular reference found, discard key
            return;
        }
        // Store value in our collection
        cache.push(value);
    }
    return value;
}

// map value to other coordinate system
function map(value, start1, stop1, start2, stop2) {
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))
}

function getValueY(e, chart){
    const helpers = Chart.helpers;
    var pos = helpers.getRelativePosition(e, chart);
    var chartArea = chart.chartArea;
    var yAxis = chart.scales['y-axis-0'];
    return map(pos.y, chartArea.bottom, chartArea.top, yAxis.min, yAxis.max);
}

function datasetAsHTable(dataset, interactable){
    var html = '<div class="table_container">';
    html += '<div class="table_row_header">';
    html += '<table class="table_tag">';
    html += '<tr> <th>#</th> </tr>';
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

function updateCalcGraph(dataset){
    for (var d=0; d<dataset.length; d++){
        calcChart.data.datasets[d].data = dataset[d];
    }

    calcChart.update();
}

function calcGraph(){
    body = [];
    for (var i=0; i<setupChart.data.datasets.length; i++){
        body.push(setupChart.data.datasets[i].data);
    }

    $.ajax({
        url: "/graph/calc",
        type: "POST",
        data: JSON.stringify(body),
        contentType: 'application/json',
        success: function(response){
            updateCalcGraph(response);
            calcchartdiv.innerHTML = datasetAsHTable(calcChart.data, false);
        }
    })

}

window.addEventListener('load', function(){

    createSetupChartAndTable();

    createCalcChartAndTable();

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
