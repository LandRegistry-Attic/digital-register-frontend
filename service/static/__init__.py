from flask.ext.assets import Environment
from . import pipeline

assets = Environment()
assets.register('sass', pipeline.sass)


def register_assets(app):
    assets.init_app(app)
    return assets
