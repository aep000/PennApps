from flask import Flask, request, redirect, jsonify
import json
import twilio.twiml
import os
import goslate
import sqliteutils as sq

HOST = '127.0.0.1'
#PORT = int(os.environ.get('PORT', 80))
#PORT = int(os.environ['PORT'])
PORT = int(os.environ.get('PORT', 80))

DEBUG_MODE = True
 
app = Flask(__name__)
app.debug = True
print "initializing on " + str(PORT) + " debug mode is set to " + str(DEBUG_MODE)
@app.route('/')
def hello():
    print "home page accessed"
    return 'Hello World!'

@app.route("/call", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""
    try: 
	    body = request.values.get('Body', None)
            from_number = request.values.get('From', None)

	    message = cbot(body)
	    resp = twilio.twiml.Response()
	    resp.message(message) 
	    return str(resp) 
    except twilio.TwilioRestException as e:
	print e

@app.route("/register", methods=['GET', 'POST'])
def register():
	register_info = request.data
	print register_info + str(type(register_info))
	Datadict = json.loads(register_info)
	out =  {'username': Datadict['username'], 'password': Datadict['password']}
	return sq.register(out)
	#return jsonify(results={"status":200})
	sq.register(out)

@app.route("/login", methods=['GET', 'POST'])
def login():
	login_info = request.data
	Datadict = json.loads(login_info)
	out =  {'username': Datadict['username'], 'password': Datadict['password']}
	return sq.login(out)
	
#('Username', 'Password')
	
'''
if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

def go_run():
    port = int(os.environ.get('PORT', 8))
    app.run(host='0.0.0.0', port=port)
go_run()
