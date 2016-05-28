from tkinter import *
from os import walk
from os import path
from os import remove
from os import makedirs
import shutil
from PIL import Image, ImageTk

directory = 'G:/'


def configure_img():
	temp = {}

	rsrc = './PNG/'

	temp_img = rsrc + 'filetype-folder.gif'
	temp['folder'] = PhotoImage(file = temp_img)

	temp_img = rsrc + 'filetype-blank.gif'
	temp['nil'] = PhotoImage(file = temp_img)

	temp_img = rsrc + 'filetype-image.gif'
	temp['.png'] = PhotoImage(file = temp_img)
	temp['.jpg'] = PhotoImage(file = temp_img)
	temp['.gif'] = PhotoImage(file = temp_img)
	temp['.bmp'] = PhotoImage(file = temp_img)
	temp['.psd'] = PhotoImage(file = temp_img)
	temp['.kra'] = PhotoImage(file = temp_img)

	temp_img = rsrc + 'filetype-archive.gif'
	temp['.7z'] = PhotoImage(file = temp_img)
	temp['.zip'] = PhotoImage(file = temp_img)
	temp['.rar'] = PhotoImage(file = temp_img)

	temp_img = rsrc + 'filetype-application.gif'
	temp['.exe'] = PhotoImage(file = temp_img)

	temp_img = rsrc + 'filetype-spreadsheet.gif'
	temp['.accdb'] = PhotoImage(file = temp_img)

	temp_img = rsrc + 'filetype-settings-1.gif'
	temp['.bat'] = PhotoImage(file = temp_img)

	temp_img = rsrc + 'filetype-web.gif'
	temp['.html'] = PhotoImage(file = temp_img)

	temp_img = rsrc + 'filetype-text.gif'
	temp['.txt'] = PhotoImage(file = temp_img)

	return temp


class FileSuite:
	def __init__(self, parent):

		self.toolbar = Toolbar(self, parent)

		panes = PanedWindow(orient = HORIZONTAL)
		panes.pack(fill = BOTH, expand = 1)

		files = Frame(panes)
		panes.add(files)

		preview = Frame(panes)
		panes.add(preview)

		self.preview = Preview(preview)

		self.file_view = ListView(files, self.preview)

	def root(self):
		self.file_view.root_path()

	def create_folder(self):
		top = Toplevel()
		top.geometry('{}x{}'.format(200, 80))
		top.title("New Folder")

		msg = Message(top, text = "Please type a folder name", width = 200)
		msg.pack(fill = X)

		# v = StringVar()

		entry = Entry(top)
		entry.pack(fill = X)
		entry.focus_set()

		frame = Frame(top)
		frame.pack(fill = X)

		b_confirm = Button(frame, text = "Okay", command = lambda: self.c2(entry.get(), top, msg))
		b_confirm.pack(side = RIGHT)
		b_cancel = Button(frame, text = "Cancel", command = top.destroy)
		b_cancel.pack(side = LEFT)

	def c2(self, name, top, alert):
		if name != "":
			self.file_view.create_folder(name)
			top.destroy()
			self.file_view.repopulate()
		else:
			alert["text"] = "You must enter a folder name"

	def create_file(self):
		top = Toplevel()
		top.geometry('{}x{}'.format(200, 80))
		top.title("New File")

		msg = Message(top, text = "Please type a file name", width = 200)
		msg.pack(fill = X)

		# v = StringVar()

		entry = Entry(top)
		entry.pack(fill = X)
		entry.focus_set()

		frame = Frame(top)
		frame.pack(fill = X)

		b_confirm = Button(frame, text = "Okay", command = lambda: self.c1(entry.get(), top, msg))
		b_confirm.pack(side = RIGHT)
		b_cancel = Button(frame, text = "Cancel", command = top.destroy)
		b_cancel.pack(side = LEFT)

	def c1(self, name, top, alert):
		if name != "":
			self.file_view.create_file(name)
			top.destroy()
			self.file_view.repopulate()
		else:
			alert["text"] = "You must enter a file name"


class Toolbar:
	def __init__(self, suite, parent):
		self.frame = Frame(parent)
		self.frame.pack(fill = X)

		self.button_new_file = Button(self.frame, text = "New File", command = suite.create_file)
		self.button_new_file.pack(side = LEFT)

		self.button_new_folder = Button(self.frame, text = "New Folder", command = suite.create_folder)
		self.button_new_folder.pack(side = LEFT)

		self.button_root = Button(self.frame, text = "...", command = suite.root)
		self.button_root.pack(side = LEFT)


class Preview:

	def preview_txt(self, directory):
		print("dir: " + directory)
		self.view.pack_forget()
		self.message["text"] = directory
		f = open(directory, 'r')
		self.view = Text(self.frame)
		self.view.insert(INSERT, f.read())
		self.view.pack(fill = BOTH, expand = 1)
		self.view["state"] = DISABLED
		print(f.read())
		f.close()

	def __init__(self, parent):
		self.frame = Frame(parent)
		self.frame.pack(fill = BOTH, expand = 1)
		self.previews = {
			'.txt': self.preview_txt,
			'.html': self.preview_txt,
			'.bat': self.preview_txt,
			'.py': self.preview_txt,
			'': self.preview_txt,
		}
		self.message = Message(self.frame, text = "[No File Selected]", width = 100)
		self.message.pack()
		self.view = Frame(self.frame)
		self.view.pack(fill = BOTH, expand = 1)

	def preview(self, directory, file):
		_, file_ext = path.splitext(file)
		print(directory[-1:])
		if directory[-1:] == '/':
			calculated_directory = directory + file
		else:
			calculated_directory = directory + '/' + file
		print(file_ext)
		if file_ext.lower() in self.previews:
			self.previews[file_ext.lower()](calculated_directory)


class FolderView:
	def __init__(self, parent):
		self.frame = Frame(parent)
		self.frame.pack(side = LEFT)

		list_view = ListView(self.frame)


def get_directory(path):
	d = []
	f = []

	for (dir_path, dir_names, file_names) in walk(path):
		d.extend(dir_names)
		f.extend(file_names)
		break

	return d, f


class ListView:

	def go_to(self, loc):
		if self.directory[len(self.directory) - 1] == '/':
			self.directory = self.directory + loc
		else:
			self.directory = self.directory + '/' + loc
		self.reset_scroll()
		self.repopulate()

	def root_path(self):

		if not self.directory[len(self.directory) - 1] == '/':
			for i in range(len(self.directory)):
				if self.directory[i] == '/':
					x = i
			self.directory = self.directory[:x]
			print(self.directory)
			if self.directory[len(self.directory) - 1] == '/' and self.directory.count('/') > 1:
				self.directory = self.directory[:len(self.directory) - 1]
			if len(self.directory) == 2:
				self.directory += '/'
			self.reset_scroll()
			self.repopulate()

	def reset_scroll(self):
		self.canvas.pack_forget()
		self.frame.pack_forget()
		self.scrollbar.pack_forget()
		self.canvas = Canvas(self.parent)

		self.frame = Frame(self.canvas)
		self.frame.pack(fill = BOTH, expand = 1)

		self.scrollbar = Scrollbar(self.parent, orient = VERTICAL, command = self.canvas.yview)
		self.canvas.configure(yscrollcommand = self.scrollbar.set, scrollregion = self.canvas.bbox("all"))
		self.scrollbar.pack(side = RIGHT, fill = Y)

		self.canvas.pack(side = LEFT, fill = BOTH, expand = 1)
		self.canvas.create_window((0, 0), window = self.frame, anchor = N + W)

		self.frame.bind(
			"<Configure>",
			lambda event: self.canvas.configure(yscrollcommand = self.scrollbar.set, scrollregion = self.canvas.bbox("all"))
		)

	def __init__(self, parent, preview):
		self.directory = 'G:/'
		self.view = []
		self.prev = preview
		self.parent = parent

		self.canvas = Canvas(self.parent)

		self.frame = Frame(self.canvas)
		self.frame.pack(fill = BOTH, expand = 1)

		self.scrollbar = Scrollbar(parent, orient = VERTICAL, command = self.canvas.yview)
		self.canvas.configure(yscrollcommand = self.scrollbar.set, scrollregion = self.canvas.bbox("all"))
		self.scrollbar.pack(side = RIGHT, fill = Y)

		self.canvas.pack(side = LEFT, fill = BOTH, expand = 1)
		self.canvas.create_window((0, 0), window = self.frame, anchor = N + W)

		self.frame.bind(
			"<Configure>",
			lambda event: self.canvas.configure(yscrollcommand = self.scrollbar.set, scrollregion = self.canvas.bbox("all"))
		)

		self.repopulate()

	def delete_folder(self, direct):
		shutil.rmtree(direct)
		self.repopulate()

	def delete_file(self, direct):
		remove(direct)
		self.repopulate()

	def create_folder(self, directory):
		new_path = self.directory + '/' + directory
		if not path.exists(new_path):
			makedirs(new_path)

	def repopulate(self):
		print(self.directory)
		for v in self.view:
			v.pack_forget()

		d, f = get_directory(self.directory)
		spacer = "   "
		dirs = []
		for directory in d:
			i = len(dirs)
			b = Button(
				self.frame,
				image = img_dict['folder'],
				text = spacer + directory,
				compound = LEFT,
				anchor = W
			)
			dirs.append(directory)
			b.configure(command = lambda this = b: this.focus_set())
			b.bind("<Double-Button-1>", lambda x, ind = i: self.go_to(dirs[ind]))
			b.bind("<Delete>", lambda x, ind = i: self.delete_folder(self.directory + '/' + dirs[ind]))
			b.pack(fill = X, expand = 1)
			self.view.append(b)

		for file in f:
			_, file_ext = path.splitext(file)

			temp = Button(
				self.frame,
				text = spacer + file,
				image = img_dict.get(file_ext.lower(), img_dict.get('nil', None)),
				compound = LEFT,
				anchor = W
			)
			temp.configure(command = lambda this = temp: this.focus_set())
			temp.bind("<Delete>", lambda x, f = file: self.delete_file(self.directory + f))

			temp.bind("<Double-Button-1>", lambda x, f = file: self.prev.preview(self.directory, f))
			temp.pack(fill = X, expand = 1)
			self.view.append(temp)

	def create_file(self, name):
		open(self.directory + '/' + name, 'a')


root = Tk()
root.geometry('{}x{}'.format(1000, 800))

img_dict = configure_img()

file_suite = FileSuite(root)

mainloop()