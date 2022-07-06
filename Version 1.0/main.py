### Copyright / Licence ###
####################################################################################
#
#MIT License
#
#Copyright (c) 2022 Morgan Winters
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
#
####################################################################################


### Set Up ###
# Import Libraries 
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Direction, Stop, Button, Color
from pybricks.hubs import TechnicHub
from pybricks.tools import wait

# Initialize the hub.
hub = TechnicHub()

# Connect to the remote.
remote = Remote()
#change the text inside the "" to set name on remote
#15 character limit 
remote.name("RemoteNameHere")

# Update Console & LED's
print("C+ Remote Speed Controller - Version 1.0")
print("\nRunning Setup...")
hub.light.on(Color.RED)
remote.light.on(Color.RED)
wait(100)
hub.light.on(Color.ORANGE)
remote.light.on(Color.ORANGE)


# System Varibles
print("declaring variables...")
# Set Startup Controller Mode
#set controller mode on startup to 2 (bang bang mode)
#set to 1 to start in precision speed control
controllerMode = 2

# Motor Varibles
#used by the code, no need to change these
drive_motor_speed = 0
steer_angle = 0
left_end = 0
right_end = 0
switch_debounce_time = 200

# User Definable Variables
drive_motor_increment = 10 #e.g. set to 20 to have 5 speed steps or 5 to have 20 speed steps | min = 1 - max = 50
steering_motor_increment = 10 #e.g. set to 5 to have 16 steer angle steps | NOTE: THIS IS MOTOR ANGLE - NOT STEER ANGLE
min_steering_angle = -80 #trial and error until you get it right, start low and increase by 10° until its right
max_steering_angle = 80 #set to the same as min_steering_angle but a positive value - min_steering_angle should be a negitive value
#the 80 value is about right for a 1x7 Technic gear rack (#87761) with a 12 tooth gear (#32270)


# Initialize The Motors
print("initializing motors...")
#set motor ports
#set direction to Direction.CLOCKWISE or Direction.COUNTERCLOCKWISE
#depending on requirement
drive1 = Motor(Port.A, Direction.CLOCKWISE)
drive2 = Motor(Port.B, Direction.CLOCKWISE)
steer = Motor(Port.C, Direction.COUNTERCLOCKWISE)
#unused = Motor(Port.D, Direction.CLOCKWISE) #un-comment this to enable port D

# Home Steering Motor
print("calibrating steering motor...")
#this finds the endstops of the steering motor
#lower duty cycle limit in increment of 5 if you have clicky gears
left_end = steer.run_until_stalled(-200, then = Stop.HOLD, duty_limit = 50)
right_end = steer.run_until_stalled(200, then = Stop.HOLD, duty_limit = 50)
# Reset steering angle
steer.reset_angle((right_end - left_end) / 2)
steer.run_target(speed = 200, target_angle = 0, wait = False)
steer_angle = 0

# Update Console & LED's
hub.light.on(Color.WHITE)
remote.light.on(Color.WHITE)
print("\nSetup Complete")
print("Battery voltage: " + str(hub.battery.voltage()) + "mV")
print("Battery current: " + str(hub.battery.current()) + "mA")
print("Hub Ready")
wait(1000)
#sets LED colour to the selected controller mode above
if controllerMode == 1:
    hub.light.on(Color.GREEN)
    remote.light.on(Color.GREEN)
elif controllerMode == 2:
    hub.light.on(Color.CYAN)
    remote.light.on(Color.CYAN)


### System Functions ###
# End Stop LED Flash
#flashes hub and remote LED red when drive motor speed is at max or steering endstop has been reached
def EndStopFlashRed():
    hub.light.on(Color.RED)
    remote.light.on(Color.RED)
    wait(250)
    #then resets back to the correct colour for the controller mode
    if controllerMode == 1:
        hub.light.on(Color.GREEN)
        remote.light.on(Color.GREEN)
    elif controllerMode == 2:
        hub.light.on(Color.CYAN)
        remote.light.on(Color.CYAN)

# Emergency Stop LED Flash
#flashes hub and remote LED red/blue alternately when the emergency stop buttons are pressed
def EmStopFlash():
    for x in range (0, 5):
        hub.light.on(Color.RED)
        remote.light.on(Color.BLUE)
        wait(150)
        hub.light.on(Color.BLUE)
        remote.light.on(Color.RED)
        wait(150)
    #then resets back to the correct colour for the controller mode    
    if controllerMode == 1:
        hub.light.on(Color.GREEN)
        remote.light.on(Color.GREEN)
    elif controllerMode == 2:
        hub.light.on(Color.CYAN)
        remote.light.on(Color.CYAN)


### Main Loop Function ###
while True:
    ### Check which buttons are pressed
    pressed = remote.buttons.pressed()
 
    ### Drive Motors
    # Precision Mode
    #get drive motor speed value from buttons
    #this section does not set the motor speed to the selected value, we'll do that after
    if controllerMode == 1:
        #increase speed value on left plus button    
        if Button.LEFT_PLUS in pressed:
            if drive_motor_speed < 100:
                drive_motor_speed = drive_motor_speed + drive_motor_increment
                print("Drive motors running at " + str(drive_motor_speed) + "%")
                wait(switch_debounce_time)
            elif drive_motor_speed == 100:
                EndStopFlashRed()
                print("Motors already running at full speed.")
            
        #decrease speed value on left minus button
        if Button.LEFT_MINUS in pressed:
            if drive_motor_speed > 0 or drive_motor_speed == 0:
                drive_motor_speed = drive_motor_speed - drive_motor_increment
                print("Drive motors running at " + str(drive_motor_speed) + "%")
                wait(switch_debounce_time)
            elif drive_motor_speed < 0 and drive_motor_speed > -100 or drive_motor_speed == 0:
                drive_motor_speed = drive_motor_speed - drive_motor_increment
                print("Drive motors running at " + str(drive_motor_speed) + "%")
                wait(switch_debounce_time)
            elif drive_motor_speed == -100:
                EndStopFlashRed()
                print("Motors already running at full speed.")
    # Bang Bang Mode
    elif controllerMode == 2:
        if Button.LEFT_PLUS in pressed:
            drive_motor_speed = 100
        elif Button.LEFT_MINUS in pressed:
            drive_motor_speed = -100            
        else:
            drive_motor_speed = 0 
    #now we apply the selected speed value to drive motors
    drive1.dc(drive_motor_speed)
    drive2.dc(drive_motor_speed)


    ### Steering
    # Precision Mode
    if controllerMode == 1:
        if Button.RIGHT_PLUS in pressed:
            if steer_angle > min_steering_angle:
                steer_angle = steer_angle - steering_motor_increment
                steer.run_target(2400, steer_angle, Stop.BRAKE, wait = False)
                print("Steering motor at " + str(steer_angle))
                wait(switch_debounce_time)
            else:
                EndStopFlashRed()
        if Button.RIGHT_MINUS in pressed:
            if steer_angle < max_steering_angle:
                steer_angle = steer_angle + steering_motor_increment
                steer.run_target(2400, steer_angle, Stop.BRAKE, wait = False)
                print("Steering motor at " + str(steer_angle))
                wait(switch_debounce_time)
            else:
                EndStopFlashRed()
    # Bang Bang Mode
    elif controllerMode == 2:
        steer_angle  = 0
        if Button.RIGHT_PLUS in pressed:
            steer_angle -= 80
        if Button.RIGHT_MINUS in pressed:
            steer_angle += 80
        steer.run_target(2400, steer_angle, Stop.BRAKE, wait = False)      


    ### Emergency Stop - Left Red Button
    if Button.LEFT in pressed or Button.RIGHT in pressed:
        if drive_motor_speed != 0 or steer_angle != 0:
            drive_motor_speed = 0
            drive1.dc(0)
            drive2.dc(0)
            steer_angle = 0
            steer.run_target(2400, 0, Stop.BRAKE, wait = False)
            print("Emergency stop button pressed, setting drive motor speed to 0 and returning steering motor to 0")
            EmStopFlash()


    # Mode Selector - Centre Green button
    if Button.CENTER in pressed:
        if controllerMode == 1:
            controllerMode = 2
            hub.light.on(Color.CYAN)
            remote.light.on(Color.CYAN)
            print("Controller mode 1")
        elif controllerMode == 2:
            controllerMode = 1
            hub.light.on(Color.GREEN)
            remote.light.on(Color.GREEN)
            print("Controller mode 2")
        wait(switch_debounce_time)

    # Wait For 10 Millisecond Before Repeating Loop
    wait(10)
