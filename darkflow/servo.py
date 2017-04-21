import serial
from time import sleep

class Servo():
    def __init__(self,port,posQ):
        self.ser = serial.Serial(port, 9600)
        self.posQ = posQ

    def move(self,deg):
        #print("deg:", deg)
        self.ser.write(deg+b'\n')
    def run(self): #while True
        print("running servo")
        mov = str(90).encode('utf8')
        while True:
            try:
                pos = self.posQ.get_nowait()
                pos = int(pos)
                print("pos get:", pos)
                mov = str(pos).encode('utf8')
            except:
                pass
            self.move(mov)
            sleep(0.5)
            #print("move:",mov)
           #      self.ser.write(deg+b'\n')
             #   except:
                    #pass
    def close(self):
        self.ser.close()

if __name__ == '__main__':
    servo = Servo('/dev/tty.wchusbserial1420', 0)
    i = 0
    while i < 180:
        servo.move(str(i).encode('utf8'))
        i += 10
        sleep(0.5)
