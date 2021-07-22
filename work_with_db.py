
from mysql.connector import MySQLConnection, Error
from todo_app_dbconfig import read_db_config


def connect():
	""" Connect to MySQL database """
	dbConfig= read_db_config()
	conn = None
	try:
		print('Connecting to MySQL database...')
		conn = MySQLConnection(**dbConfig)

		if conn.is_connected():
			print('Connection established.')
		else:
			print('Connection failed.')

	except Error as error:
		print(error)
	# finally:
	# 	if conn is not None and conn.is_connected():
	# 		conn.close()
	# 		print('Connection closed.')
	return conn


def show_tables():
	# connect to database and get the cursor
	conn= connect()
	cur= conn.cursor(dictionary=True)

	sqlEntry= 'SHOW TABLES;'
	cur.execute(sqlEntry)
	output= cur.fetchall()
	conn.close()
	return output


def create_db_table(tableName):
	# connect to database and get the cursor
	conn= connect()
	cur= conn.cursor(dictionary=True)

	sqlEntry= 'CREATE TABLE %s (TaskID INT NOT NULL AUTO_INCREMENT, TaskTitle varchar(50), ToDueDate datetime, CreatedBy int, DoneBy int, PRIMARY KEY (TaskID))'%tableName
	cur.execute(sqlEntry)
	output= cur.fetchall()
	conn.close()
	return output


def read_table(tableName):
	# connect to database and get the cursor
	conn= connect()
	cur= conn.cursor(dictionary=True)

	sqlEntry= 'SELECT * FROM %s;'%tableName
	cur.execute(sqlEntry)
	output= cur.fetchall()
	conn.close()
	return output


def insert_todo_task(tableName, newEntry, userID, dueDate):
	# connect to database and get the cursor
	conn= connect()
	cur= conn.cursor()

	sqlEntry= "INSERT INTO %s (TaskTitle, CreatedBy, ToDueDate) VALUES ('%s', %s, '%s');"%(tableName, newEntry, userID, dueDate)
	cur.execute(sqlEntry)
	conn.commit()
	conn.close()


def update_todo_task(tableName, entryTitle, dueDate, taskID):
	# connect to database and get the cursor
	conn= connect()
	cur= conn.cursor()

	sqlEntry= "UPDATE %s SET TaskTitle='%s', ToDueDate='%s' WHERE taskID=%s;"%(tableName, entryTitle, dueDate, taskID)
	cur.execute(sqlEntry)
	conn.commit()
	conn.close()


def complete_todo_task(tableName, taskID, doneBy):
	# connect to database and get the cursor
	conn= connect()
	cur= conn.cursor()

	sqlEntry= "UPDATE %s SET DoneBy=%s WHERE taskID=%s;"%(tableName, doneBy, taskID)
	cur.execute(sqlEntry)
	conn.commit()
	conn.close()


def delete_todo_task(tableName, taskID):
	# connect to database and get the cursor
	conn= connect()
	cur= conn.cursor()

	sqlEntry= "DELETE FROM %s WHERE TaskID=%s;"%(tableName, taskID)
	cur.execute(sqlEntry)
	conn.commit()
	conn.close()

# if __name__ == '__main__':
# 	#connect()
# 	tableName= 'own_todo_list'
# 	newEntry= 'test mySQL'
# 	newEntryDesc= 'testing the db'
# 	userID= 0
# 	insert_todo_task(tableName, newEntry,newEntryDesc, userID)
# 	a= read_table()
# 	print(a)
	