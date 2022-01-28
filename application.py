import flask
import flask_cors
import config


application = flask.Flask(__name__)
application.debug = config.APP_DEBUG
cors = flask_cors.CORS()
application.config["SECRET_KEY"] = config.SECRET_KEY
application.config["S3"] = config.S3_ACCESS
application.config["API_ROUTES"] = config.API_ROUTES
cors.init_app(application)

with application.app_context():
    import routes

if __name__ == '__main__':
    application.run(debug=True)

