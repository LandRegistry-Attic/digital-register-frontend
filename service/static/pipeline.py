from flask.ext.assets import Bundle  # type: ignore
from os import path                  # type: ignore


css = Bundle('land-registry-elements/assets/stylesheets/govuk-template.css',
             'land-registry-elements/assets/stylesheets/fonts.css',
             'land-registry-elements/assets/stylesheets/elements.css',
              output='dist/css/main.css')

css_print = Bundle('land-registry-elements/assets/stylesheets/govuk-template-print.css',
                    output='dist/css/print.css')

css_ie8 = Bundle('land-registry-elements/assets/stylesheets/govuk-template-ie8.css',
                 'land-registry-elements/assets/stylesheets/fonts-ie8.css',
                 'land-registry-elements/assets/stylesheets/elements-ie8.css',
                  output='dist/css/main-ie8.css')

css_ie7 = Bundle('land-registry-elements/assets/stylesheets/govuk-template-ie7.css',
                 'land-registry-elements/assets/stylesheets/elements-ie7.css',
                  output='dist/css/main-ie7.css')

css_ie6 = Bundle('land-registry-elements/assets/stylesheets/govuk-template-ie6.css',
                 'land-registry-elements/assets/stylesheets/elements-ie6.css',
                  output='dist/css/main-ie6.css')

js_ie = Bundle('land-registry-elements/assets/javascripts/ie.js',
               'land-registry-elements/assets/javascripts/polyfills.js',
               filters='rjsmin', output='dist/javascript/ie.js')

js = Bundle('land-registry-elements/assets/javascripts/govuk-template.js',
            'land-registry-elements/assets/javascripts/landregistry.js',
            filters='rjsmin', output='dist/javascript/main.js')

js_leaflet = Bundle('land-registry-elements/assets/javascripts/leaflet.js',
            filters='rjsmin', output='dist/javascript/leaflet.js')
