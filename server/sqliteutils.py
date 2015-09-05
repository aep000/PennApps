import MySQLdb as mdb

def register(username, password):
	mysql_conn =  mdb.connect('localhost', 'root', "I8~8(IV)RU}Pf.O=9G51<IOgm)9z", 'Pennapps')
	mysql_cursor = mysql_con.cursor(mdb.cursors.DictCursor)
	query = "INSERT INTO `doctors` (username, password) VALUES ('" + str(username) + "' , '" + str(password) + "')"	
	print query 
	res = mysql_cursor.execute(query)
	mysql_conn.commit()
	


	

