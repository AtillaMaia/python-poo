import sqlite3
import logging

class MetaSingleton(type):
	"""This Metaclass represents a Singleton, design pattern that
	   control the instantiation of a class.
	"""
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]	

class Database(metaclass=MetaSingleton):
	"""Simple database SQLite3"""

	def __init__(self, name='database.db'):
		self.name = name
		self.conn = None

		FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
		logging.basicConfig(filename='db.log', filemode='w', format=FORMAT, datefmt="%d/%m/%Y %I:%M:%S %p", level=logging.DEBUG)
		self.logger = logging.getLogger(__name__)
	
	def connect(self):
		"""Connects a database"""
		try: 
			self.conn = sqlite3.connect(self.name)
			self.logger.info('Database connected')
		except sqlite3.OperationalError as e:
			print('Cannot connect to database: %s' % e)
			self.logger.error('Database cannot be connected')

	def disconnect(self):
		"""Disconnect a database"""
		try:
			self.conn.close()
			self.logger.info('Database closed')
		except AttributeError as e:
			print('Cannot disconnect to the database: %s' % e)
			self.logger.error('Database cannot be closed')

	def create_table(self):
		"""Creates a table in the database"""
		try:
			cursor = self.conn.cursor()

			cursor.execute("""
			CREATE TABLE IF NOT EXISTS customers (
					id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
					name TEXT NOT NULL,
					password VARCHAR(20) NOT NULL,
					cpf VARCHAR(11) UNIQUE NOT NULL,
					email TEXT NOT NULL
			);
			""")
			self.conn.commit()
			self.logger.info('Table was created')			
		except (AttributeError, sqlite3.ProgrammingError) as e:
			print('Cannot create a table before connecting to the database: %s' % e)
			self.logger.exception('%s' % e)

	def insert_customer(self, name, password, cpf, email):
		"""Inserts a customer into the database"""
		try:
			cursor = self.conn.cursor()

			try:
				cursor.execute("""
					INSERT INTO customers (name, password, cpf, email) VALUES (?,?,?,?)
				""", (name, password, cpf, email))

				self.conn.commit()
				self.logger.info('Customer inserted')
			except sqlite3.IntegrityError:
				print('CPF %s already exists' % cpf)
				self.logger.warn('Customer already exists')
		except (AttributeError, sqlite3.ProgrammingError) as e:
			print('Cannot insert into a table before connecting to the database: %s' % e )
			self.logger.exception('%s' % e)

	def search_customer(self, cpf):
		"""Finds a customer by your CPF"""
		try:
			cursor = self.conn.cursor()

			cursor.execute("SELECT * FROM customers WHERE cpf=?", (cpf,))

			cliente = cursor.fetchone()
			
			if cliente:
				print('Customer %s.' % cliente[1])
				self.logger.info('Customer found')
				return True
			else:
				print('Customer does not exist')
				self.logger.warn('Customer not found')
				return False
		except (AttributeError, sqlite3.ProgrammingError) as e:
			print('Cannot find a customer before connecting to the database: %s' % e)
			self.logger.exception('%s' % e)

	def remove_customer(self, cpf):
		"""Deletes a customer by your CPF"""
		try:
			cursor = self.conn.cursor()

			cursor.execute("DELETE FROM customers WHERE cpf=?", (cpf,))

			self.conn.commit()

			if cursor.rowcount > 0:
				print('Customer deleted successfully.')
				self.logger.info('Customer deleted')
			else:
				print("Customer is not registered.")
				self.logger.warn('Customer not deleted')
		except (AttributeError, sqlite3.ProgrammingError) as e:
			print('Cannot delete a customer before connecting to the database: %s' % e)
			self.logger.exception('%s' % e)

	def search_email(self, email):
		"""Finds a customer by your email"""
		try:
			cursor = self.conn.cursor()

			cursor.execute("SELECT * FROM customers WHERE email=?", (email,))

			cliente = cursor.fetchone()
			
			if cliente:
				print('Customer %s.' % cliente[1])
				self.logger.info('Customer found')
				return True
			else:
				print('Customer does not exist')
				self.logger.warn('Customer not found')
				return False

		except (AttributeError, sqlite3.ProgrammingError) as e:
			print('Cannot find a customer before connecting to the database: %s' % e)
			self.logger.exception('%s' % e)
