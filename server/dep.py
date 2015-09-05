from flask import Flask, request, redirect, jsonify
import json
import MySQLdb as mdb
from txtcommands import init

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

class messaging():
	def __init__(self, phone_number, message):

		
		self.number = phone_number
		self.message = message
		
		self.con = mdb.connect('127.0.0.1', 'root', "emerson1", 'Pennapps');
		self.cur = con.cursor(mdb.cursors.DictCursor)

		user_data = self.is_new()
		if user_data != True:
			#TODO check if lang exsists if not reply is lang
			if  user_data['lang'] == 'null':
				user_data['lang'] = str(self.find_lang(self.message))
				query = "UPDATE `texters` set lang = " +  user_data['lang'] ", name = 'null' WHERE phone = " + self.number
				cur.execute(query)
				self.message = translate('en', user_data['lang'], "What is your name?") #TODO add translation function
			elif user_data['name'] == 'null':
				self.name = self.message
				query = "UPDATE `texters` set name = '" str(self.name) + "' WHERE phone = " + self.number
				cur.execute(query)
				self.message("Welcome " + self.name + " to see help, type /help, to ask a question, type /ask"
				
			self.user_data = user_data
		else:
			#TODO create conversation, message 
			#TODO ask name if name=null, set name in database, then after you check on all that stuff ask what is your question
			query = "INSERT INTO `texters` (lang, phone) VALUES 'null', '"  + str(self.number) + "'"
			cur.execute(query) 
			self.message = "What language do you speak?"
			#TODO call/write lang function

	def get_message():
		return self.message
	def is_new():
		query = "SELECT * FROM `texters` WHERE phone = '" + self.number + "' "
		cur.execute(query)
		results = cur.fetchone()
		if results != None and  len(results) > 0:
			return results
		else:
			return True

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


