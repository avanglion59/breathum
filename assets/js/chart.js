function getAsyncOneDataPromise(id, from, to) {
    return Promise.resolve($.getJSON({
        url: '../api/timedelta',
        data: {
            id: id,
            from: from,
            to: to
        }
    }));
}

function getAsyncManyDataPromises(sensors, from, to) {
    var promises = [];
    for (var i = 0; i < sensors.length; i++) {
        promises.push(getAsyncOneDataPromise(sensors[i], from, to));
    }
    return promises;
}

function prepareChartData(promises, riskBound, dangerBound) {
    var datasets = [];

    datasets.push({
        label: 'Risk Bound',
        borderColor: 'rgb(192, 0, 0)',
        backgroundColor: 'rgba(192, 0, 0, .3)',
        data: [],
        fill: 'end',
        pointRadius: 0,
        pointHoverRadius: 0
    });
    datasets.push({
        label: 'Danger Bound',
        borderColor: 'rgb(192, 192, 0)',
        backgroundColor: 'rgba(192, 192, 0, .3)',
        data: [],
        fill: 'end',
        pointRadius: 0,
        pointHoverRadius: 0
    });

    // for (var i = 0; i < promises.length; i++) {
    //     (function (i) {
    //         promises[i].then(function (result) {
    //             datasets.push(
    //                 {
    //                     label: label,
    //                     borderColor: 'rgb(0, 192, 0)',
    //                     backgroundColor: 'rgba(255, 255, 255, 0)',
    //                     data: [],
    //                     cubicInterpolationMode: 'monotone'
    //                 }
    //             );
    //
    //             console.log(datasets[i + 2]);
    //
    //             for (var j = 0; j < data.length; j++) {
    //                 datasets[i + 2].data.push({x: result.labels[j], y: result.data[j]});
    //                 datasets[0].data.push({x: result.labels[j], y: riskBound});
    //                 datasets[1].data.push({x: result.labels[j], y: dangerBound});
    //             }
    //         }, function (reason) {
    //             console.log(reason);
    //         });
    //     })(i);
    // }

    Promise.all(promises).then(function (value) {
        for (var i = 0; i < value.length; i++) {
            datasets.push(
                {
                    label: label,
                    borderColor: 'rgb(' + Math.floor(Math.random() * 256) + ', ' + Math.floor(Math.random() * 256) + ', ' + Math.floor(Math.random() * 256) + ')',
                    backgroundColor: 'rgba(255, 255, 255, 0)',
                    data: [],
                    cubicInterpolationMode: 'monotone'
                }
            );
            var result = value[i];

            for (var j = 0; j < data.length; j++) {
                datasets[i + 2].data.push({x: result.labels[j], y: result.data[j]});
                datasets[0].data.push({x: result.labels[j], y: riskBound});
                datasets[1].data.push({x: result.labels[j], y: dangerBound});
            }
        }
    }, function (reason) {
        console.log(reason);
    });

    return datasets
}

function getAsyncEdgesPromise(id) {
    return Promise.resolve($.getJSON({
        url: '../api/edges',
        data: {'id': id}
    }));
}

$(document).ready(function () {
    $('select').material_select();
});

// Query Variables
var sensors = [];
var from = '';
var to = '';

$("#category-select").change(function () {
    var category = this.value;

    var sensor_select = $('#sensor-select');

    sensor_select.empty();
    $.getJSON({
        url: '../api/sensors',
        data: {'type': category},
        success: function (data) {
            for (var i = 0; i < data.length; i++) {
                sensor_select
                    .append($("<option></option>")
                        .attr("value", data[i])
                        .text(data[i]));
            }

            sensor_select.material_select();
        }
    });

});


ctx = document.getElementById('chart').getContext('2d');
config = {
    type: 'line',

    data: {
        labels: dates,
        datasets: [{
            label: 'Danger Bound',
            borderColor: 'rgb(192, 192, 0)',
            backgroundColor: 'rgba(192, 192, 0, .3)',
            data: new Array(data.length).fill(danger),
            fill: 'end',
            pointRadius: 0,
            pointHoverRadius: 0
        }, {
            label: 'Risk Bound',
            borderColor: 'rgb(192, 0, 0)',
            backgroundColor: 'rgba(192, 0, 0, .3)',
            data: new Array(data.length).fill(risk),
            fill: 'end',
            pointRadius: 0,
            pointHoverRadius: 0
        }, {
            label: label,
            borderColor: 'rgb(0, 192, 0)',
            backgroundColor: 'rgba(255, 255, 255, 0)',
            data: data,
            cubicInterpolationMode: 'monotone'
        }]
    },

    options: {
        legend: {
            position: 'bottom'
        },
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    tooltipFormat: 'll HH:mm'
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Datetime'
                }
            }],
            yAxes: [{
                ticks: {
                    beginAtZero: true
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Value'
                }
            }]
        },
        layout: {
            padding: {
                left: 25,
                right: 100,
                top: 25,
                bottom: 25
            }
        }
    }
};

$("#sidebar-btn").sideNav();

$('.datepicker').pickadate({
    selectMonths: true,
    selectYears: 15,
    today: 'Today',
    clear: 'Clear',
    close: 'Ok',
    closeOnSelect: true,
    onStart: function () {
        var date = new Date();
        this.set('select', [date.getFullYear(), date.getMonth(), date.getDate()]);
    }
});

chart = new Chart(ctx, config);

setInterval(function () {
    var promises = getAsyncManyDataPromises(sensors, from, to);
    getAsyncEdgesPromise(sensors[0]).then(function (edges) {
        config.data.datasets = prepareChartData(promises, edges['risk'], edges['danger']);
        chart.destroy();
        chart = new Chart(ctx, config);
    }, function (reason) {
        console.log(reason);
    });
}, 15000);


$("#update-sensors").click(function () {
    sensors = $('#sensor-select').val();

    config.data.labels = [];
    config.data.datasets = [];

    from = $('#from').pickadate('picker').get('select', 'dd/mm/yyyy');
    to = $('#to').pickadate('picker').get('select', 'dd/mm/yyyy');

    var promises = getAsyncManyDataPromises(sensors, from, to);
    getAsyncEdgesPromise(sensors[0]).then(function (edges) {
        config.data.datasets = prepareChartData(promises, edges['risk'], edges['danger']);
        chart.destroy();
        chart = new Chart(ctx, config);
    }, function (reason) {
        console.log(reason);
    });
});