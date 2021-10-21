from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from . import main

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = b"\x8c\xa5\x04\xb3\x8f\xa1<\xef\x9bY\xca/*\xff\x12\xfb"

    #SQL ALCHEMY     
    app.config["SQL_ALCHEMY_URI"] =\
        "mysql+mysqldb://22_appweb_20:ch2663s7@mysql.lab.it.uc3m.es/22_appweb_20a"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 'False'
    db.init_app(app)

    #Blue prints
    from . import main  
    app.register_blueprint(main.bp)
    return app