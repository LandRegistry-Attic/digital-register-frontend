var path = require('path');
var buildAssets = require('/vagrant/apps/land-registry-elements');

buildAssets({
  'includePath': '/vagrant/apps/land-registry-elements',
  'destination': path.resolve(__dirname, 'service/static/.land-registry-elements'),
  'assetPath': '/static/.land-registry-elements/assets',
  'components': [
    'pages/find-property-information/landing-form',
    'pages/find-property-information/search-form',
    'pages/find-property-information/search-results',
    'pages/find-property-information/order-confirmation',
    'pages/find-property-information/summary',
    'pages/find-property-information/cookies',
    'pages/land-registry/error-page'
  ]
})
  .then(function(dest) {
    console.log('Done');
  })
  .catch(function(e) {
    console.error(e);
  });
