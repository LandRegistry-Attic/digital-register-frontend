from flask.ext.assets import Bundle  # type: ignore
import sass                          # type: ignore


def compile_sass(_in, out, **kw):
    out.write(
        sass.compile(
            string=_in.read()
        )
    )

govuk = Bundle('.dist/stylesheets/govuk-template.css')
govuk_ie8 = Bundle('.dist/stylesheets/govuk-template-ie8.css')
govuk_ie7 = Bundle('.dist/stylesheets/govuk-template-ie7.css')
govuk_ie6 = Bundle('.dist/stylesheets/govuk-template-ie6.css')

govuk_print = Bundle('.dist/stylesheets/govuk-template-print.css')

elements = Bundle('.dist/stylesheets/elements.css',
                  'app/stylesheets/application.scss',
                  filters=(compile_sass, 'cssmin'), output='.dist/stylesheets/main.css')

elements_ie8 = Bundle('.dist/stylesheets/elements-ie8.css',
                      '.dist/stylesheets/fonts-ie8.css',
                      'app/stylesheets/application.scss',
                      filters=(compile_sass, 'cssmin'), output='.dist/stylesheets/main-ie8.css')

elements_ie7 = Bundle('.dist/stylesheets/elements-ie7.css',
                      '.dist/stylesheets/fonts-ie8.css',
                      'app/stylesheets/application.scss',
                      filters=(compile_sass, 'cssmin'), output='.dist/stylesheets/main-ie7.css')

elements_ie6 = Bundle('.dist/stylesheets/elements-ie6.css',
                      '.dist/stylesheets/fonts-ie8.css',
                      'app/stylesheets/application.scss',
                      filters=(compile_sass, 'cssmin'), output='.dist/stylesheets/main-ie6.css')


js_polyfills_ie9 = Bundle('.dist/javascripts/polyfills-ie9.js')
js_polyfills_ie8 = Bundle('.dist/javascripts/polyfills-ie8.js')
js_promise = Bundle('.dist/javascripts/polyfills-promise.js')

js = Bundle('.dist/javascripts/govuk-template.js',
            '.dist/javascripts/landregistry.js',
            filters='rjsmin', output='.dist/javascripts/main.js')

js_map = Bundle('.land-registry-elements/assets/javascripts/leaflet.js',
                'app/javascripts/map.js',
                filters='rjsmin', output='.dist/javascripts/property-map.js')

js_googleanalytics = Bundle('app/javascripts/googleanalytics.js',
                            filters='rjsmin', output='.dist/javascripts/googleanalytics.js')

js_ga_search = Bundle('app/javascripts/ga_search.js',
                      filters='rjsmin', output='.dist/javascripts/ga_search.js')

js_ga_search_results = Bundle('app/javascripts/ga_search_results.js',
                              filters='rjsmin', output='.dist/javascripts/ga_search_results.js')
