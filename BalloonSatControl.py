import serial
import RPi.GPIO as GPIO
import time

ser=serial.Serial("/dev/ttyACM0",9600)  # change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600

# Sets up the Relay controls
in1 = 17
in2 = 27
in3 = 22
in4 = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.output(in1, GPIO.HIGH)
GPIO.output(in2, GPIO.HIGH)
GPIO.output(in3, GPIO.HIGH)
GPIO.output(in4, GPIO.HIGH)

activate = True
callsign = 'AAM2P-2' # To make sure that the destination radio is in the packet


ser.write(" ".encode())

while True: 
    print("--- Waiting for Input ---")
    read_ser=ser.readline()
    print(str(read_ser))
    
    if("burn" in str(read_ser) and activate and callsign in str(read_ser)):
        activate = False
        try:
            # Turns on two relays for 2 seconds and turns them off
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)

            time.sleep(2)
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in3, GPIO.HIGH)

            time.sleep(0.5) # Pause for voltage to settle
            
            # Turns on other two relays for 2 seconds and turns them off
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in4, GPIO.LOW)

            time.sleep(2)
            GPIO.output(in2, GPIO.HIGH)
            GPIO.output(in4, GPIO.HIGH)

            # Ack message
            ser.write("`KJ5HY-3,AAM2P-2,:ack light".encode())

        except KeyboardInterrupt:
            GPIO.output(LedPin, GPIO.HIGH)     # led off
            GPIO.cleanup()                     # Release resource
             
    elif("reset" in str(read_ser) and not activate):
        print('Laser reset')
        activate = True
        ser.write("`KJ5HY-3,AAM2P-2,:ack reset".encode())

        
        
    else:
        print("Message not recognized")   
        #ser.write("`KJ5HY-3,AAM2P-2,:rej0".encode())

