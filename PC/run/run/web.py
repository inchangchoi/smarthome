# from http://flask.pocoo.org/ tutorial
import os
from flask import Flask, url_for, request, render_template
import run
import threading


thread = threading.Thread(target=run.run)
thread.start()


app = Flask(__name__)

@app.route('/')
def index(): 
    return render_template('index.html', temp = run.temperature)
    #return "Current temperature: " + str(run.temperature)


@app.route('/onoff')
def onoff(): 
    #return render_template('index.html')
    mode = request.args['mode']
    run.manipulate( int(mode) )
    return "OK"




#@app.route('/user/<username>')
#def profile(username): pass


#def do_the_login():
#    print("DTL")

#def show_the_login_form():
#    print("STLF")


#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    if request.method == 'POST':
#        do_the_login()
#    else:
#        show_the_login_form()
#    return "AAAA"

#@app.route('/hello/')
#@app.route('/hello/<name>')
#def hello(name=None):
#    return render_template('hello.html', name=name)



if __name__ == "__main__":
    print(os.getcwd())
    #app.config['SERVER_NAME'] = "0.0.0.0:5000"

    #with app.test_request_context():
    #    url_for('static', filename='style.css')
    app.run(host = '0.0.0.0', port=1248)



    #with app.test_request_context():
    #    print ( url_for('index') )
    #    print ( url_for('login') )
    #    print ( url_for('login', next='/', test="hello") )
    #    print ( url_for('profile', username='John Doe') )
