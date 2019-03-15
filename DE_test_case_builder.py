import tkinter as gui
import os
import sys
import platform
import json
from tkinter import *
from tkinter import filedialog


def get_json_file_path(default_path):
   file_path = filedialog.askopenfilename(initialdir=default_path)

   return file_path


class JSON_EDITOR:
   def __init__(self, master=None):
      self.master = master
      self.default_path = os.path.dirname(os.path.abspath(__file__))
      self.save_path = self.default_path

      self.build_gui()

      return

   def build_gui(self):
      # BUILD MAIN FRAME
      main_frame = gui.Tk(className='DE TOOL')

      # BUILD LIST OF TEST CASES

      # BUILD LIST OF TEST CASE STEPS

      # BUILD EDITOR OF STEP

      # ACTIVATE GUI
      main_frame.mainloop()


      # top = tkinter.Tk(className='DE_Tool')
      # top_menu = TopMenu(master=top)
      # top.mainloop()
      #
      # self.btn_edit_json = tkinter.Button(self.master, text="LOAD JSON", command=self.edit_json)
      # self.btn_edit_json.pack()
      #
      # self.btn_create_json = tkinter.Button(self.master, text="CREATE JSON", command=self.create_json)
      # self.btn_create_json.pack()
      #
      # # Build new window
      # menu_json = tkinter.Tk(className='EDIT JSON FILE')
      #
      # file_path_title = Label(menu_json, text=self.save_path)
      # file_path_title.pack(fill=X)
      #
      # lb_index = Label(master=menu_json)
      #
      # lb_name = Label(master=menu_json, text='Tên mô tả: ')
      # input_name = Entry(master=menu_json)
      #
      # lb_type = Label(master=menu_json, text='Loại thao tác')
      # types = {
      #    'url': 'URL',
      #    'input': 'nhập',
      #    'click': 'click',
      #    'drag_drop_by_index': 'kéo thả theo index',
      #    'click_by_index': 'click theo index'
      # }
      #
      # inputs_type = []
      # for type, type_label in types.items():
      #    input_type = Radiobutton(master=menu_json, text=type_label)
      #    input_type.pack(side=LEFT)
      #
      # cases = Listbox(master=menu_json)
      #
      # b = Button(menu_json, text="Delete",
      #            command=lambda x=cases: cases.delete(ANCHOR))
      #
      # b.pack()
      #
      # for i in range(len(self.test_cases)):
      #    cases.insert(i, self.test_cases[i]['name'])
      #
      #
      #
      # cases.pack(side=BOTTOM, fill=X)
      # menu_json.mainloop()
      return


gui = JSON_EDITOR()
