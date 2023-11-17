import sqlite3

class DB():

	def Connect(self):
		self.connection = sqlite3.connect('Project_Database.db')
		self.cursor = self.connection.cursor()

	def Disconnect(self):
		self.connection.commit()
		self.connection.close()

	def AddCountyTable(self):
		self.Connect()
		self.cursor.execute("""CREATE TABLE Counties (State text, CountyName text)""")
		self.Disconnect()

	def AddCodeTable(self):
		self.Connect()
		self.cursor.execute("""CREATE TABLE Codes (CodeName text, ShortName text, Year integer)""")
		self.Disconnect()

	def AddWebsiteTable(self):
		self.Connect()
		self.cursor.execute("""CREATE TABLE Websites (CountyName text, Website text, CodeDirectory text, Lookup date)""")
		self.Disconnect()

	def AddAdoptedCodesTable(self):
		self.Connect()
		self.cursor.execute("""CREATE TABLE Adopted (CountyName text, CodeName text, Year text, Adopted date)""")
		self.Disconnect()

	def AddScrapesTable(self):
		self.Connect()
		self.cursor.execute("""CREATE TABLE Scrapes (CountyName text, ScrapeDate date, AdoptedCodeName text, AdoptedCodeYear text, Adopted date)""")
		self.Disconnect()

	def AddRecord(self, ScrapeInfo):
		self.Connect()
		self.cursor.execute("""INSERT INTO Scrapes VALUES(:CountyName, :ScrapeDate, :AdoptedCodeName, :AdoptedCodeYear, :Adopted)""",
				{
					'CountyName': ScrapeInfo[0],
					'ScrapeDate': ScrapeInfo[1],
					'AdoptedCodeName': ScrapeInfo[2],
					'AdoptedCodeYear': ScrapeInfo[3],
					'Adopted': ScrapeInfo[4]
				}
			)
		self.Disconnect()

	def UpdateAdoptedCodes(self):
		self.Connect()
		# Code to compare recently scraped data w/ existing and update tables accordingly
		self.Disconnect()


