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

function getChartMouseUpFunc(chart){
    return function(e){
        var yValue = getValueY(e, chart)
        if (dIndex > -1){
            var data = chart.data;
            data.datasets[dIndex].data[cIndex] = yValue;
            chart.update();
            dIndex = -1;
        }
    }
}

function createCharts(fund_id, chartStat, stats){

        var Canvas = $('canvas', $(chartStat, $('[fund='+fund_id+']')))[0];
        var Ctx = Canvas.getContext('2d');

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

        chart = new Chart(Ctx, {
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

        Canvas.onmousedown = getChartMouseDownFunc(chart)
        Canvas.onmouseup = getChartMouseUpFunc(chart)

}


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

        createCharts(fund_id, '.fund-alpha', ['RF', 'RM', 'Alpha']);
        createCharts(fund_id, '.fund-beta', ['Beta']);
        createCharts(fund_id, '.fund-curves', ['c_rate', 'd_rate']);

    }





})