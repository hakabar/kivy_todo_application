
#ToDo Application Using the kivy MD Library
#from kivy_todo_application.work_with_db import update_todo_task
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, TwoLineAvatarIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.properties import StringProperty
import shelve
from kivymd.icon_definitions import md_icons
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
import time
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.picker import MDDatePicker
from datetime import datetime
from kivymd.uix.menu import MDDropdownMenu
# -- Added by DAL --
import mysql.connector
from mysql.connector import Error
from work_with_db import show_tables, read_table, create_db_table, insert_todo_task, update_todo_task, complete_todo_task, delete_todo_task
from kivymd.uix.menu import MDDropdownMenu, RightContent
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty


def toast(text):
    from kivymd.toast.kivytoast import toast
    toast(text)


class Home(GridLayout):
	dialog = None
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.cols = 1


class CustomToolbar(ThemableBehavior, RectangularElevationBehavior, MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = self.theme_cls.primary_color


class RightContentCls(RightContent):
    pass


class NewTableDialog(BoxLayout):
	"""Opens a dialog box asking for the name and users of for the new table"""
	def __init__(self, widget=None, **kwargs):
		super().__init__(**kwargs)
		self.widget=widget
		self.ids.new_table_name.text= str(self.widget.text)

	def open_new_table_dialog(self):
		print("inside open_new_tabla_dialog")
		self.dialog = MDDialog(
			title='Create new table',
			type="custom", 
			content_cls=NewTableDialog(widget=self.widget), 
			size_hint=[.95, .5],
		)
		self.dialog.open()		

	def close_dialog(self):
		self.dialog.dismiss()
# ---- End Class NewTableDialog ----


class TaskDetailDialog(BoxLayout):
	"""OPENS A DIALOG BOX WITH TASK DETAILS"""
	def __init__(self, currentTable, widget=None, **kwargs):
		super().__init__(**kwargs)
		self.widget=widget
		self.currentTable= currentTable
		self.ids.task_detail_text.text = str(self.widget.text)
		self.ids.task_detail_date.text = str(self.widget.secondary_text)
		
	def open_edit_dialog(self):
		self.dialog = MDDialog(
			title='Edit Task',
			type="custom", 
			content_cls=TaskEditDialog(self.currentTable, widget=self.widget), 
			size_hint=[.95, .5],
		)
		self.dialog.open()

	def delete_task_dialog(self):
		self.delete_dialog = MDDialog(
			title='Delete Item',
			type="custom", 
			content_cls=ConfirmDelete(self.currentTable, widget=self.widget), 
			size_hint=[.95, .5],
		)
		self.delete_dialog.open()

	def close_dialog(self):
		self.dialog.dismiss()
# ---- End Class TaskDetailDialog ----


class TaskEditDialog(BoxLayout):
	"""OPENS A DIALOG BOX TO EDIT A SELECTED TASK"""

	def __init__(self, currentTable, widget=None, **kwargs):
		super().__init__(**kwargs)
		self.widget = widget
		self.currentTable= currentTable
		self.ids.edit_task_text.text = self.widget.text
		self.ids.edit_date_text.text = self.widget.secondary_text
		self.pk = int(self.widget.pk)
	

	def show_date_picker(self):
		"""Opens the date picker, duh"""
		date_dialog = MDDatePicker(callback=self.get_date)
		date_dialog.open()


	def get_date(self, date):
		"""This functions gets the date from the date picker and converts its it a
		more friendly form then changes the date label on the dialog to that"""
		date = date.strftime('%Y-%m-%d')
		self.ids.edit_date_text.text = str(date)
		print(date)


	def save_task_data(self):
		self.widget.text = str(self.ids.edit_task_text.text)
		self.widget.secondary_text = str(self.ids.edit_date_text.text)
		self.save_edit_data_to_file()
		Snackbar(text='Task Saved!').show()  


	def save_edit_data_to_file(self):
		entryName= self.ids.edit_task_text.text
		dueDate= self.ids.edit_date_text.text
		taskID= self.pk
		update_todo_task(self.currentTable, entryName, dueDate, taskID)
# ---- End Class TaskEditDialog ----


class DialogContent(BoxLayout):
	"""OPENS A DIALOG BOX THAT GETS THE TASK FROM THE USER"""
	def __init__(self,currentTable, **kwargs):
		super().__init__(**kwargs)
		#self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))
		self.ids.date_text.text = str(datetime.now().strftime("%Y-%m-%d"))
		self.currentTable= currentTable

	def save_task(self, value):
		the_task = Task(value)
		the_task.save_data_entry(self.currentTable)
	
	def show_date_picker(self):
		"""Opens the date picker, duh"""
		date_dialog = MDDatePicker(callback=self.get_date)
		date_dialog.open()

	def get_date(self, date):
		"""This functions gets the date from the date picker and converts its it a
		more friendly form then changes the date label on the dialog to that"""
		date= date.strftime("%Y-%m-%d")
		self.ids.date_text.text = str(date)	
# ---- End Class DialogContent ----


class ListItemWithCheckbox(TwoLineAvatarIconListItem):
	"""Custom list item"""
	icon = StringProperty('bullseye')

	def __init__(self,check = False, pk=1, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ids.check.active = check
		self.pk = pk


class RightCheckbox(IRightBodyTouch, MDCheckbox):
	'''Custom right container'''


class ConfirmDelete(BoxLayout):
	""""""
	def __init__(self, currentTable, widget=None, **kwargs):
		super().__init__(**kwargs)
		self.widget = widget
		self.currentTable= currentTable

	def delete_the_task(self):
		self.widget.parent.remove_widget(self.widget)
		self.delete_data_in_file()

		Snackbar(text= 'Task Deleted!').show()

	def delete_data_in_file(self):
		taskID= self.widget.pk
		delete_todo_task(self.currentTable, taskID)
# ---- End Class COnfirmDelete ----


# --- TASK LOGIC ---
class Task:
	"""This class is responsible for creating a task"""
	def __init__(self, task=None, date=None, completed=False, pk=1):
		self.task = str(task)
		self.completed = completed
		self.date = date
		self.pk = pk
	
	def save_data_entry(self, tableName):
		""" Method to save information into the DB """
		try:	
			#DB params
			userID=0
			newEntry= self.task
			dueDate=self.date
			insert_todo_task(tableName, newEntry, userID, dueDate)
			#self.ids.newToDo.text=""
			#self.ids.newToDoDesc.text=""
			#self.ids.ownList.add_widget(ListItemWithCheckbox(text=newEntry))
		except Exception as e:
				print(e)

	def retrive_everything(self, tableName):
		todoList=None
		try:
			todoList= read_table(tableName)
			return todoList
		except KeyError:
			print('Todo tasks db table empty')
			return todoList
# ---- End Class Task ----



class MainApp(MDApp):

	dialog = None
	tableName= 'own_todo_list'
	listTables= ObjectProperty()#None
	newListTxt="New TODO list"
	lastestTaskID= 0		#To keep track for the next taskID to use (when adding a todo task to the list)

	def build(self):
		self.theme_cls.primary_palette = "Indigo"
		self.theme_cls.accent_palette = 'Green'
		self.root = root = Home()
		return root

	def create_menu(self, instance):
		print("inside create_menu() ")
		self.listTables= show_tables()
		menu_items = [
			{
				"right_content_cls": RightContentCls(
					# Used to display the todo list selection menu on the top left (why/how? no idea)
					text=f"R+{self.listTables[i]['Tables_in_todo_app']}", icon="apple-keyboard-command",
				),
				"icon": "git",
				"text": self.listTables[i]['Tables_in_todo_app'],
			} for i in range(len(self.listTables))
		]
		menu_items.append({
			"right_content_cls": RightContentCls(
				# Used to display the todo list selection menu on the top left (why/how? no idea)
				text="", icon="apple-keyboard-command",
			),
			"icon": "git",
			"text": self.newListTxt,
			}	
		)
		return MDDropdownMenu(caller=self.root.ids.toolbar.ids.btnList, items=menu_items, callback= self.refresh_todo_list, width_mult=5)


	def on_start(self, currTable= None):
		#print("inside on_START")
		todoList=None
		# Look for the different todo lists for current user
		self.listTables= show_tables()

		if currTable:
			todoList= Task().retrive_everything(currTable)
			self.menuList = self.create_menu(self.root.ids.toolbar.ids.btnList)
		else:
			todoList= Task().retrive_everything(self.tableName)
			self.menuList = self.create_menu(self.root.ids.toolbar.ids.btnList)

		null='null'
		if todoList:
			for todo in todoList:
				try:
					self.lastestTaskID= max(self.lastestTaskID, todo['TaskID'])
					if todo['DoneBy']:
						self.root.ids.completed_container.add_widget(
								ListItemWithCheckbox(text=todo['TaskTitle'], secondary_text="Due: "+str(todo['ToDueDate'].strftime('%A %b %Y')) , check=True, pk=todo['TaskID']))
					elif not todo['DoneBy']:
						self.root.ids.container.add_widget(
								ListItemWithCheckbox(text=todo['TaskTitle'], secondary_text="Due: "+str(todo['ToDueDate'].strftime('%A %b %Y')), pk=todo['TaskID']))
				except TypeError:
					continue


	def refresh_todo_list(self, instance):
		#Fct to decide if a new todo list must be loaded or if a new todo list must be created
		self.tableName= instance.text
		if self.tableName == self.newListTxt:
			#IF user selected "New TODO list" option, open the dialog window
			# to create a new table (not yet implemented/debugged)
			#self.show_new_table_dialog()
			pass
		else:
			self.load_current_todo_list()


	def create_new_todo_list(self):
		# Fct to create a new table 
		print("inside mainApp.create_new_todo_list")
		self.clean_todo_list()
		create_db_table(self.ids.new_table_name.text) #Not finished!!!! WE NEED TO PASS IT THE TABLENAME THAT WE WROTE INT HE DIALOG WINDOW

	def clean_todo_list(self):
		#Remove tasks from previous list (displayed in screen)
		for i in range(len(self.root.ids.container.children)-1, -1,-1):
			self.root.ids.container.remove_widget(self.root.ids.container.children[i])
		for i in range(len(self.root.ids.completed_container.children)-1, -1,-1):
			self.root.ids.completed_container.remove_widget(self.root.ids.completed_container.children[i])		


	#def load_current_todo_list(self, textOnDropDownItem):
	def load_current_todo_list(self):
			print('inside load_current_todo_list')
			print("Inside load_current_todo_list: table reading: %s"%self.tableName)

			# Clean the current todo task displayed
			self.clean_todo_list()
			 
			#Load the todo task for the new list 
			todoList= Task().retrive_everything(self.tableName)
			null='null'
			if todoList:
				for todo in todoList:
					try:
						if todo['DoneBy']:
							self.root.ids.completed_container.add_widget(
									ListItemWithCheckbox(text=todo['TaskTitle'], secondary_text="Due: "+str(todo['ToDueDate'].strftime('%A %b %Y')) , check=True, pk=todo['TaskID']))
						elif not todo['DoneBy']:
							self.root.ids.container.add_widget(
									ListItemWithCheckbox(text=todo['TaskTitle'], secondary_text="Due: "+str(todo['ToDueDate'].strftime('%A %b %Y')), pk=todo['TaskID']))
					except TypeError:
						continue


	def menu_callback(self, *args):
		print(args[0])
		toast(args[0])	#Check funtion on top of the script


	def show_new_table_dialog(self, widget):
		"""Shows the new table creation dialog"""
		self.dialog = MDDialog(title="Create a new TODO list", 
		type="custom", 
		content_cls=NewTableDialog(widget), 
		size_hint=[.95, .8],
		auto_dismiss=False,
		)
		self.dialog.open()


	def show_task_dialog(self):
		"""Shows the task creation dialog"""
		self.dialog = MDDialog(title="Create a new task", 
		type="custom", 
		content_cls=DialogContent(self.tableName), 
		size_hint=[.95, .8],
		auto_dismiss=False,
		)
		self.dialog.open()
	
	def close_dialog(self):
		"""Closes the task creation dialog"""
		self.dialog.dismiss()

	def save_task(self, value, date):
		"""Saves tasks by creating a list item and adding it to the container"""
		try:
			if value and date:
				pk= self.lastestTaskID+1	#Next TaskID to be assigned
				self.root.ids.container.add_widget(ListItemWithCheckbox(text=value, secondary_text="Due: "+date, pk=pk))

				Task(value, date, pk=pk).save_data_entry(self.tableName)
				Snackbar(text="Your Task Has Been Saved").show()
			else:
				MDDialog(title="Alert",
					text='Please add a task name!',
					size_hint=[.9, None]
				).open()

		except KeyError:
			if value and date:
				self.root.ids.container.add_widget(ListItemWithCheckbox(text=value, secondary_text="Due: "+date, pk=1))

				Task(value, date).save_data_entry(self.tableName)
				Snackbar(text="Your Task Has Been Saved").show()
			
			else:
				MDDialog(title="Alert",
					text='Please add a task name!',
					size_hint=[.9, None]
				).open()
			
		
	def confirm_delete_task(self, widget):
		self.root.ids.container.remove_widget(widget)


	def mark(self, instance_check, widget):
		"""Does something when the task checkbox is marked or unmarked (in the not completed or completed task lists)"""
		if instance_check.active == True:
			#Task finished (task will move from the unfinished list to the finished)
			self.root.ids.container.remove_widget(widget)
			self.root.ids.completed_container.add_widget(widget)
			Snackbar(text="Task Complete").show()
			# update the information in the db table file 
			doneBy= 1
			taskID= widget.pk
			complete_todo_task(self.tableName, taskID, doneBy)

		elif instance_check.active == False:
			#Cancel task completion (task will move from the finished list to the unfinished)
			self.root.ids.completed_container.remove_widget(widget)
			self.root.ids.container.add_widget(widget)
			Snackbar(text="Task Unmarked!").show()
			# update information in the DB table 
			doneBy= 'null'
			taskID= widget.pk
			complete_todo_task(self.tableName, taskID, doneBy)
			

	def show_detail(self, widget):
		"""Shows the details of a selected task"""
		self.detail_dialog = MDDialog(
			title="Task Detail", 
			type="custom", 
			content_cls=TaskDetailDialog(self.tableName, widget=widget),
			size_hint=[.8, .8],
			auto_dismiss=True,
		)

		self.detail_dialog.open()


	def close_detail_dialog(self):
		"""Closes the task detail dialog"""
		self.detail_dialog.dismiss()

		





MainApp().run()