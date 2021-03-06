#
# motorpitx v0.1 Python module for the MotorPiTX addon board for the Raspberry Pi
# Copyright (c) 2013 Jason Barnett <jase@boeeerb.co.uk>
#
# This module will allow you to control all the interfaces of the MotorPiTX
# addon board easily. This has been tested with a Raspberry Pi Model A with
# MotorPiTX v0.2 beta board. There is no reason why it shouldn't work with 
# other configurations, if it doesn't, email me with as much information and
# let me know!
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# Servod is a ServoBlaster daemon by Richard Hirst <richardghirst@gmail.com>
# https://github.com/richardghirst/PiBits/tree/master/ServoBlaster
#
# Revisions
#
# 0.1 - Initial release (Functions are; blink, motor1, motor2, out1, out2, in1, in2, servo1, servo2, cleanup)
#
#
#


from time import sleep
import RPi.GPIO as GPIO
import os

print "Setting up pins"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

READY = 7
MOTA1 = 9
MOTA2 = 10
MOTAE = 11
MOTB1 = 24
MOTB2 = 23
MOTBE = 25
OUT1 = 22
OUT2 = 17
if GPIO.RPI_REVISION == 1:
	IN1 = 21
else:
	IN1 = 27
IN2 = 4
SERVO1 = 18
SERVO2 = 15

GPIO.setup(READY, GPIO.OUT)
GPIO.setup(MOTA1, GPIO.OUT)
GPIO.setup(MOTA2, GPIO.OUT)
GPIO.setup(MOTAE, GPIO.OUT)
GPIO.setup(MOTB1, GPIO.OUT)
GPIO.setup(MOTB2, GPIO.OUT)
GPIO.setup(MOTBE, GPIO.OUT)
GPIO.setup(OUT1, GPIO.OUT)
GPIO.setup(OUT2, GPIO.OUT)
GPIO.setup(IN1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IN2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SERVO1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(SERVO2, GPIO.OUT, initial=GPIO.LOW)

MOTAPWM = GPIO.PWM(MOTAE, 100)
MOTAPWM.start(0)
MOTBPWM = GPIO.PWM(MOTBE, 100)
MOTBPWM.start(0)

OUT1PWM = GPIO.PWM(OUT1, 100)
OUT1PWM.start(0)
OUT2PWM = GPIO.PWM(OUT2, 100)
OUT2PWM.start(0)

_MOTORS = {'1' : {
			'1' : MOTA1,
			'2' : MOTA2,
			'PWM' : MOTAPWM
			},
		'2' : {
			'1' : MOTB1,
			'2' : MOTB2,
			'PWM' : MOTBPWM
			}
		}

_OUTPUTS = {'1' : {
			'PIN' : OUT1,
			'PWM' : OUT1PWM      
			},
		'2' : {
			'PIN' : OUT2,
			'PWM' : OUT2PWM      
			}
		}

_INPUTS = {
		'1' : IN1,
		'2' : IN2
		}

# # Blink the Ready light, perfect first test
def blink():
	GPIO.output(READY, GPIO.LOW)
	sleep(1)
	GPIO.output(READY, GPIO.HIGH)
	sleep(1)

def _set_motor(index, value):
	try:
		value = int(value)
		if -100 <= value <= 100:
			if value > 0:
				GPIO.output(_MOTORS[index]['1'], GPIO.HIGH)
				GPIO.output(_MOTORS[index]['2'], GPIO.LOW)
				_MOTORS[index]['PWM'].ChangeDutyCycle(value)
			elif value < 0:
				GPIO.output(_MOTORS[index]['1'], GPIO.LOW)
				GPIO.output(_MOTORS[index]['2'], GPIO.HIGH)
				_MOTORS[index]['PWM'].ChangeDutyCycle(abs(value))
			else:
				GPIO.output(_MOTORS[index]['1'], GPIO.LOW)
				GPIO.output(_MOTORS[index]['2'], GPIO.LOW)
				_MOTORS[index]['PWM'].ChangeDutyCycle(0)
		else:
			print "Motor " + index + ": Number must be between -100 and 100 - '" + str(value) + "' isn't valid"
	except:
		print "Motor " + index + ": Please enter a number - " + value + " isn't valid"

def motor1(value):
	_set_motor('1', value);

def motor2(value):
	_set_motor('2', value);

def _set_output(index, value):
	if value == True:
		_OUTPUTS[index]['PWM'].ChangeDutyCycle(100)
	elif value == int(value):
		_OUTPUTS[index]['PWM'].ChangeDutyCycle(value)
	else:
		GPIO.output(_OUTPUTS[index]['PIN'], GPIO.LOW)

def out1(value):
	_set_output('1', value)

def out2(value):
	_set_output('2', value)

def _read_input(index):
	return GPIO.input(_INPUTS[index])

def in1():
	return _read_input('1')

def in2():
	return _read_input('2')

def _set_servo(index, value):
	try:
		value = int(value)
		servo_id = int(index) - 1
		if 0 <= value <= 180:
			servo = "echo " + str(servo_id) + "=%d > /dev/servoblaster" % value
			os.system(servo)
			sleep(0.2)
			servo = "echo " + str(servo_id) + "=0 > /dev/servoblaster"
			os.system(servo)
		else:
			print "Servo " + index + ": Number must be between 0 and 180 - '" + str(value) + "' isn't valid"
	except:
		print "Servo " + index + ": Please enter a number - " + value + " isn't valid"

def servo1(value):
	_set_servo('1', value)

def servo2(value):
	_set_servo('2', value)
		
def cleanup():
	GPIO.cleanup()
