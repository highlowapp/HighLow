# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request


# create the application object
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')  # return a string

@app.route('/signin', methods=['GET', 'POST'])
def signin():

  error = None
  if request.method == 'POST':
    if request.form['email'] != 'admin@gmail.com' or request.form['password'] != 'admin':
        error = 'Invalid Credentials. Please try again.'
    else:
        return redirect(url_for('HighLowInput'))
  return render_template('signin.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  error = None
  #confirmpassword = request.form['confirmpassword']
  #password = request.form['password']
  if request.method == 'POST':
    if request.form['confirmpassword'] != request.form['password']:
        error = 'Your password doesn\'t match. Please try again.'
    else:
      return redirect(url_for('HighLowInput'))
  return render_template('signup.html', error=error)  # render a template
 # if request.method == 'POST':
 # sign_up.sign_up(firstname=request.form['firstname'], lastname=request.form['lastname'], email=request.form['email'], password=request.form['password'], confirmpassword=request.form['confirmpassword'])

@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPassword():
  return render_template('resetPassword.html', methods=['GET', 'POST'])  # render a template

@app.route('/input', methods=['GET', 'POST'])
def HighLowInput():
  error = None
  if request.method == 'POST':
    return redirect(url_for('delay'))
    #return 'High: {} <br> Low: {}'.format(request.form['high'], request.form['low'])
  return render_template('HighLow_Input.html', error=error)


@app.route('/display', methods=['GET', 'POST'])
def display():
  if request.method == 'POST':
    return 'High: {} <br> Low: {}'.format(request.form['high'], request.form['low']) 

#Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
