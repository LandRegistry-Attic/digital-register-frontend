from flask.ext.assets import Bundle
from os import path
import sass as libsass


__dot = path.dirname(path.realpath(__file__))
__toolkit_dir = path.join(__dot, 'govuk_frontend_toolkit/stylesheets/')
__elements_dir = path.join(__dot, 'stylesheets/elements/')
__landregistry_dir = path.join(__dot, 'stylesheets/landregistry/')

def __compile_sass(_in, out, **kw):
    out.write(
        libsass.compile(
            string=_in.read(),
            include_paths=[__toolkit_dir, __elements_dir, __landregistry_dir]
        )
    )


sass = Bundle('stylesheets/main.scss',
              'stylesheets/main-ie6.scss',
              'stylesheets/main-ie7.scss',
              'stylesheets/main-ie8.scss',
              filters=(__compile_sass,),
              output='gen/main.css')
