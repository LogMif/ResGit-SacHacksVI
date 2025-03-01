import warnings

from flask import Flask, requests
from flask_cors import CORS
from pyngrok import ngrok

app = Flask(__name__)
CORS(app)



if __name__ == '__main__':
    public_url = ngrok.connect(5000)