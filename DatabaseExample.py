import os
import sys
import sqlite3
if sys.version_info[0] >= 3:
	import tkinter as tk
	from tkinter.ttk import *
else:
	import Tkinter as tk
	from Tkinter.ttk import *

class ProjectLookup():
	def __init__(self):
		self.DB = DB()
		self.DisplayProjects()
		self.Egnyte = os.path.join('//','Shared','Projects')
		self.ProjectNo = str(input('Enter Project Number:'))

		self.Directory = self.CheckDatabase(self.ProjectNo)

		if self.Directory == None:
			self.Directory = self.BuildFilePath(self.ProjectNo)
			self.ProjectInfo = self.Format(self.Directory)
			self.DB.AddRecord(self.ProjectInfo)
		else:
			print(self.Directory)

		self.OpenDirectory(self.Directory)
		
	def DisplayProjects(self):
		try:
			for i, Project in enumerate(self.DB.GetProjects()):
				print('{i}.) {No} - {Name}'.format(i=i+1,No=Project[0],Name=Project[1]))
		except TypeError:
			return

	def BuildFilePath (self, ProjectNo):
		frst = ProjectNo[0:2] + '000-' + ProjectNo[0:2] + '999'
		scnd = ProjectNo[0:3] + '00-' + ProjectNo[0:3] + '99'

		try:
			Parent = os.path.join(self.Egnyte,frst,scnd)
		except FileNotFoundError:
			return(None)

		for Project in os.listdir(Parent):
			if Project[0:5] != ProjectNo:
				continue
			else:
				directory = os.path.join(Parent,Project)
				directory = os.path.realpath(directory)
				return(directory)
		return(None)

	def OpenDirectory(self, directory):
		if os.path.isdir(directory) == True:
			os.startfile(directory)
		else:
			return(None)

	def CheckDatabase(self, ProjectNo):
		return(self.DB.GetProjectFilePath(ProjectNo))

	def Format(self, Directory):
		ProjectInfo = ['','','']
		ProjectInfo[2] = Directory
		ProjectInfo[1] = Directory[Directory.index(self.ProjectNo)+6:]
		ProjectInfo[0] = self.ProjectNo
		return(ProjectInfo)

class DB():
	#def __init__(self):		

	def Connect(self):
		self.connection = sqlite3.connect('Project_Database.db')
		self.cursor = self.connection.cursor()

	def Disconnect(self):
		self.connection.commit()
		self.connection.close()

	def AddTable(self):
		self.Connect()
		self.cursor.execute("""CREATE TABLE Projects (ProjectNo text, ProjectName text, Directory text)""")
		self.Disconnect()

	def AddRecord(self, ProjectInfo):
		self.Connect()
		self.cursor.execute("""INSERT INTO Projects VALUES(:ProjectNo, :ProjectName, :Directory)""",
				{
					'ProjectNo': ProjectInfo[0],
					'ProjectName': ProjectInfo[1],
					'Directory': ProjectInfo[2]
				}
			)
		self.Disconnect()

	def DeleteRecord(self, ProjectInfo):
		self.Connect()
		sql_delete_query = """
				DELETE FROM Projects WHERE ProjectNo =?
			"""
		try:
			self.cursor.execute(sql_delete_query, (ProjectInfo[0]))
		except sqlite3.OperationalError:
			self.Disconnect()
		else:
			self.Disconnect()

	def GetProjectFilePath(self, ProjectNo):
		self.Connect()
		sql_select_query = """
				SELECT Directory FROM Projects WHERE ProjectNo =?
			"""
		try:
			self.cursor.execute(sql_select_query, (ProjectNo,))
		except sqlite3.OperationalError:
			self.Disconnect()
			self.AddTable()
			return(None)
		else:
			try:
				return(self.cursor.fetchone()[0])
			except TypeError:
				return(None)
		self.Disconnect()

	def GetProjects(self):
		self.Connect()
		sql_select_query = """
				SELECT DISTINCT * FROM Projects
			"""
		self.cursor.execute(sql_select_query)
		return(self.cursor.fetchall())
		self.Disconnect()

ProjectLookup()