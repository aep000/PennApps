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
	con.close()

def helpget(input):
	#/help
	if input[:5] == "/help":
		ret = """
		/reply - Reply to a doctor's response.
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
			ret += "c) "+retval2[0]['name']+": "+chat['question']+"\n"
			c+=1
		return ret
'''
@app.route("/doclist", methods=['GET', 'POST'])
def doclist():
	register_info = request.data
	Datadict = json.loads(register_info)
	start=Datadict['amount']
	specialty = Datadict['special']
	tot ="{"
	query="SELECT * FROM conversations WHERE ID > max(ID)-"+amount+" ORDER BY ID DESC"
	retval = dbquery(query)
	c=0
	for conv in retval:
		query= "SELECT * FROM messages WHERE conversationID = "+str(conv['ID'])
		retval2 = dbquery(query)
		if len(retval2) == 1:
			query = "SELECT * FROM texters WHERE phone = "+conv['texternumber']
			retval3 = dbquery(query)
			tot += '"'str(c)+'": { "question": "'+conv[question]+'", "sendername": "'+retval3[0]['name']+'"},'
	tot = tot[:-1]
	tot += "}"
	return tot
'''
def fix_message(message):
	message = message.split(" ")
	message = message[0]
	message = message.lower()
	mchar = message[0]
	message.pop(0)
	mchar.upper()
	message = mchar + message
	return message

def get_list():
	lang = open('language-codes.json')
	lang = lang.read()
	lang_json = json.dumps(lang)
	lang_json = {v: k for k, v in map.items()}# Invert the dictionary
	return lang_json



def find_lang(message):	
	message = fix_message(message)
	lang_json = get_list()
	
	if message not in lang_json:
		return "en"#When it's invalid default to english
	else:
		return lang_json['message']

find_lang('')
