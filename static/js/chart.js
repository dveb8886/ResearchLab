
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

function getValueY(e, myChart){
    const helpers = Chart.helpers;
    var pos = helpers.getRelativePosition(e, myChart);
    var chartArea = myChart.chartArea;
    var yAxis = myChart.scales['y-axis-0'];
    return map(pos.y, chartArea.bottom, chartArea.top, yAxis.min, yAxis.max);
}

function datasetAsHTable(dataset){
    var html = '<table class="table_tag">';
    html += '<tr> <th>#</th>';

    var columnCount = 0;
    for (var item of dataset.labels){
        html += '<th class="table_colHeader">'+item+'</th>'; // column header
        columnCount += 1;
    }

    var idx = 0;
    for (var item of dataset.datasets){
        html += '<tr class="table_row"><td class="table_rowHeader">'+item.label+'</td>'; // row header
        for (i=0; i<columnCount; i++){
            value = dataset.datasets[idx].data[i]
            html += '<td class="table_valueContainer"><input class="table_valueInput" onkeydown="changeValue(this)" type="text" dataset="'+idx+'" index="'+i+'" value="'+value.toFixed(3)+'"></td>';
        }
        html += '</tr>';
        idx += 1;
    }

    html += '</tr>';
    html += '</table>';
    return html;
}

function changeValue(ele){
    if (event.key === 'Enter' || event.key === 'Tab'){
        var data = myChart.data;
        datasetIndex = ele.getAttribute("dataset");
        valueIndex = ele.getAttribute("index");
        data.datasets[datasetIndex].data[valueIndex] = parseFloat(ele.value);
        myChart.update();
        // chartdiv.innerHTML = datasetAsHTable(myChart.data);
    }
}

var myChart = null;
var chartdiv = null;
window.addEventListener('load', function(){
    var canvas = document.getElementById('myChart');
    var ctx = canvas.getContext('2d');
    var hovertxt = document.getElementById('hovertxt');
    var clicktxt = document.getElementById('clicktxt');
    chartdiv = document.getElementById('theTable');
    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['One', 'Two', 'Three', 'Four', 'Five', 'Six'],
            datasets: [{
                label: 'Red',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            },
            {
                label: 'Blue',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(99, 99, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(99, 99, 255, 1)'
                ],
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
    canvas.onmousedown = function(e){
        ele = myChart.getElementAtEvent(e);
        if (ele.length > 0){
            dIndex = ele[0]._datasetIndex;
            cIndex = ele[0]._index;
            // clicktxt.innerHTML = "click: data="+ele[0]._datasetIndex+", index="+ele[0]._index;
        } else {
            // clicktxt.innerHTML = "click: nothing";
        }


    }

    canvas.onmouseup = function(e){
        var yValue = getValueY(e, myChart)
        // hovertxt.innerHTML = yValue;

        if (dIndex > -1){
            var data = myChart.data;
            data.datasets[dIndex].data[cIndex] = yValue;
            myChart.update();
            chartdiv.innerHTML = datasetAsHTable(myChart.data);
            dIndex = -1;
        }
    }


    chartdiv.innerHTML = datasetAsHTable(myChart.data);


})
