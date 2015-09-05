import MySQLdb as mdb

def register(info):
	mysql_conn =  mdb.connect('localhost', 'root', "emerson1", 'Pennapps')
	mysql_cursor = mysql_con.cursor(mdb.cursors.DictCursor)
	query = "INSERT INTO `doctors` (username, password) VALUES ('" + str(info['username']) + "' , '" + str(info['password']) + "')"	
	print query 
	res = mysql_cursor.execute(query)
	mysql_conn.commit()
	


	

