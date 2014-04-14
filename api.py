# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()
from flask import Flask, request, abort, url_for, flash, Blueprint, jsonify
import sys
import json
import os
from os import path, environ
import time
from configs import DevConfig
from views import ctl
#from extensions import mdb



__all__ = ['create_app']

DEFAULT_BLUEPRINTS = (
    ctl,
)


def create_app(config=None, app_name=None, blueprints=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = DevConfig.PROJECT
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name)
    configure_app(app, config)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_error_handlers(app)

    return app


def configure_app(app, config):
    """Configure app from object, parameter and env."""

    app.config.from_object(DevConfig)
    if config is not None:
        app.config.from_object(config)
    # Override setting by env var without touching codes.
    app.config.from_envvar('%s_APP_CONFIG' % DevConfig.PROJECT.upper(), silent=True)


def configure_extensions(app):
    pass
    # flask-mongo
#    mdb.init_app(app)


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_error_handlers(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return "Forbidden", 403

    @app.errorhandler(404)
    def page_not_found(error):
        return "Not found", 404

    @app.errorhandler(500)
    def server_error_page(error):
        return "Server Error", 500

##run
app = create_app()
if __name__ == '__main__':
    port = int(environ.get("PORT", 81))
    app.run(host='0.0.0.0', port=port, debug=True)
