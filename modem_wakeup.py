import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

ir_id = 23
blue_id = 10
uv_id = 11
motor_sleep = 8

modem_pin = 13

fan_1 = 7
fan_2 = 18

GPIO.setup(fan_1,GPIO.OUT)
GPIO.setup(fan_2,GPIO.OUT)
GPIO.setup(ir_id,GPIO.OUT)
GPIO.setup(blue_id,GPIO.OUT)
GPIO.setup(uv_id,GPIO.OUT)
GPIO.setup(motor_sleep,GPIO.OUT)
GPIO.setup(modem_pin,GPIO.OUT)

GPIO.output(fan_1, False)
GPIO.output(fan_2, False)
GPIO.output(ir_id, False)
GPIO.output(blue_id, False)
# Turn off the flight mode
GPIO.output(uv_id, False) 
GPIO.output(motor_sleep, False) 
GPIO.output(modem_pin, False) 