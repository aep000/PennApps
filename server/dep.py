import json
from flask import Flask, request, redirect
import MySQLdb as mdb
app = Flask(__name__)
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
	start = request.values.get('start', None)
	end = request.values.get('end', None)
	cid = request.values.get('cid', None)
	query = "SELECT max(messagenumber) FROM messages WHERE conversationID ="+cid
        retval = dbquery(query)
	query = "SELECT * FROM messages WHERE conversationID ="+cid+" and messagenumber >"+retval-end+" and messagenumber <"+retval-start+" ORDER BY messagenumber ASC;"
	retval = dbquery(query)
	c=0
	tot=""
	for message in retval:
		tot += json.dumps({c,message["messagebody"],message["sendertype"]})
		c +=1
	return tot
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
