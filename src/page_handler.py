"""
Author: Joe Ingham
Last Modified: 05/12/2023
"""
import os

""""
This class loads and decodes the page info files
"""
class capa_page_handler:

    #Creates the object
    def __init__(self):
        #Stores the current page info
        self.loaded_page_name = "None"
        self.loaded_page_filepath = "None"
        self.strings = []
        self.images = []
        self.info = []
        self.pg_col = None
        self.pg_desc = None


    #Loads the config file and decodes it 
    #Returns all the relevant lists of items
    def load_page(self, file):
        
        #Clear the currently loaded strings and images
        self.strings = []
        self.images = []      
        

        #Set the base filepath to the correct one 
        
        base_filepath =  os.getcwd() + "/configs/"
        #Construct the filepath
        filepath = base_filepath + file + ".txt"
        
        print(filepath)

        #Try and open the file 
        try:
            config = open(filepath)

        except:
            print("ERROR: Page config load error")

        #Iterate through the lines in the file
        for line in config.readlines():
            line = line.strip("\n")           
            #Ignore lines with the hash in them
            if "#" in line:
                continue
            #! indicates page colour
            if "!" in line:                
                self.pg_col = line.split(" ", 1)[1].strip()                
                continue 
            #' indicates sector description
            if "@" in line:
                self.pg_desc = line.split(" ", 1)[1].strip("\n")
                continue

            #Split the line otherwise
            line_split = line.split(",")            
           

            #Add the splits to the appropriate list
            self.strings.append(line_split[0])
            self.images.append(line_split[1].strip())
            self.info.append(line_split[2].split("`"))
            

 

        return 


        

    
    def __str__(self):
        print(f"Page Handler - Current Page: {self.loaded_page_name}")








if __name__ == "__main__":
    print("Page handler")

    ph = capa_page_handler()

    ph.load_page("test.txt")

    print(ph.get_strings())
    print(ph.get_images())
