from flask import Flask, request, redirect
import twilio.twiml
import os
import goslate
import cleverbot


HOST = '127.0.0.1'
#PORT = int(os.environ.get('PORT', 80))
#PORT = int(os.environ['PORT'])
PORT = int(os.environ.get('PORT', 5000))

DEBUG_MODE = True
 
app = Flask(__name__)

def from_latin(to_translate):
        target_language = "en"
        source_language='la'
        gs = goslate.Goslate()
        return  gs.translate(to_translate, target_language, source_language)
def to_latin(to_translate):
        target_language = "la"
        source_language='en'
        gs = goslate.Goslate()
        return  gs.translate(to_translate, target_language, source_language)

def cbot(to_work):
        cb1 = cleverbot.Cleverbot()
        english = from_latin(to_work)
        reply = cb1.ask(english)
        reply = to_latin(reply)
        return reply


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
'''
if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

def go_run():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

