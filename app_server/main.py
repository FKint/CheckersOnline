from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_boto3 import Boto3

from navbar import nav_bar

app = Flask("Checkers Online App Server", template_folder="templates")
app.config.from_pyfile('config.cfg')
boto_flask = Boto3(app)
Bootstrap(app)

nav = Nav(app)
nav.register_element('navbar', nav_bar)

from views import *


def main():
    app.run(host=app.config['HOSTNAME'])


if __name__ == "__main__":
    main()
