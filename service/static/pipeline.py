from flask.ext.assets import Bundle  # type: ignore
import sass                          # type: ignore


def compile_sass(_in, out, **kw):
    out.write(
        sass.compile(
            string=_in.read()
        )
    )

govuk = Bundle('.land-registry-elements/assets/stylesheets/govuk-template.css',
               filters=(compile_sass, 'cssmin'), output='.dist/css/govuk-template.css')

govuk_ie8 = Bundle('.land-registry-elements/assets/stylesheets/govuk-template-ie8.css',
                   filters=(compile_sass, 'cssmin'), output='.dist/css/govuk-template-ie8.css')

govuk_ie7 = Bundle('.land-registry-elements/assets/stylesheets/govuk-template-ie7.css',
                   filters=(compile_sass, 'cssmin'), output='.dist/css/govuk-template-ie7.css')

govuk_ie6 = Bundle('.land-registry-elements/assets/stylesheets/govuk-template-ie6.css',
                   filters=(compile_sass, 'cssmin'), output='.dist/css/govuk-template-ie6.css')

govuk_print = Bundle('.land-registry-elements/assets/stylesheets/govuk-template-print.css',
                     filters=('cssmin'), output='.dist/css/print.css')

elements = Bundle('.land-registry-elements/assets/stylesheets/elements.css',
                  'app/stylesheets/application.scss',
                  filters=(compile_sass, 'cssmin'), output='.dist/css/main.css')

elements_ie8 = Bundle('.land-registry-elements/assets/stylesheets/elements-ie8.css',
                      '.land-registry-elements/assets/stylesheets/fonts-ie8.css',
                      'app/stylesheets/application.scss',
                      filters=(compile_sass, 'cssmin'), output='.dist/css/main-ie8.css')

elements_ie7 = Bundle('.land-registry-elements/assets/stylesheets/elements-ie7.css',
                      '.land-registry-elements/assets/stylesheets/fonts-ie8.css',
                      'app/stylesheets/application.scss',
                      filters=(compile_sass, 'cssmin'), output='.dist/css/main-ie7.css')

elements_ie6 = Bundle('.land-registry-elements/assets/stylesheets/elements-ie6.css',
                      '.land-registry-elements/assets/stylesheets/fonts-ie8.css',
                      'app/stylesheets/application.scss',
                      filters=(compile_sass, 'cssmin'), output='.dist/css/main-ie6.css')


js_polyfills_ie9 = Bundle('.land-registry-elements/assets/javascripts/polyfills-ie9.js',
                          filters='rjsmin', output='.dist/javascript/polyfills-ie9.js')

js_polyfills_ie8 = Bundle('.land-registry-elements/assets/javascripts/polyfills-ie8.js',
                          filters='rjsmin', output='.dist/javascript/polyfills-ie8.js')

js_promise = Bundle('.land-registry-elements/assets/javascripts/polyfills-promise.js',
                    filters='rjsmin', output='.dist/javascript/polyfills-promise.js')

js = Bundle('.land-registry-elements/assets/javascripts/govuk-template.js',
            '.land-registry-elements/assets/javascripts/landregistry.js',
            filters='rjsmin', output='.dist/javascript/main.js')

js_map = Bundle('.land-registry-elements/assets/javascripts/leaflet.js',
                'app/javascripts/map.js',
                filters='rjsmin', output='.dist/javascript/leaflet.js')

js_googleanalytics = Bundle('app/javascripts/googleanalytics.js',
                            filters='rjsmin', output='.dist/javascript/googleanalytics.js')

js_ga_search = Bundle('app/javascripts/ga_search.js',
                      filters='rjsmin', output='.dist/javascript/ga_search.js')

js_ga_search_results = Bundle('app/javascripts/ga_search_results.js',
                              filters='rjsmin', output='.dist/javascript/ga_search_results.js')
