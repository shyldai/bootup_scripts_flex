import time
import RPi.GPIO as GPIO
#import RPi.GPIO as GPIO
import argparse 

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.")

parser.add_argument("--LED", type=int, default=1, help="desired height of camera stream (default is 720 pixels)")
parser.add_argument("--x", type=int, default=0, help="desired height of camera stream (default is 720 pixels)")
parser.add_argument("--y", type=int, default=0, help="desired height of camera stream (default is 720 pixels)")
parser.add_argument("--light", type=int, default=0, help="desired height of camera stream (default is 720 pixels)")


try:
    opt = parser.parse_known_args()[0]
except:
    print("error parsing")
    parser.print_help()
    sys.exit(0)

# pin setup
#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup(27,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)

GPIO.setup(13,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)
GPIO.setup(9,GPIO.OUT)
GPIO.setup(8,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)

s = 11
GPIO.output(s, False)
GPIO.output(11, True)


#GPIO.output(21, False)
#GPIO.output(20, False)

# Motor and driver functions


WaitTime = .0003
print('hi')
def motor(d,p1,p2):
    n = int(abs(d)/ (2*5.625 * 1/64))
    print('motor: ', n)
    if d>0:
        A = False
    else:
        A = True


    #print(p1,A)
    GPIO.output(p1, A)

    for i in range(n):        
        GPIO.output(p2, False)
        time.sleep(WaitTime)
        GPIO.output(p2, True)
        time.sleep(WaitTime)


def UV_driver(x,y,uv,p1,p2,q1,q2,l):
    
    if uv:
        GPIO.output(l,True)
        print(l,'True')
    else:
        GPIO.output(l,False)
        print(l,'False')

    if x!=0 or y !=0:
        print('controlling motor...')
        GPIO.output(s, True)
        motor(x,p1,p2)
        motor(y,q1,q2)
        GPIO.output(s, False)



### main code
if opt.LED==1:
    p1,p2 = 25,24 # direction, pulse 
    q1,q2 = 16,12 # direction, pulse 
    l = 23
elif opt.LED==2:
    p1,p2 = 26,19
    q1,q2 = 21, 20
    l = 9
elif opt.LED==3:
    p1,p2 = 6,13
    q1,q2 = 5, 22
    l = 10   
elif opt.LED==4:
    p1,p2 = 17,27
    q1,q2 = 18, 9
    l = 23 #### to be modifed  

if opt.light:
    uv=True
else:
    uv=False

UV_driver(x= opt.x, y=opt.y, uv=uv,p1=p1,p2=p2,q1=q1,q2=q2,l=l)

GPIO.output(8, False)
GPIO.output(11, False)
