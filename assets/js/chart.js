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
    var datasets = {
        xs: {},
        columns: [],
        unload: true
    };

    chart.regions([
        {axis: 'y', start: riskBound, end: dangerBound, class: 'regionRisk'},
        {axis: 'y', start: dangerBound, class: 'regionDanger'}
    ]);

    Promise.all(promises).then(function (value) {
        for (var i = 0; i < value.length; i++) {
            var result = value[i];
            datasets.columns.push(['sensor' + i]);
            for (var j = 0; j < data.length; j++) {
                datasets.columns[datasets.columns.length - 1].push(result.data[j]);
            }
            datasets.columns.push(['sensor' + i + '_x']);
            for (j = 0; j < data.length; j++) {
                datasets.columns[datasets.columns.length - 1].push(new Date(result.labels[j]).toISOString());
            }
            datasets.xs['sensor' + i] = 'sensor' + i + '_x';
        }

        console.log(datasets);
        chart.load(datasets);
    }, function (reason) {
        console.log(reason);
    });
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

var chart = c3.generate({
    bindto: '#chart',
    data: {
        xFormat: '%Y-%m-%dT%H:%M:%S.%LZ',
        columns: []
    },
    axis: {
        x: {
            type: 'timeseries',
            tick: {
                format: '%Y-%m-%d %H:%M:%S'
            }
        }
    }
});

setInterval(function () {
    var promises = getAsyncManyDataPromises(sensors, from, to);
    getAsyncEdgesPromise(sensors[0]).then(function (edges) {
        prepareChartData(promises, edges['risk'], edges['danger']);
    }, function (reason) {
        console.log(reason);
    });
}, 15000);


$("#update-sensors").click(function () {
    sensors = $('#sensor-select').val();

    from = $('#from').pickadate('picker').get('select', 'dd/mm/yyyy');
    to = $('#to').pickadate('picker').get('select', 'dd/mm/yyyy');

    var promises = getAsyncManyDataPromises(sensors, from, to);
    getAsyncEdgesPromise(sensors[0]).then(function (edges) {
        prepareChartData(promises, edges['risk'], edges['danger']);
    }, function (reason) {
        console.log(reason);
    });
});