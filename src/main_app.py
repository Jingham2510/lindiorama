"""
Author: Joe Ingham
Last Updated: 12/12/2023
Version: 0.7
"""

import tkinter as tk
from PIL import Image, ImageTk
import os
import time
import sys
import platform

"""
The main applet that controls the raspberry pi for the Alaris Linwave Diorama
"""

#The main app - a child of the "tk" as this tends to be standard to tkinter applets
class app(tk.Tk):
    #The controller for the application
    def __init__(self):

        #Check the platform - determines the filepath for where the cwd is
        #OS.cwd() isn;t used here, as the code is run on startup by the raspberry pi from the root directory (the code is not stored there ATM)
        if "Windows" in platform.platform():
            print("Windows system")
            self.base_filepath = "P:/Joe/Python Scripts/diorama_app"
        else:
            print("Raspbian system")
            self.base_filepath = "/home/pi/diorama_app"

        #Create the window
        tk.Tk.__init__(self)
        #Setup the control flags 
        self.closed_flag = 0
        


        #Setup the window
        self.title = ("Linwave Diorama App")
        

        #Configure the main window
        self.grid_columnconfigure(0, weight=1)                 
        self.grid_rowconfigure(0, weight=1)   

        #Determine the starting frame     
        self._frame = None
        self.switch_frame(Start_Window)
        #Start the timer
        self.start_time = time.time()

        #Setup so escape key closes the program
        #DEBUG only - normally device in kiosk mode so won't have peripherals plugged in
        self.bind("<Escape>", self.on_close)

        #Hide the window bar and go fullscreen after 500ms
        self.after(500, lambda: self.attributes("-fullscreen", True))


    
    #Switches to the desired frame window
    def switch_frame(self, frame_class, *, arg = None):
        
        #Set the start page flag 
        self.start_flag = 0
        
        #Determines which frame to go to
        match arg:
            #Sector overview page            
            case ("MARINE" | "AVIATION" | "DEFENCE" | "INDUSTRIAL" | "MEDICAL" | "SATCOM") as s:
                print("overview page")
                new_frame = frame_class(self, s)
                
            
            #Futureprrofing for the possibility that the capabilities page is different
            case("CAPABILITIES") as s :
                print("capabilities page")
                new_frame = frame_class(self, s)
                
            #Go to the home page
            case("Return"):
                print("Home page")
                new_frame = frame_class(self)                   

            #Go to the specified page 
            case _:
                new_frame = frame_class(self)     
                
              
        
        #Destroys the current window (as long as it exists)
        if self._frame is not None:
            self._frame.destroy()
        

        #Creates the new frame and places it 
        self._frame = new_frame
        self._frame.grid(row = 0, column = 0, sticky = "NESW")


    #Get the current idle time on the page (i.e. how long the page has been open)
    def get_idle_time(self):
        return int(time.time() - self.start_time)
    
    #Set the flag so that the program knows the app has been closed
    def on_close(self, event):
        self.destroy()
        self.closed_flag = 1



#The start page
class Start_Window(tk.Frame):
    #Startup of the GUI - Start Window
    def __init__(self, master):             
               
        #Create the window and set the relevant flags
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.start_time = time.time()
        self.master.start_flag = 1 

        
        
        #The filepath where the screensavers are saved      
        ssavers_filepath = self.master.base_filepath + "/images/Screensavers/"

        #Generate a list of filepaths to loads the images from - based on all the images in the file 
        self.screensavers = [ f"{ssavers_filepath}{x}" for x in os.listdir(ssavers_filepath) if x[-3:] in ["png", "jpg"]]
        

        #Loads the first image in the generated list 
        self.curr_ssaver_index = 0
        display = Image.open(self.screensavers[self.curr_ssaver_index])
        display = display.resize((self.master.winfo_width(), self.master.winfo_height()))
        display = ImageTk.PhotoImage(display)
        self.curr_image = tk.Label(self, image = display)
        self.curr_image.grid(row=0, column=0, sticky="NEWS")        
        self.curr_image.photo = display
        
        
        #Sets the start time for the loaded image
        self.start_menu_time = time.time()

        #Binds mouse click 1 (or touchscreen click) to the menu swap
        self.curr_image.bind("<Button-1>", self._start_action)


    #Press start button to go to the main window
    def _start_action(self, event):
        print("changing page")
        self.master.switch_frame(Main_Window)

    #Loops through the screensavers
    def _next_image(self):
        print("Next slide")

        #Sets the start time
        self.start_menu_time = time.time()


        #Generates the next index
        if self.curr_ssaver_index == len(self.screensavers) - 1:
            self.curr_ssaver_index = 0            
        else:
            self.curr_ssaver_index = self.curr_ssaver_index + 1
            

        #Loads the next image
        display = Image.open(self.screensavers[self.curr_ssaver_index])
        display = display.resize((self.master.winfo_width(), self.master.winfo_height()))
        display = ImageTk.PhotoImage(display)
        self.curr_image = tk.Label(self, image = display)        
        self.curr_image.grid(row=0, column=0, sticky="NEWS")
        self.curr_image.photo = display        
        self.curr_image.bind("<Button-1>", self._start_action)



      

    
    #Return the time since the last screensaver changed
    def start_menu_tot_time(self):
        return int(time.time() - self.start_menu_time)

                


  

#The main overview window
class Main_Window(tk.Frame):

    #Load the main page 
    def __init__(self, master):
        
        tk.Frame.__init__(self, master)
        
        #Format the master
        self.master = master
        self.master.start_time = time.time()
    
        #Determine the filepath for the menu screen image
        overview_fp = self.master.base_filepath + "/images/menus/HomeScreen.png"

        #Load the menu screen image
        img = Image.open(overview_fp)
        img2 = img.resize((self.master.winfo_width(), self.master.winfo_height()))
        display = ImageTk.PhotoImage(img2)        
        curr_image = tk.Label(self, image = display)       
        curr_image.grid(row=0, column=0, sticky="NEWS")
        curr_image.resized_photo = display

        #Set the mouse to be bound to changing the screen
        curr_image.bind("<Button-1>", self._open_overview)

        
    


    #Open an overview page 
    def _open_overview(self, event):
        
        
        butt_label = ""

        #Get the coordinates of the click
        x = event.x
        y = event.y

        #Get page height and width
        page_width = self.winfo_width()
        page_height = self.master.winfo_height()

        #Ifelse rather than match because no pattern matching, always x,y format

        #Check if capabilities:
        if y >= page_height  * 3/4:
            butt_label = "CAPABILITIES"        


        #Check the x coordinate
        #Left half
        elif x <= page_width/2:
            #Defence Page
            if y < page_height * 1/4:
                butt_label = "DEFENCE"
            #Aviation Page
            if y > page_height * 1/4 and y < page_height / 2:
                butt_label = "AVIATION"            
            #Marine page
            elif y > page_height/2:
                butt_label = "MARINE"

        #Right half of the page
        elif x > page_width/2:
            #Medical Page
            if y < page_height * 1/4:
                butt_label = "MEDICAL"
            #Industrial Page
            if y > page_height * 1/4 and y < page_height / 2:
                butt_label = "INDUSTRIAL"
            #Sat comms page
            if y > page_height/2:
                butt_label = "SATCOM"        

     

        
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

        #Pick which page to show based on the page config

        overview_fp = self.master.base_filepath + "/images/menus/" + page_config + ".png"

        img = Image.open(overview_fp)
        img2 = img.resize((self.master.winfo_width(), self.master.winfo_height()))
        display = ImageTk.PhotoImage(img2)        
        curr_image = tk.Label(self, image = display)       
        curr_image.grid(row=0, column=0, sticky="NEWS")
        curr_image.resized_photo = display

        curr_image.bind("<Button-1>", self._open_overview)

 

    #Open an overview page 
    def _open_overview(self, event):
          
        butt_label = ""

        #Get the coordinates of the click
        x = event.x
        y = event.y


        

        #Get page height and width
        page_width = self.winfo_width()
        page_height = self.master.winfo_height()


        #Check that the click is at the top of the page
        if y < page_height * 1/8:
            
            if x < page_width * 1/7:
                butt_label = "MARINE"

            elif x > page_width * 1/7 and x < page_width * 2/7:
                butt_label = "AVIATION"

            elif x > page_width * 2/7 and x < page_width * 3/7:
                butt_label = "DEFENCE"

            elif x > page_width * 3/7 and x < page_width * 4/7:
                butt_label = "INDUSTRIAL"

            elif x > page_width * 4/7 and x < page_width * 5/7:
                butt_label = "MEDICAL"
            
            elif x > page_width * 5/7 and x < page_width * 6/7:
                butt_label = "SATCOM"
            
            elif x > page_width * 6/7: 
                butt_label = "CAPABILITIES"



        #If not exit the function        
        else:
            return    

        
        
        print(butt_label)

        #Open the relevant overview page
        #self.master.switch_frame(Overview_Window, arg = butt_label)

        #Open the relevant overview page
        self.master.switch_frame(Overview_Window, arg = butt_label)
        



if __name__ == "__main__":

    print("Main app starting up")    
    print(platform.platform())
    

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
                app._frame._next_image()


            #If a button hasn't been pressed in 60 seconds - and not currently on the start page
            if app.get_idle_time() > 60 and not app.start_flag:
                app.switch_frame(Start_Window)
                start_time = time.time()           

        except:
            break

    