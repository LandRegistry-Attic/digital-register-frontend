var path = require('path');
var landRegistryElements = require('land-registry-elements');

landRegistryElements({
  'mode': 'production',
  'includePath': __dirname,
  'destination': path.resolve(__dirname, 'service/ui/.land-registry-elements'),
  'assetPath': false, // Don't insert an asset path, we'll let flask set it as a global JS variable
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
