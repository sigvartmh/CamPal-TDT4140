import serial
from time import sleep

class Servo():
	def __init__(self,port): 
		self.ser = serial.Serial(port, 9600, timeout=1)

	def move(self,deg):
		self.ser.write(str(deg))
	def pos(self):
		return self.ser.readline();
	
	def close(self):
		self.ser.close()

if __name__ == '__main__':
	servo = Servo('/dev/ttyUSB0')
	i=0
	while i < 180:
		print(i)	 
		servo.move(i)
		i +=10
	
		sleep(1)
		try:
			print(servo.pos())
		except:
			pass
	servo.close()
