from flask import Flask
from flask_bootstrap import Bootstrap
from flask_boto3 import Boto3
from flask_nav import Nav, register_renderer

from navbar import logged_in_nav_bar, not_logged_in_nav_bar
from utilities.ui.bootstrap import CustomBootstrapRenderer

app = Flask("Checkers Online App Server", template_folder="templates")
app.config.from_pyfile('config.cfg')
boto_flask = Boto3(app)
Bootstrap(app)
nav = Nav()

register_renderer(app, 'custom_bootstrap_nav', CustomBootstrapRenderer)
nav.init_app(app)
nav.register_element('login_navbar', logged_in_nav_bar)
nav.register_element('not_login_navbar', not_logged_in_nav_bar)

import views
import setup


def main():
    app.run(host=app.config['HOSTNAME'])


if __name__ == "__main__":
    main()
