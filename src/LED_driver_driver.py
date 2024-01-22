"""
Author: Joe Ingham
Version: 0.0.1
Date Created: 13/12/2023
Date Modified: 15/1/2023
Description: Raspberry Pi "LED Driver" driver software
"""
#Imports for Raspberry Pi
#import board
#import busio
#import adafruit_tlc59711


class LED_driver:



    #Creates the LED driver
    def __init__(self):

        #Create the spi lines
        spi = busio.SPI(board.SCK, MOSI=board.MOSI)

        #Create the LED driver "object"
        #Need to figure out the number of LEDS and which is which (requires the pi)
        LED_COUNT = 24

        driver = adafruit_tlc59711.TLC59711(spi, LED_COUNT)

        pass


    #External class to let the gui pick a led mode
    def set_led_mode(self, mode):

        #Match the mode to the correct function
        match mode:
            case "DEFENCE":
                self._defence_mode()
 
            case "AVIATION":
                self._aviation_mode()

            case "MARINE":
                self._marine_mode()

            case "MEDICAL":
                self._medical_mode()

            case "INDUTRIAL":
                self._industrial_mode()

            case "SATCOM":
                self._satcom_mode()

            case "CAPABILITIES":
                self._capabilities_mode()

            #If anything else set the LEDS to default
            case _:
                self._default_mode()
                



    #Turns on the Defence LEDs
    def _defence_mode(self):
        pass
    
    
    #Turns on the Aviation LEDs
    def _aviation_mode(self):
        pass


    #Turns on the Marine LEDs
    def _marine_mode(self):
        pass


    #Turns on the Medical LEDs
    def _medical_mode(self):
        pass

    #Turns on the Industrial LEDs
    def _industrial_mode(self):
        pass

    #Turns on the SATCOM LEDs
    def _satcom_mode(self):
        pass

    #Turns on the Capabilities LEDs
    def _capabilities_mode(self):
        pass

    #Turns on the default LEDs
    def _default_mode(self):
        pass