var copy = require('ncp').ncp;

require('land-registry-elements').then(function(assetPath) {

  var destPath = 'service/static/land-registry-elements';

  copy(assetPath, destPath, function(err, files) {
    if(err) {
      throw err;
      return;
    }

    console.log('Assets copied to', destPath);
  });
})
.catch(function(e) {
  console.error(e);
});

