"""
SQLite3
USER-ID, THEME , COINS , EMAIL
"""

import sqlite3 as sql
import os

class DB:
	# check if db exists

	def __init__(self, db_name:str="app-user.db"):

		self.db_name:str = ""
		self.conn:sql.Connection = None
		self.cursor:sql.Cursor = None

		if not os.path.exists(db_name):
			print("Database does not exist : CREATING ONE....")
			self.conn = sql.connect(db_name)
			self.db_name = db_name
			self.cursor = self.conn.cursor()
			# create table
			self.create_table()
			#insert sample 
			self.insert(user_id= "d2f-13980" , theme = "Drak" , coins=100 , email="smaple123@zap.com")


		else:
			self.conn = sql.connect(db_name)
			self.db_name = db_name
			self.cursor = self.conn.cursor()
			print("Database exists : CONNECTED TO IT....")
		
	### Private methods
	def create_table(self):
		'''
		CREATE A TABLE THAT CONSISTS OF COLUMNS : USER-ID, THEME , COINS , EMAIL
		'''
		self.cursor.execute("CREATE TABLE IF NOT EXISTS USER (user_id TEXT PRIMARY KEY UNIQUE, theme TEXT, coins INTEGER, email TEXT)")
		self.conn.commit()
	
	def insert(self, user_id, theme, coins, email):
		'''
		INSERT A NEW ROW INTO THE TABLE
		usage: 1.fetch_data() -> result 2.update_db(result+updated_data)
		'''
		self.cursor.execute("INSERT INTO USER (user_id, theme, coins, email) VALUES (?, ?, ?, ?)", (user_id, theme, coins, email))
		self.conn.commit()

	def close_db(self):
		'''
		CLOSE THE CONNECTION TO THE DATABASE
		'''
		self.conn.close()

	### Public methods
	def update_db(self, user_id, theme, coins, email):
		'''
		UPDATE THE ROW IN THE TABLE
		'''
		self.cursor.execute("UPDATE USER SET theme = ?, coins = ?, email = ? WHERE user_id = ?", (theme, coins, email, user_id))
		self.conn.commit()
	
	def fetch_data(self):
		'''
		FETCH ALL THE ROWS FROM THE TABLE
			"user_id": str,
			"theme": str,
			"coins": int,
			"email": str
		'''
		self.cursor.execute("SELECT * FROM USER")
		_:list=self.cursor.fetchall()
		return {
			"user_id":_[0][0],
			"theme":_[0][1],
			"coins":_[0][2],
			"email":_[0][3]
		}




db = DB()
# db.__init__()
print(db.fetch_data())