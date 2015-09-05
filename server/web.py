from flask import Flask, request, redirect, jsonify
import json
import twilio.twiml
import os
import goslate
import sqliteutils as sq
import MySQLdb as mdb
import dep
HOST = '45.79.138.244'
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
	    message = dep.messaging(phone_number, message)  
	    body = request.values.get('Body', None)
 	    from_number = request.values.get('From', None)
	    if body[0] == "/":
		pass
	    else:
		message_interface = dep.messenger(phone_number, message)
		message = message_interface.get_message()
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
	out =  {'username': Datadict['username'], 'name': Datadict['name'], 'password': Datadict['password'], 'specialty':Datadict['specialty']}
	return sq.register(out)
	#return jsonify(results={"status":200})
@app.route("/doclist", methods=['GET', 'POST'])
def doclist():
	register_info = request.data
	Datadict = json.loads(register_info)
	amount=Datadict['amount']
	uid = Datadict['uid']
	tot ="{"
	query="SELECT * FROM conversations ORDER BY ID DESC"
	retval = dbquery(query)
	c=0
	for conv in retval:
		if(c < int(amount)):
			query= "SELECT * FROM messages WHERE conversationID = "+str(conv['ID'])
			retval2 = dbquery(query)
			if len(retval2) == 1:
				query = "SELECT * FROM texters WHERE phone = "+conv['texternumber']
				retval3 = dbquery(query)
				print retval3
				tot += '"'+str(c)+'": { "question": "'+conv['question']+'", "sendername": "'+retval3[0]['name']+'"},'
				c+=1
	tot = tot[:-1]
	tot += "}"
	return tot
@app.route("/login", methods=['GET', 'POST'])
def login():
	login_info = request.data
	Datadict = json.loads(login_info)
	out =  {'username': Datadict['username'], 'password': Datadict['password']}
	return sq.login(out)
def dbquery(query):
	con = mdb.connect('127.0.0.1', 'root', "emerson1", 'Pennapps');
	cur = con.cursor(mdb.cursors.DictCursor)
	cur.execute(query)
	results =  cur.fetchall()
	con.close()
	return results
def dbinsert(query):
	con = mdb.connect('127.0.0.1', 'root', "emerson1", 'Pennapps');
	cur = con.cursor(mdb.cursors.DictCursor)
	cur.execute(query)
	results =  cur.fetchall()
	con.commit()
	con.close()
@app.route("/addmessage", methods=['GET', 'POST'])
def storemessage():
	register_info = request.data
	Datadict = json.loads(register_info)
	stype=Datadict['stype']
	cid= Datadict['cid']
	message = Datadict['message']
	query = "SELECT max(messagenumber) FROM messages WHERE conversationID = "+cid
	retval = dbquery(query)
	print retval[0]['max(messagenumber)']
	query = "INSERT INTO messages (messagenumber, messagebody, sendertype, conversationID) VALUES ("+str(retval[0]['max(messagenumber)']+1)+", '"+message+"', '"+stype+"', "+str(cid)+")"
	dbinsert(query)
	return "ok"
@app.route("/getmessage", methods=['GET', 'POST'])
def retmessages():
	register_info = request.data
	Datadict = json.loads(register_info)
	start=Datadict['start']
	cid= Datadict['cid']
	end = Datadict['end']
	query = "SELECT max(messagenumber) FROM messages WHERE conversationID ="+str(retval[0]['max(messagenumber)'])
	retval = dbquery(query)
	query = "SELECT * FROM messages WHERE conversationID ="+cid+" and messagenumber >"+retval-end+" and messagenumber <"+retval-start+" ORDER BY messagenumber ASC;"
	retval = dbquery(query)
	c=0
	tot=""
	for message in retval:
		tot += '{"messagenumber": "'+c+'", "body": "',message["messagebody"]+'", "stype": "',message["sendertype"]+'"}'
		c +=1
	return tot

#('Username', 'Password')

'''
if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

def go_run():
    port = int(os.environ.get('PORT', 80))
    app.run(host='45.79.138.244', port=port)
go_run()
