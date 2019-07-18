########################################################################
# Filename   		: ButtonLightWater.py
# Description		: Button To Control Display Of A 10 LED Bar Graph 
# Author     		: Neil Smith
# First Created		: 14/07/2019
# Last Modification : 18/07/2019
########################################################################

import RPi.GPIO as GPIO
import time

class ButtonMultiLED:
	#buttonPin = 7 # The pin of the button
	#LEDPins = [0,1,2,3,4,5,6,8,9,10] # The pins of the LEDs
	#multiLEDPin = 21 # The pin of the multiLED
	#multiLEDState = 'off' # The state of the multiLED
	#currentLEDPin = 0 # The pin of the LED currently on
	#currentLEDNumber = 0 # The LED number that is currently on
	#lastLEDChangeTime = datetime.datetime.now() # The time at which the LEDs last changed
	#LEDDelayTime = 300 # The time to wait before turning on the next LED
	#LEDDirection = 1 # Direction of LEDs. 1 for right, 0 for left.
	
	def __init__(self, LEDDelayTime = 300, LEDDirection = 1):
		print('Initialising...')
		GPIO.cleanup()
		GPIO.setmode(GPIO.BCM)
		self.LEDDelayTime = LEDDelayTime
		self.LEDDirection = LEDDirection
		
		self.buttonPin = 4
		self.LEDPins = [21,20,16,12,25,24,23,18,26,19]
		self.multiLEDPin = 5
		self.multiLEDState = 'off'
		self.currentLEDNumber = 0
		self.currentLEDPin = 21
		 
		for pin in self.LEDPins:
			print(pin)
			GPIO.setup(pin, GPIO.OUT)   # Set the mode of all the LED pins to be outputs
			GPIO.output(pin, GPIO.HIGH) # Turn all the LEDs off
		GPIO.setup(self.buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set the mode of the button pin to be an input, and set it to be initially released
		GPIO.setup(self.multiLEDPin, GPIO.OUT) # Set the mode of the multiLED pin to be an output
		GPIO.output(self.multiLEDPin, GPIO.HIGH) # Turn off the multiLED
		GPIO.add_event_detect(self.buttonPin,GPIO.BOTH,callback = self.buttonChanged,bouncetime=50) # Call the buttonChanged method on change of button state
		
	def run(self):
		self.lastLEDChangeTime = time.time()*1000
		print('Starting the program...')
		while(1):
			#time.sleep(1)
			rising = GPIO.input(self.buttonPin)
			#print(rising)
			if (self.multiLEDState == 'on'): # If the multiLED is on
				if (self.timeToChangeLEDs() == True): # If its time to change the LEDs
					self.changeLEDs() # Turn on the next LED
		
	# Check whether its time to change the LEDs
	def timeToChangeLEDs(self):
		change = False
		currentTime = time.time()*1000
		if (currentTime > self.lastLEDChangeTime + self.LEDDelayTime):
			change = True
		return change
		
	# Turn on the next LED
	def changeLEDs(self):
		self.lastLEDChangeTime = time.time()*1000
		# Turn off the current LED
		GPIO.output(self.currentLEDPin, GPIO.HIGH)
		if (self.LEDDirection == 1): # If LEDs going right
			# If another LED to the right
			if (self.currentLEDNumber < len(self.LEDPins) - 1):
				self.currentLEDNumber = self.currentLEDNumber + 1
				self.currentLEDPin = self.LEDPins[self.currentLEDNumber]
				GPIO.output(self.currentLEDPin, GPIO.LOW)
			# No more LEDs to the right, set the leftmost to on
			else:
				self.currentLEDNumber = 0;
				self.currentLEDPin = self.LEDPins[self.currentLEDNumber]
				GPIO.output(self.currentLEDPin, GPIO.LOW)
		
		
	# Turn the nth LED on
	def ledOn(self,n):
		GPIO.output(n, GPIO.LOW)
		
	# Turn the nth LED off
	def ledOff(self,n):
		GPIO.output(n, GPIO.HIGH)
		
	# Turn on/off the multiLED based on button state
	def buttonChanged(self,_):
		print('Button has changed!')
		rising = GPIO.input(self.buttonPin)
		if rising:
			self.buttonPressed()
		else:
			self.buttonReleased()
		
	# When the button is released, turn off the multiLED
	def buttonReleased(self):
		self.multiLEDState = 'off'
		GPIO.output(self.multiLEDPin, GPIO.LOW)
		print('MultiLED turned off!')
		
	# When the button is pressed, turn on the multiLED
	def buttonPressed(self):
		self.multiLEDState = 'on'
		GPIO.output(self.multiLEDPin, GPIO.HIGH)
		print('MultiLED turned on!')
		
		
	# Turn off all the LEDs and release resources
	def destroy(self):
		for pin in ledPins:
			GPIO.output(pin, GPIO.HIGH)
		GPIO.cleanup()


if __name__ == "__main__":
	myClass = ButtonMultiLED(300, 1)
	try:
		myClass.run()
	except KeyboardInterrupt:
		myClass.destroy()
