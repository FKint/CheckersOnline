from flask import Flask
from flask_bootstrap import Bootstrap
from flask_boto3 import Boto3
from flask_nav import Nav, register_renderer

from helpers.ui.bootstrap import CustomBootstrapRenderer
from navbar import logged_in_nav_bar, not_logged_in_nav_bar
import os
app = Flask("Checkers Online App Server", template_folder="templates")
app.config.from_pyfile('config/public.general.config')
app.config.from_pyfile('config/public.{}.config'.format(os.environ['ENVIRONMENT']))
app.config.from_pyfile('config/private.{}.config'.format(os.environ['ENVIRONMENT']))

boto_flask = Boto3(app)
Bootstrap(app)
nav = Nav()

register_renderer(app, 'custom_bootstrap_nav', CustomBootstrapRenderer)
nav.init_app(app)
nav.register_element('login_navbar', logged_in_nav_bar)
nav.register_element('not_login_navbar', not_logged_in_nav_bar)

from views import *
from setup import *

def main():
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    main()
