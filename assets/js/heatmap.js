$("#sidebar-btn").sideNav();

var cfg = {
    radius: 0.001,
    scaleRadius: true,
    latField: 'lat',
    lngField: 'lng',
    valueField: 'val'
};


// To change data
// markers[0]._popup._content = "HALOU"

var heatmap_data = {
    max: 1000,
    min: -100,
    data: data
};

var heatmapLayer = new HeatmapOverlay(cfg);

var base = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
});

var map = new L.Map('content', {
    zoom: 4,
    layers: [base, heatmapLayer]
});

// navigator.geolocation.getCurrentPosition(
//     function (position) {
//         map.setView([position.coords.latitude, position.coords.longitude], 12);
//         console.log(position);
//     },
//     function (error) {
//         console.log(error);
//         map.setView([47.09514, 37.54131], 12);
//     }
// );

map.setView([47.09514, 37.54131], 12);

heatmapLayer.setData(heatmap_data);

$.ajaxSetup({
    url: '../api/map',
    success: function (result) {
        data = result;
        heatmap_data.data = data;
        heatmapLayer.setData(heatmap_data);
    }
});

setInterval($.ajax, 15000);