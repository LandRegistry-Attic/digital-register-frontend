from flask.ext.assets import Environment  # type: ignore

from . import pipeline

assets = Environment()

assets.register('js', pipeline.js)
assets.register('js_map', pipeline.js_map)
assets.register('js_ie', pipeline.js_ie)
assets.register('js_ga_search', pipeline.js_ga_search)
assets.register('js_ga_search_results', pipeline.js_ga_search_results)
assets.register('js_googleanalytics', pipeline.js_googleanalytics)

assets.register('css', pipeline.css)
assets.register('css_print', pipeline.css_print)
assets.register('css_ie8', pipeline.css_ie8)
assets.register('css_ie7', pipeline.css_ie7)
assets.register('css_ie6', pipeline.css_ie6)


def register_assets(app):
    assets.init_app(app)
    return assets
