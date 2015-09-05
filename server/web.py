from flask import Flask, request, redirect
import twilio.twiml
import os
import goslate
import sqliteutils

HOST = '127.0.0.1'
#PORT = int(os.environ.get('PORT', 80))
#PORT = int(os.environ['PORT'])
PORT = int(os.environ.get('PORT', 80))

DEBUG_MODE = True
 
app = Flask(__name__)

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

@app.route("/call", methods=['GET', 'POST'])
def register():
	register_info = request.data
	Datadict = json.loads(data)
	out =  {'username': Datadict['username'], 'password': Datadict['password']}
	sq.register(out)
	
#('Username', 'Password')
	
'''
if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

def go_run():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

