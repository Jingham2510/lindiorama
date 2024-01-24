"""
Author: Joe Ingham
Version: 0.0.2
Date Created: 13/12/2023
Date Modified: 15/1/2023
Description: Raspberry Pi "LED Driver" driver software
"""
#Imports for Raspberry Pi
#import board
#import busio
#import digitalio
#import adafruit_tlc5947
import random
import datetime


class LED_driver:



    #Creates the LED driver
    def __init__(self):

        #Create the spi lines
        self.spi = busio.SPI(.clock = board.SCK, MOSI = board.MOSI)
        self.latch = digitalio.DigitialInOut(board.D22)

        #Create the LED driver "object"      

        self.driver = adafruit_tlc5947.TLC5947(self.spi, self.latch)

        #Define the LED numbers and there respective groups
        self.aviation_group = (0, 1, 2, 3)
        self.defence_group = (4, 5, 8, 9, 10, 11)
        self.industry_group =(6, 7)
        self.marine_group = (12, 18, 19, 20, 21, 21 ,23)
        self.space_group = (13, 14)
        self.medical_group = (15, 16, 17)


        


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

            case mode in "CAPABILITIES":
                self._capabilities_mode()

            case "RANDOM":
                self._random_mode()

            #If anything else set the LEDS to default
            case _:
                self._default_mode()
                



    #Turns on the Defence LEDs
    def _defence_mode(self):
        self._turn_all_off()
        for i in self.defence_group:
            self.driver[i] = 4095
    
    
    #Turns on the Aviation LEDs
    def _aviation_mode(self):
        self._turn_all_off()

        for i in self.aviation_group:
            self.driver[i] = 4095


    #Turns on the Marine LEDs
    def _marine_mode(self):
        self._turn_all_off()

        for i in self.marine_group:
            self.driver[i] = 4095


    #Turns on the Medical LEDs
    def _medical_mode(self):
        self._turn_all_off()

        for i in self.medical_group:
            self.driver[i] = 4095

    #Turns on the Industrial LEDs
    def _industrial_mode(self):
        self._turn_all_off()

        for i in self.industry_group:
            self.driver[i] = 4095

    #Turns on the SATCOM LEDs
    def _satcom_mode(self):
        self._turn_all_off()

        for i in self.space_group:
            self.driver[i] = 4095


    def _capabilities_mode(self):
        self._turn_all_off()

        self.driver[6] = 4095

    #Turns on the default LEDs
    def _default_mode(self):
        self._turn_all_on()


    def _turn_all_on(self):
        for i in range(24):
            self.driver[i] = 4095

    #Turn all the LEDS off
    def _turn_all_off(self):
        
        for i in range(24):
            self.driver[i] = 0


    #Randomly turns LEDs on and off (different everytime)
    def _random_mode(self):

        #Generate the seed from the exact time 
        random.seed(datetime.datetime.now())

        #Determine how many to turn on 
        total_on = random.randint(1, 24)

        LEDS_selected = []

        #Determine which ones to turn on
        for i in total_on:
            generated = False

            while not generated:
                LED = random.randint(0, 23)

                if LED not in LEDS_selected:
                    LEDS_selected.append(LED)
                    generated = True

        #Turn on the randomly selected LEDS 
        for i in LEDS_selected:
            self.driver[i] = 4096


