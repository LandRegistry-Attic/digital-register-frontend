from flask.ext.assets import Environment  # type: ignore
import os
from . import pipeline
from shutil import copytree, rmtree

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

    # Copy various images from the original stylesheet directory into the built output
    # Reason being, we are using flash assets to compress the css to a new folder
    # but the images don't automatically come along with it so we have to copy them manually
    dir = os.path.dirname(__file__)
    folders = ['external-links', 'fonts', 'images']

    for folder in folders:
      src = os.path.join(dir, 'land-registry-elements/assets/stylesheets', folder)
      dest = os.path.join(dir, 'dist/css', folder)
      rmtree(dest, True)
      copytree(src, dest)


    return assets
