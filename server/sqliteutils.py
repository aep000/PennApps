import MySQLdb as mdb
from flask import jsonify
import json

def register(info):
	mysql_conn =  mdb.connect('localhost', 'root', "emerson1", 'Pennapps')
	mysql_cursor = mysql_conn.cursor(mdb.cursors.DictCursor)
	query = "INSERT INTO `doctors` (name, user, password, specialty) VALUES ( '" + str(info['name'])  + "', '" + str(info['username']) + "' , '" + str(info['password']) + "', '" + str(info['specialty']) + "')"	
	print query 
	res = mysql_cursor.execute(query)
	mysql_conn.commit()
	return jsonify({"status":200})
	

def login(info):
	#try:
	mysql_conn =  mdb.connect('localhost', 'root', "emerson1", 'Pennapps')
	mysql_cursor = mysql_conn.cursor(mdb.cursors.DictCursor)
	query = "SELECT * FROM `doctors` WHERE user = '" + str(info['username']) + "' AND password = '" + str(info['password']) + "'" 
	res = mysql_cursor.execute(query)
	res = mysql_cursor.fetchone()
	if (res!=None) and (len(res) >0) :
		jreturn = json.dumps(res)
		print jreturn
	else:
		return jsonify({"login":"Invalid"})
	mysql_conn.commit()
	return (jreturn)

