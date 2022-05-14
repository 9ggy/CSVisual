from flask import Flask

app = Flask(__name__)


def create_application():
	from .core import core
	app.register_blueprint(core)
	
	return app