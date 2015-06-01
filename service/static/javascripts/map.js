window.onload = function() {

  document.getElementById('map').innerText = '';

  if (polygons && polygons.length > 0) {
    // set up control and options
    options = {
      continuousWorld: true,
      worldCopyJump: false,
      minZoom: 15,
      maxZoom: 19,

      // controls
      dragging: false,
      touchZoom: false,
      doubleClickZoom: false,
      scrollWheelZoom: false,
      boxZoom: false,
      keyboard: false,
      tap: false,
      zoomControl: true,
      attributionControl: false
    };

    var map = new L.Map('map', options);

    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osm = new L.TileLayer(osmUrl);
    map.addLayer(osm);

    L.control.scale().addTo(map);

    var indexStyle = {
      fillcolor: 'blue',
      fillOpacity: 0.5,
      opacity: 0
    };

    var polygon = L.polygon(polygons).addTo(map);

    var bounds = polygon.getBounds();

    map.fitBounds(bounds, {maxZoom: 18, animate: false});
  } else {
    document.getElementById('map').innerText = 'No map information available';
  }
};
