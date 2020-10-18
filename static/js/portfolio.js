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

dIndex = -1;
cIndex = -1;

function getChartMouseDownFunc(chart){
    return function(e){
        ele = chart.getElementAtEvent(e);
        if (ele.length > 0){
            dIndex = ele[0]._datasetIndex;
            cIndex = ele[0]._index;
        }
    }
}

function getChartMouseUpFunc(chart, chart0){
    return function(e){
        var yValue = getValueY(e, chart)
        if (dIndex > -1){
            var data = chart.data;
            data.datasets[dIndex].data[cIndex] = yValue;
            chart.update();
            chart0.update();
            dIndex = -1;
        }
    }
}

function createCharts(fund_id, chartStat, stats){

        var Canvas0 = $('canvas', $(chartStat, $('[fund='+fund_id+']')))[0];
        var Canvas1 = $('canvas', $(chartStat, $('[fund='+fund_id+']')))[1];

        var Ctx0 = Canvas0.getContext('2d');
        var Ctx1 = Canvas1.getContext('2d');

        data = {
            labels: [1,2,3,4,5,6],
            datasets: []
        };

        for (stat in stats){
            stat = stats[stat]
            dataset = {label: stat, data: fund[stat]};
            dataset['borderWidth'] = 1;
            data['datasets'].push(dataset);
        }

        chart0 = new Chart(Ctx0, {
            type: 'line',
            data: data,
            options: {
                legend: {
                    display: false
                },
                scales: {
                    xAxes:[{
                        ticks: {
                            display: false
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            display: false,
                            beginAtZero: true
                        }
                    }]
                }
            }
        });

        chart1 = new Chart(Ctx1, {
            type: 'line',
            data: data,
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            display: true,
                            beginAtZero: true
                        }
                    }]
                }
            }
        });


        Canvas1.onmousedown = getChartMouseDownFunc(chart1)
        Canvas1.onmouseup = getChartMouseUpFunc(chart1, chart0)

        return [chart0, chart1];
}

var calcChart = null;

/**
 * This function generates the bottom graph with default (all 0) values
 */
function createCalcChart(){
    var calcCanvas = document.getElementById('calcChart');
    var calcCtx = calcCanvas.getContext('2d');
    data = {
        labels: [1,2,3,4,5,6],
        datasets: []
    };
//    for (let stat in loaddata['stats']){
//        if (loaddata['stats_calculated'].includes(stat)){
//            dataset = {label: stat, data: loaddata['stats'][stat]['y']};
//            dataset['backgroundColor'] = [loaddata['stats'][stat]['color_fill']];
//            dataset['borderColor'] = [loaddata['stats'][stat]['color_line']];
//            dataset['borderWidth'] = 1
//            data['datasets'].push(dataset);
//        }
//    };
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
}

/**
 * This function updates the bottom graph with the given dataset values
 */
function updateAllResultGraph(ds){
    calcChart.data.labels = [1,2,3,4,5,6];
    calcChart.data.datasets = [];
    for (let stat in ds['stats']){
        dataset = {label: stat, data: ds['stats'][stat]['y']};
        dataset['backgroundColor'] = [ds['stats'][stat]['color_fill']];
        dataset['borderColor'] = [ds['stats'][stat]['color_line']];
        dataset['borderWidth'] = 1
        calcChart.data.datasets.push(dataset);
    };
    calcChart.update();

    for (let idx in ds['funds']){
        fund = ds['funds'][idx]
        fundChart0 = allChartList[fund['fund_id']][3][0]
        fundChart = allChartList[fund['fund_id']][3][1]
        fundChart.data.labels = [1,2,3,4,5,6];
        fundChart.data.datasets = [];
        for (let stat in fund['stats']){
            dataset = {label: stat, data: fund['stats'][stat]['y']};
            dataset['backgroundColor'] = [fund['stats'][stat]['color_fill']];
            dataset['borderColor'] = [fund['stats'][stat]['color_line']];
            dataset['borderWidth'] = 1
            fundChart.data.datasets.push(dataset);
        };
        fundChart.update();
        fundChart0.update();
    }
}

function calcGraph(){
    body = {funds: {}, portfolio: portfolio_data['portfolio']};

    for (var fund=0; fund<portfolio_data['funds'].length; fund++){
        var fund_id = portfolio_data['funds'][fund]['id'];
        stat_dict = {};
        for (var canvas=0; canvas<allChartList[fund_id].length; canvas++){
            chart = allChartList[fund_id][canvas][1]
            for (var stat=0; stat<chart.data.datasets.length; stat++){
                stat_dict[chart.data.datasets[stat].label] = chart.data.datasets[stat].data;
            };
        }
        body['funds'][fund_id] = stat_dict;
    }

    console.log(body);

     $.ajax({
        url: "/portfolio/calc",
        type: "POST",
        data: JSON.stringify(body),
        contentType: 'application/json',
        success: function(response){
            console.log(response)
            updateAllResultGraph(response);
            $('.fund-result').removeClass('hidden');
//            calcchartdiv.innerHTML = datasetAsHTable(calcChart.data, false);
        }
    });
}

allChartList = {};

// Runs when the page is fully loaded
window.addEventListener('load', function(){

    // click listener that switches graph contents when tabs are clicked
    $('.tab').click(function(){
        var clicked_tab_name = $(this).attr('value')

        $('.fund-tab-item').each(function(){
            $(this).addClass('hidden');
            if ($(this).hasClass(clicked_tab_name)) {
                $(this).removeClass('hidden');
            }
        });
    });

    // click listener that show fund contents when fund name is clicked
    $('.fund-name').click(function(){
        var fund_id = $(this).attr('fund');
        var fund_contents = $('.fund-contents', $('.fund-container[fund=\''+fund_id+'\']'))
        fund_contents.toggleClass('hidden');
    });

//    alert(JSON.stringify(portfolio_data));
//    $('#myid').html('<b>my custom text</b>');

    for (i in portfolio_data['funds']){
        fund = portfolio_data['funds'][i]
        var fund_id = fund['id'];
        $('.fund-attributes', $('[fund='+fund_id+']')[0]).html(fund['manager']+' '+fund['vintage']+' '+fund['nav']+' '+fund['unfunded']);

        allChartList[fund_id] = [];

        chart = createCharts(fund_id, '.fund-alpha', ['RF', 'RM', 'Alpha']);
        allChartList[fund_id].push(chart);
        chart = createCharts(fund_id, '.fund-beta', ['Beta']);
        allChartList[fund_id].push(chart);
        chart = createCharts(fund_id, '.fund-curves', ['c_rate', 'd_rate']);
        allChartList[fund_id].push(chart);
        chart = createCharts(fund_id, '.fund-results', []);
        allChartList[fund_id].push(chart);

    }

    createCalcChart();

})