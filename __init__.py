from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from rides.rides import rides_bp

load_dotenv()
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

app.register_blueprint(rides_bp, url_prefix="/rides")