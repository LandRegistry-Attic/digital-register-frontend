from flask.ext.assets import Bundle  # type: ignore
from os import path                  # type: ignore


css = Bundle('land-registry-elements/stylesheets/govuk-template.css',
             'land-registry-elements/stylesheets/fonts.css',
             'land-registry-elements/stylesheets/elements.css',
              output='dist/css/main.css')

css_print = Bundle('land-registry-elements/stylesheets/govuk-template-print.css',
                    output='dist/css/print.css')

css_ie8 = Bundle('land-registry-elements/stylesheets/govuk-template-ie8.css',
                 'land-registry-elements/stylesheets/fonts-ie8.css',
                 'land-registry-elements/stylesheets/elements-ie8.css',
                  output='dist/css/main-ie8.css')

css_ie7 = Bundle('land-registry-elements/stylesheets/govuk-template-ie7.css',
                 'land-registry-elements/stylesheets/elements-ie7.css',
                  output='dist/css/main-ie7.css')

css_ie6 = Bundle('land-registry-elements/stylesheets/govuk-template-ie6.css',
                 'land-registry-elements/stylesheets/elements-ie6.css',
                  output='dist/css/main-ie6.css')

js_ie = Bundle('land-registry-elements/javascripts/ie.js',
                      'land-registry-elements/javascripts/polyfills.js',
                      filters='rjsmin', output='dist/javascript/ie.js')


js = Bundle('land-registry-elements/javascripts/govuk-template.js',
            'land-registry-elements/javascripts/leaflet.js',
            'land-registry-elements/javascripts/landregistry.js',
            filters='rjsmin', output='dist/javascript/main.js')
