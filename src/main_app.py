"""
Author: Joe Ingham
Last Updated: 06/12/2023
"""

import tkinter as tk
from PIL import Image, ImageTk
import page_handler as ph 
import os
import time
import sys

"""
The main applet that controls the raspberry pi for the Alaris Linwave Diorama
"""

class app(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.closed_flag = 0
        #Set the CWD correctly (i.e. up one)
        os.chdir("../")  

        #Setup the window
        self.title = ("Linwave Diorama App")
        self.geometry("576x317")

        #Configure the main window
        self.grid_columnconfigure(0, weight=1)                 
        self.grid_rowconfigure(0, weight=1)   

        #Determine the starting frame     
        self._frame = None
        self.switch_frame(Start_Window)
        self.start_time = time.time()

        #Setup so escape key closes the program
        self.bind("<Escape>", self.on_close)

        #Hide the window bar and go fullscreen after 500ms
        self.after(500, lambda: self.attributes("-fullscreen", True))


    
    #Switches to the desired frame window
    def switch_frame(self, frame_class, *, arg = None):
        
        self.start_flag = 0
        
        #Create the class correctly
        match arg:
            #Sector overview page
            
            case ("MARINE" | "AVIATION" | "DEFENCE" | "INDUSTRIAL" | "MEDICAL" | "SPACE") as s:
                print("overview page")
                new_frame = frame_class(self, s)
                
            
            #Incase the capabilities and services page is different
            case("Capabilities") as s :
                print("capabilities page")
                new_frame = frame_class(self, s)
                

            case("Return"):
                print("Home page")
                new_frame = frame_class(self)                   

            case _:
                new_frame = frame_class(self)     
                
              
        
        #Destroys the current window
        if self._frame is not None:
            self._frame.destroy()
        #Swaps to the next one 
        self._frame = new_frame
        self._frame.grid(row = 0, column = 0, sticky = "NESW")

    #Get the current idle time on the page
    def get_idle_time(self):
        return int(time.time() - self.start_time)
    
    #Set the flag so that the program knows to close
    def on_close(self, event):
        self.destroy()
        self.closed_flag = 1




class Start_Window(tk.Frame):
    #Startup of the GUI - Start Window
    def __init__(self, master):             
               
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.start_time = time.time()
        self.master.start_flag = 1 

        
        
        #The filepath where the screensavers are saved
        #On the Pi : /home/pi/diorama_app/images/Screemsavers/
        ssavers_filepath = "P:/Joe/Python Scripts/diorama_app/images/Screensavers/"

        self.screensavers = [ f"{ssavers_filepath}{x}" for x in os.listdir(ssavers_filepath)]
        print(self.screensavers)

        self.curr_ssaver_index = 0
        image = Image.open(self.screensavers[self.curr_ssaver_index])
        img2 = image.resize((self.winfo_width(), self.winfo_height()))
        display = ImageTk.PhotoImage(img2)
        self.curr_image = tk.Label(self, image = display)        
        self.curr_image.image = display
        self.curr_image.grid(row=0, column=0, sticky="NEWS")
        

        self.start_menu_time = time.time()

       
        self.curr_image.bind("<Button-1>", self._start_action)


    #Press start button to go to the main window
    def _start_action(self, event):
        print("chaging page")
        self.master.switch_frame(Main_Window)


    def _next_image(self):
        print("Next slide")

        self.start_menu_time = time.time()

        if self.curr_ssaver_index == len(self.screensavers) - 1:
            self.curr_ssaver_index = 0            
        else:
            self.curr_ssaver_index = self.curr_ssaver_index + 1
            

        image = Image.open(self.screensavers[self.curr_ssaver_index])
        img2 = image.resize((self.winfo_width(), self.winfo_height()))
        display = ImageTk.PhotoImage(img2)
        self.curr_image = tk.Label(self, image = display)        
        self.curr_image.image = display
        self.curr_image.grid(row=0, column=0, sticky="NEWS")
        self.curr_image.bind("<Button-1>", self._start_action)

        print(self.curr_image)

    
    #Return the time since the last screensaver cjagem
    def start_menu_tot_time(self):
        return int(time.time() - self.start_menu_time)

                


  


class Main_Window(tk.Frame):

    #Load the main page 
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        #Format the master
        self.master = master
        self.master.start_time = time.time()

        
        #Configure the columns
        for i in range(6):
            self.grid_columnconfigure(i, weight=1)        
        #Configure the rows
        self.grid_rowconfigure(0, weight=1)       



        #Iteratively create the 6 buttons - predetermined titles/colours
        BUTTON_TITLES = ["MARINE", "AVIATION", "DEFENCE", "INDUSTRIAL", "MEDICAL", "SPACE"]
        BUTTON_COLOURS = ["pale green", "light goldenrod", "seashell3", "powder blue", "coral1", "firebrick1"]

        button_list = []
        row = 0
        curr_column = 0        

        #Create all the buttons
        for title in BUTTON_TITLES:
            #Creates the button
            button = tk.Button(self, text=title, command=lambda title = title: self._open_overview(title), bg=BUTTON_COLOURS[curr_column], height="10")
            button.grid(row = row, column = curr_column, sticky="NESW")
            button.grid_columnconfigure(curr_column, weight=1)
            self.grid_columnconfigure(curr_column, weight = 1)
            button_list.append(button)
            curr_column = curr_column + 1


        #Create the bottom button
        title = "Capabilities"
        button = tk.Button(self, text= title, command=lambda title = title: self._open_overview(title), bg="OrangeRed2", width=15)
        button.grid(row = 2, columnspan=6, sticky="NESW")
        button_list.append(button)

        



    #Open an overview page 
    def _open_overview(self, butt_label):
        
        print(butt_label)       

        #Open the relevant overview page
        self.master.switch_frame(Overview_Window, arg = butt_label)



"""
Window that displays the overview of the market sector
"""
class Overview_Window(tk.Frame):
    def __init__(self, master, page_config):
        #Create the frame
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.start_time = time.time()


        #Remove slashes 
        self.page_config = page_config
        

        try:
            self._load_page()
        except:
            print("ERROR: Page loading error")

        #GUI 
        #Set the page colour        
        self["bg"] = self.page_col
        
        #Create top row buttons
        #Iteratively create the 6 buttons - predetermined titles/colours
        BUTTON_TITLES = ["MARINE", "AVIATION", "DEFENCE", "INDUSTRIAL", "MEDICAL", "SPACE", "Capabilities"]
        BUTTON_COLOURS = ["pale green", "light goldenrod", "seashell3", "powder blue", "coral1", "firebrick1", "OrangeRed2"]

        button_list = []
        row = 0
        curr_column = 0        

        #Create all the buttons on the top row (and the bits beneath them)
        for title in BUTTON_TITLES:
            #Creates the button
            button = tk.Button(self, text=title, command=lambda title = title: self._open_overview(title), bg=BUTTON_COLOURS[curr_column], height="1")
            button.grid(row = row, column = curr_column, sticky="NESW")
            button.grid_columnconfigure(curr_column, weight=1)
            button.grid_rowconfigure(row, weight = 1)
            self.grid_columnconfigure(curr_column, minsize= 5,weight = 1)
            button_list.append(button)

            self.update()
            

            #Determine whether the spot below should be grey or not
            blank_lab = tk.Label(self, text=" " * button.winfo_width() * 8) 
            blank_lab.grid(row = row + 1, column = curr_column)

            if title == self.page_config:
                blank_lab["bg"] = BUTTON_COLOURS[curr_column]
            else:
                blank_lab["bg"] = "lavender"

            curr_column = curr_column + 1
        


        #Place the product description label
        desc_label = tk.Label(self, text=self.page_desc, bg = self.page_col, wraplength = 500, font = ("Arial", 10))
        
        desc_label.grid(row=2, rowspan = 2, columnspan=7, sticky="NESW")
        

        #Place the product title line
        prod_label = tk.Label(self, text="Products", bg = "lavender")
        prod_label.grid(row = 5, columnspan=7, stick = "NESW")


        frame_list = []

        
        base_filepath = os.getcwd()
        #Create new frames holding the images the name and the info
        #Create a new frame
        generic_frame = tk.Frame(self, bg = self.page_col, highlightbackground="black", highlightthickness=0)
        for i in range(len(self.strings)):
            


            #Place the label
            label = tk.Label(generic_frame, text=self.strings[i], bg = self.page_col)
            
            label.grid(row = 0, column = i)
            
            #Place the image
            #Get the filepath of the image
            #On pi ~ base_filepath = "/home/pi/diorama_app/image/ + self.images[i]"
            filepath = base_filepath + "/images/" + self.images[i]            
            #Open the image and resize it 
            img = Image.open(filepath)
            resized_img = img.resize((100, 75), Image.Resampling.NEAREST)
            img2 = ImageTk.PhotoImage(resized_img)            
            
            #Place the image in a label in a computed spot
            label = tk.Label(generic_frame, image = img2, bg = self.page_col)
            
            label.grid(row = 1, rowspan = 2, column = i, pady =2)        
            label.image = img2   
            label.grid_rowconfigure(1, weight=1)
            label.grid_columnconfigure(1, weight=1)

            #Place the information
            #Create the text for the label
            b = "•"
            text = ""
            for inf in self.info[i]:
                text = text + b + inf + "\n"

            label = tk.Label(generic_frame, text=text, bg=self.page_col)
            
            label.grid(row = 3, rowspan=2, column = i)            

            frame_list.append(generic_frame)




        #Place the frame into the mainframe            
        generic_frame.grid(row = 6, rowspan = 3, column = 0, columnspan=8)
        






    #Loads all the relevant information onto the page
    #Updates the images and the labels on the page
    def _load_page(self):

        #Create the page handler
        handle = ph.capa_page_handler()
        #Have the page handler load all the releveant information
        handle.load_page(self.page_config)

        #Get the strings and the filepaths for the images
        self.strings = handle.strings
        self.images = handle.images
        self.info = handle.info
        self.page_col = handle.pg_col
        self.page_desc = handle.pg_desc
        

        #Check that the lengths are the same
        if len(self.strings) != len(self.images):
            raise Exception("Strings/Images not matching")
        
        #Load complete
        loaded = 1 

        return loaded
    

    #Open an overview page 
    def _open_overview(self, butt_label):
        
        print(butt_label)       

        #Open the relevant overview page
        self.master.switch_frame(Overview_Window, arg = butt_label)



if __name__ == "__main__":

    print("Main app starting up")    
  
    

    app = app()

    while True:

        app.update_idletasks()
        app.update()

        #Try and get the idle time - if not break the loop
        try:
            if app.closed_flag:
                sys.exit()           


            #If on the main page - every 5 seconds change the image
            if app.start_flag and (x := app._frame.start_menu_tot_time()) > 0 and x % 5 == 0:
                print("CHANGE")
                app._frame._next_image()


            #If a button hasn't been pressed in 60 seconds
            if app.get_idle_time() > 60:
                app.switch_frame(Start_Window)
                start_time = time.time()           

        except:
            break

    