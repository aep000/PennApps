import json
import MySQLdb as mdb

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
	con.close()\

def helpget(input):
	#/help
	if input[:5] == "/help":
		ret = """
		/reply (conversation number) - Reply to a doctor's response.
		/list - Lists all of your chats
		/close - End a chat
		/ask - Ask a quetion
		/help - See this message again"""
		return ret
	else:
		pass
def txtlist(input, number):
	if input[:5] == "/list":
		query = "SELECT * FROM conversations WHERE texternumber = '"+number+"'"
		retval = dbquery(query)
		ret = ""
		c = 0;
		for chat in retval:
			query = "SELECT * FROM doctors WHERE ID = "+chat['doctorID']
			retval2 = dbquery(query)
			ret += c+") "+retval2[0]['name']+": "+chat['question']+"\n"
			c+=1
		return ret

def close(input, number):
    if input[:6]=="/close":
        query = "SELECT * FROM conversation WHERE texternumber ="+number
        retval=dbquery(query)
        cid = retval[0]['ID']
        query = "DELETE FROM messages WHERE conversationID ="+cid
        dbinsert(query)
        query = "DELETE FROM conversations where texternumber ="+number
        return "Conversation deleted"
def ask(input, number):
    if input[:4]=="/ask":
        query = "SELECT max(ID) FROM conversations"
        retval= dbquery(query)
        cid = retval[0]['max(ID)']
        query = "INSERT INTO conversations (texternumber, question) VALUES ("+str(number)+", "+input[4:]
        retval= dbinsert(query)
        query = "SELECT max(messagenumber) FROM messages WHERE convesationID ="+str(cid)
        retval= dbquery(query)
        mid = retval[0]['max(messagenumber)']
        query = "INSERT INTO messages (conversationID, messagebody, sendertype, messagenumber) VALUES ("+cid+", "+input[4:]+", texter, "+ str(mid+1)+")"
        return "Your question has been submitted"
def reply(input, number):
    if input[:6]=="/reply":
        command = input.split(" ")[1]
        c=0
        tot=""
        for word in input.split(" "):
            if c>1:
                tot += word+" "
            c+=1
        query = 'SELECT * FROM conversations WHERE texternumber ='+str(number)+'ORDER BY ASC'
        retval = dbquery(query)
        cid=retval[command]['ID']
        query = 'SELECT max(messagenumber) FROM messages WHERE conversationID = '+str(cid)
        retval = dbquery(query)
        msgs = retval[0]['max(messagenumber)']
        query = "INSERT INTO messages (conversationID, messagebody, sendertype, messagenumber) VALUES ("+str(cid)+", "+str(tot)+", 'texter', "+str(msgs+1)+")"
        dbinsert(query)
        return "Your reply has been sent"
def init(input, number):
    help =helpget(input)
    lis= txtlist(input, number)
    close=close(input, number)
    ask=ask(input, number)
    reply=reply(input)
    return str(help)+str(lis)+str(close)+str(ask)+str(reply)
