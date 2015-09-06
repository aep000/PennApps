from flask import Flask, request, redirect, jsonify
import json
import MySQLdb as mdb
import csv
from twilio.rest import TwilioRestClient

def send_sms(to_number, the_body):
        account_sid = "AC7a14830568ec769f5f68d7d3d2ac7287"
        auth_token = "3a0cd8283b0788e463e43f6fcab93f46"
        client = TwilioRestClient(account_sid, auth_token)

        message = client.messages.create(to=to_number, from_="+19087524729",
                                     body=the_body)
        return True


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
		self.cur = self.con.cursor(mdb.cursors.DictCursor)

		user_data = self.is_new()
		print user_data
		if user_data != True:
				#TODO check if lang exsists if not reply is lang
				if  user_data['lang'] == 'null':
					user_data['lang'] = str(self.find_lang(self.message))
					query = "UPDATE `texters` set lang = " +  user_data['lang'] + ", name = 'null' WHERE phone = " + self.number
					self.cur.execute(query)
					self.message = translate('en', user_data['lang'], "What is your name?") #TODO add translation function
				elif user_data['name'] == 'null':
					self.name = self.message
					query = "UPDATE `texters` set name = '" + str(self.name) + "' WHERE phone = " + self.number
					self.cur.execute(query)
					self.message = "Welcome " + self.name + " to see help, type /help, to ask a question, type /ask"
					
				else:
					self.user_data = user_data
					#ind out language
					eng = self.from_lang(self.message, 'en',  user_data['lang'])
					txtcommands.init(end, self.number)
					self.message = self.from_lang("The doctor has received your message and will be replying shortly", user_data['lang'], 'en')
					

		else:	
		
			#TODO create conversation, message 
			#TODO ask name if name=null, set name in database, then after you check on all that stuff ask what is your question
			query = "INSERT INTO `texters` (lang, phone) VALUES ('null', '"  + str(self.number) + "')"
			self.cur.execute(query) 
			self.message = "What language do you speak?"
			self.con.commit()
			#TODO call/write lang function

	def get_message(self):
		return self.message
	def is_new(self):
		query = "SELECT * FROM `texters` WHERE phone = '" + self.number + "' "
		print query
		self.cur.execute(query)
		results = self.cur.fetchone()
		if results != None and  len(results) > 0:
			return results
		else:
			return True

	def helpget(self, input):
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
	def txtlist(self, input, number):
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
	
	
	def fix_message(self, message):
		message = message.split(" ")
		message = message[0]
		message = message.lower()
		mchar = message[0]
		message = message[1:(len(message) +1 )]
		mchar.upper()
		message = mchar + message
		return message



	
	def get_list(self):
		lang_list = {
			'Spanish':'es',
			'Srench' : 'fr',
			'Danish' : 'da',
			'Aymaran' : 'ay',
			'English' : 'en'
		}
		return lang_list

	def find_lang(self, target):	
		message = self.fix_message(self.message)
		lang_json = self.get_list()
			
		if message not in lang_json:
			return "en"#When it's invalid default to english
		else:
			return lang_json['message']
	def translate(to_translate, target, source):
		gs = goslate.Goslate()
		return  gs.translate(to_translate, target_language, source_language)

