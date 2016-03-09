var path = require('path');
var buildAssets = require('/vagrant/apps/land-registry-elements');

buildAssets({
  'destination': path.resolve(__dirname, 'service/static/land-registry-elements'),
  'mode': 'production'
})
  .then(function(dest) {
    console.log('Done');
  })
  .catch(function(e) {
    console.error(e);
  });
