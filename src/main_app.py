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

class app(tk.Tk):
    def __init__(self):

        #Check the 
        if "Windows" in platform.platform():
            print("Windows system")
            self.base_filepath = "P:/Joe/Python Scripts/diorama_app"
        else:
            print("Raspbian system")
            self.base_filepath = "/home/pi/diorama_app"


        tk.Tk.__init__(self)
        #self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.closed_flag = 0
        #Set the CWD correctly (i.e. up one)


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
        ssavers_filepath = self.master.base_filepath + "/images/Screensavers/"

        self.screensavers = [ f"{ssavers_filepath}{x}" for x in os.listdir(ssavers_filepath)]
        

        self.curr_ssaver_index = 0
        display = Image.open(self.screensavers[self.curr_ssaver_index])
        display = display.resize((self.master.winfo_width(), self.master.winfo_height()))
        display = ImageTk.PhotoImage(display)
        self.curr_image = tk.Label(self, image = display)
        self.curr_image.grid(row=0, column=0, sticky="NEWS")        
        self.curr_image.photo = display
        
        

        self.start_menu_time = time.time()

       
        self.curr_image.bind("<Button-1>", self._start_action)


    #Press start button to go to the main window
    def _start_action(self, event):
        print("changing page")
        self.master.switch_frame(Main_Window)


    def _next_image(self):
        print("Next slide")

        self.start_menu_time = time.time()

        if self.curr_ssaver_index == len(self.screensavers) - 1:
            self.curr_ssaver_index = 0            
        else:
            self.curr_ssaver_index = self.curr_ssaver_index + 1
            

        display = Image.open(self.screensavers[self.curr_ssaver_index])
        display = display.resize((self.master.winfo_width(), self.master.winfo_height()))
        display = ImageTk.PhotoImage(display)
        self.curr_image = tk.Label(self, image = display)        
        self.curr_image.grid(row=0, column=0, sticky="NEWS")
        self.curr_image.photo = display        
        self.curr_image.bind("<Button-1>", self._start_action)

      

    
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
    
        overview_fp = self.master.base_filepath + "/images/menus/HomeScreen.png"

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

        coords = (event.x, event.y)
        print(coords)

        #Hardcoded :(
        #Calibrated to match the touchscreen image coords
        match coords:
            #Marine Button
            case coords as x, y if x < (self.master.winfo_width()/2) and y > (self.master.winfo_height()/2) and y < (self.master.winfo_height() * 3/4):
                print("SCORE")
                butt_label = "MARINE"
                
            case coords as x, y if y > 200:
                print("MISS")
                return
            case _:
                return           

        
             


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
        
        coords = (event.x, event.y)

        #Hardcoded :(
        #Calibrated to match the touchscreen image coords
        match coords:
            case coords as x, y if y < 200:
                print("SCORE")
                return
            case coords as x, y if y > 200:
                print("MISS")
                return
            case _:
                return               

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


            #If a button hasn't been pressed in 60 seconds
            if app.get_idle_time() > 60:
                app.switch_frame(Start_Window)
                start_time = time.time()           

        except:
            break

    