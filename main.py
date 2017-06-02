from database import Database

if __name__ == "__main__":
	
	db = Database()
	db.connect()
	db.disconnect()
	db.create_table()
	db.connect()
	db.insert_customer('John', 'python', '11111111111', 'john@gmail.com')
	db.insert_customer('Durant', 'javascript', '22222222222', 'durant@gmail.com')
	db.search_customer('11111111111')
	db.remove_customer('22222222222')
	db.search_email('durant@gmail.com')
	db.search_customer('11111111111')
