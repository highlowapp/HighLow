from flask import Flask, request
import requests

app = Flask(__name__)

#Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
