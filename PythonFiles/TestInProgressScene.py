# Imports all the necessary modules
import tkinter as tk
from tkinter import ttk
from xml.dom.expatbuilder import parseFragmentString
import sys

# Imports the ConsoleOutput class and its functions
from PythonFiles.ConsoleOutput import *

# Creating the frame itself
class TestInProgressScene(tk.Frame):

    def __init__(self, parent, master_frame, data_holder):
        
        self.data_holder = data_holder
        self.is_current_scene = False
        self.initialize_scene(parent, master_frame)

    # A function to be called within GUIWindow to create the console output
    # when the frame is being brought to the top
    def initialize_console(self):

        global console_popup

        # Creating a popup window for the console output
        console_popup = tk.Tk()
        console_popup.geometry("300x300+975+200")
        console_popup.title("Console Output Window")
        console_popup.wm_attributes('-toolwindow', 'True')

        # Used to tell the console window that its 
        # exit window button is being given a new function
        console_popup.protocol('WM_DELETE_WINDOW', self.fake_destroy)

        # Creating a Frame For Console Output
        frm_console = tk.Frame(console_popup, width = 300, height = 300, bg = 'black')
        frm_console.pack_propagate(0)
        frm_console.pack()

        # Giving the console output a scroll bar
        scrollbar = tk.Scrollbar(frm_console)
        scrollbar.pack(side = "right", fill = 'y')


        # Placing an entry box in the frm_console
        global ent_console
        ent_console = tk.Text(
            frm_console, 
            bg = 'black', 
            fg = 'white', 
            font = ('Arial', 8),
            yscrollcommand = scrollbar.set
            )
        ent_console.pack(anchor = 'center', fill = tk.BOTH, expand = 1)

        # Adding scrollbar functionality
        scrollbar.config(command = ent_console.yview)

        # Instantiates the console writing class
        console = ConsoleOutput(ent_console)

        # replace sys.stdout with our new console object
        sys.stdout = console

    # A pass function that the console window is being redirected to so its exit button
    # does not function
    def fake_destroy(self):
        pass

    # A Function to be called when the console should be destroyed
    def console_destroy(self):
        
        # Redirects any console readouts back to the actual console rather than the fake object
        sys.stdout = sys.__stdout__
        
        # Destroys the console output window
        console_popup.destroy()
        

    # Used to initialize the frame that is on the main window
    # next_frame is used to progress to the next scene and is passed in from GUIWindow
    def initialize_scene(self, parent, master_frame):
        super().__init__(master_frame, width = 850, height = 500)


        # Creating the main title in the frame
        lbl_title = tk.Label(self, 
            text = "Test in progress. Please wait.", 
            font = ('Arial', 20)
            )
        lbl_title.pack(padx = 0, pady = 100)

        # Create a progress bar that does not track progress but adds motion to the window
        prgbar_progress = ttk.Progressbar(
            self, 
            orient = 'horizontal',
            mode = 'indeterminate', length = 350)
        prgbar_progress.pack(padx = 50)
        prgbar_progress.start()

        # A Button To Stop the Progress Bar and Progress Forward (Temporary until we link to actual progress)
        btn_stop = ttk.Button(
            self, 
            text='Stop', 
            command= lambda: self.btn_stop_action(parent))
        btn_stop.pack(padx = 0, pady = 100)

        # Forces the frame to stay the size of the master_frame
        self.pack_propagate(0)

    # A function for the stop button
    def btn_stop_action(self, _parent):

        _parent.go_to_next_test()

        
        # Destroys the console window
        self.console_destroy()
        
        


    # Goes to the next scene after the progress scene is complete
    def go_to_next_frame(self, _parent):
        _parent.go_to_next_test()

        

    # Used to bring the user back to the test that just failed
    def go_to_previous_frame(self, _parent, previous_frame):
        self.previous_frame = previous_frame
        _parent.set_frame(previous_frame)

    

     

    # Dummy Script Function
    def run_test_gen_resist(self):
        print ("General Resistance Test Run")

    # Dummy Script Function
    def run_test_id_resistor(self):
        print ("ID Resistor Test Run")

    # Dummy Script Function
    def run_test_i2c_comm(self):
        print("I2C Comm. Test Run") 

    # Dummy Script Function
    def run_test_bit_rate(self):
         print("Bit Rate Test Run")

    
    def update_frame(self, parent):
        self.initialize_console()