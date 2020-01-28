
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

window.addEventListener('load', function(){
    var canvas = document.getElementById('myChart');
    var ctx = canvas.getContext('2d');
    var hovertxt = document.getElementById('hovertxt');
    var clicktxt = document.getElementById('clicktxt');
    var myChart = new Chart(ctx, {
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
            clicktxt.innerHTML = "click: data="+ele[0]._datasetIndex+", index="+ele[0]._index;
        } else {
            clicktxt.innerHTML = "click: nothing";
        }


    }

    canvas.onmouseup = function(e){
        var yValue = getValueY(e, myChart)
        hovertxt.innerHTML = yValue;

        if (dIndex > -1){
            var data = myChart.data;
            data.datasets[dIndex].data[cIndex] = yValue;
            myChart.update();
            dIndex = -1;
        }
    }

})
