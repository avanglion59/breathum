ctx = document.getElementById('chart').getContext('2d');
config = {
    type: 'line',

    data: {
        labels: dates,
        datasets: [{
            label: label,
            borderColor: 'rgb(0, 192, 0)',
            backgroundColor: 'rgba(255, 255, 255, 0)',
            data: data,
            cubicInterpolationMode: 'monotone'
        }, {
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

from = '';
to = '';

var chart = new Chart(ctx, config);

$.ajaxSetup({
    url: 'api',
    success: function (result) {
        config.data.labels = result.labels;
        config.data.datasets[0].data = result.data;
        config.data.datasets[1].data = new Array(data.length).fill(danger);
        config.data.datasets[2].data = new Array(data.length).fill(risk);
        chart.update();
    },
    contentType: 'application/json; charset=utf-8'
});

setInterval(function () {
    $.ajax({
        data: {
            id: sensor,
            from: from,
            to: to
        }
    });
}, 15000);


$("#click").click(function () {
    from = $('#from').pickadate('picker').get('select', 'dd/mm/yyyy');
    to = $('#to').pickadate('picker').get('select', 'dd/mm/yyyy');
    $.ajax({
        data: {
            id: sensor,
            from: from,
            to: to
        }
    });
});

from = $('#from').pickadate('picker').get('select', 'dd/mm/yyyy');
to = $('#to').pickadate('picker').get('select', 'dd/mm/yyyy');
$.ajax({
    data: {
        id: sensor,
        from: from,
        to: to
    }
});
