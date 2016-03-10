var path = require('path');
var buildAssets = require('/vagrant/apps/land-registry-elements');

buildAssets({
  'destination': path.resolve(__dirname, 'service/static/land-registry-elements'),
  'mode': 'production',
  'assetPath': '/static/land-registry-elements/assets',
  'components': [
    'pages/drv/landing-form',
    'pages/drv/search-form',
    'pages/drv/search-results',
    'pages/drv/order-confirmation',
    'pages/drv/summary',
    'pages/land-registry/error-page'
  ]
})
  .then(function(dest) {
    console.log('Done');
  })
  .catch(function(e) {
    console.error(e);
  });
