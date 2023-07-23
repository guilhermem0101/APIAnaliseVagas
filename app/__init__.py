from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    from .routes import eixos, estudos, empregos, minerador

    app.register_blueprint(eixos.bp)
    
    app.register_blueprint(empregos.bp)

    return app
