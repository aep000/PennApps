import MySQLdb as mdb

def register(info):
	mysql_conn =  mdb.connect('45.79.138.244', 'root', "emerson1", 'Pennapps')
	mysql_cursor = mysql_con.cursor(mdb.cursors.DictCursor)
	query = "INSERT INTO `doctors` (username, password) VALUES ('" + str(info['username']) + "' , '" + str(info['password']) + "')"	
	print query 
	res = mysql_cursor.execute(query)
	mysql_conn.commit()
	return (response)
	

def login(username, password):
	mysql_conn =  mdb.connect('localhost', 'root', "I8~8(IV)RU}Pf.O=9G51<IOgm)9z", 'Pennapps')
	mysql_cursor = mysql_con.cursor(mdb.cursors.DictCursor)
	query = "SELECT * FROM `doctors` (username, password)" 
	print query 
	res = mysql_cursor.execute(query)
	res = cur.fetchall()
	if len(res) >0:
		jreturn = json.dumps(res)
	mysql_conn.commit()
	return (jreturn)
	


	

