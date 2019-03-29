from flask import Flask, redirect, url_for, request
import requests #This is not used for now but it may be implemented in the future 

#Create a Flask app instance
app = Flask(__name__)

home = ""
high_low_input = ""

with open("home.html", 'r') as file:
    home = file.read()

with open("HighLow_Input.html", 'r') as file:
    high_low_input = file.read()

@app.route("/", methods=["GET", "POST"])
def main_page():
    return home

@app.route("/input", methods=["GET", "POST"])
def HighLowInput():
    if request.method == "POST":
        return redirect(url_for('display'))
    return high_low_input

@app.route("/display", methods=["GET", "POST"])
def display():
    if request.method == 'POST':
      return 'High: {} <br> Low: {}'.format(request.form['high'], request.form['low'])
#Run the app
if __name__ == '__main__':
  app.run(debug=True)
