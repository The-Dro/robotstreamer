from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import atexit
import json


turningSpeedActuallyUsed = 255
#drivingSpeedAcutallyUsed = 255
turnDelay = 0.2
drivingSpeed = 255
straightDelay = 0.5
movementSystemActive = False
pingPongNumActive = 0



def runMotor(motorIndex, direction):
    motor = mh.getMotor(motorIndex+1)
    if direction == 1:
        motor.setSpeed(drivingSpeed)
        motor.run(Adafruit_MotorHAT.FORWARD)
    if direction == -1:
        motor.setSpeed(drivingSpeed)
        motor.run(Adafruit_MotorHAT.BACKWARD)
    if direction == 0.5:
        motor.setSpeed(128)
        motor.run(Adafruit_MotorHAT.FORWARD)
    if direction == -0.5:
        motor.setSpeed(128)
        motor.run(Adafruit_MotorHAT.BACKWARD)



# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)




def times(lst, number):
                    return [x*number for x in lst]
    



def init(forwardDefinition, leftDefinition, pEnabled):

                global left
                global right
                global forward
                global backward
                global motorA
                global motorB
                global pingPongEnabled
                global mhPingPong
                pingPongEnabled = pEnabled
                forward = forwardDefinition
                backward = times(forward, -1)
                left = leftDefinition
                right = times(left, -1)
                print("directions", forward, backward, left, right)


                atexit.register(turnOffMotors)
                motorA = mh.getMotor(1)
                motorB = mh.getMotor(2)
                        
                
                atexit.register(turnOffMotors)

                if pingPongEnabled:
                    mhPingPong = Adafruit_MotorHAT(addr=0x61)
                

def turnOffMotors():

    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)    
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
                
   

def move(command):
                global movementSystemActive
                global pingPongNumActive

                d = 255
    
                motorA.setSpeed(255)
                motorB.setSpeed(255)
                if command == 'F':
                    if movementSystemActive:
                        print("skip")
                    else:
                        drivingSpeed = d
                        for motorIndex in range(4):
                            runMotor(motorIndex, forward[motorIndex])
                        movementSystemActive = True
                        time.sleep(straightDelay)
                        turnOffMotors()
                        movementSystemActive = False
                if command == 'B':
                    if movementSystemActive:
                        print("skip")
                    else:
                        drivingSpeed = d
                        for motorIndex in range(4):
                            runMotor(motorIndex, backward[motorIndex])
                        movementSystemActive = True
                        time.sleep(straightDelay)
                        turnOffMotors()
                        movementSystemActive = False
                if command == 'L':
                    if movementSystemActive:
                        print("skip")
                    else:
                        drivingSpeed = turningSpeedActuallyUsed
                        for motorIndex in range(4):
                            runMotor(motorIndex, left[motorIndex])
                        movementSystemActive = True
                        print("starting")
                        time.sleep(turnDelay)
                        print("finished")
                        turnOffMotors()
                        movementSystemActive = False
                if command == 'R':
                    if movementSystemActive:
                        print("skip")
                    else:
                        drivingSpeed = turningSpeedActuallyUsed
                        for motorIndex in range(4):
                            runMotor(motorIndex, right[motorIndex])
                        movementSystemActive = True
                        time.sleep(turnDelay)
                        turnOffMotors()
                        movementSystemActive = False
                if command == 'U':
                    #mhArm.getMotor(1).setSpeed(127)
                    #mhArm.getMotor(1).run(Adafruit_MotorHAT.BACKWARD)
                    incrementArmServo(1, 10)
                    time.sleep(0.05)
                if command == 'D':
                    #mhArm.getMotor(1).setSpeed(127)
                    #mhArm.getMotor(1).run(Adafruit_MotorHAT.FORWARD)
                    incrementArmServo(1, -10)
                    time.sleep(0.05)
                if command == 'O':
                    #mhArm.getMotor(2).setSpeed(127)
                    #mhArm.getMotor(2).run(Adafruit_MotorHAT.BACKWARD)
                    incrementArmServo(2, -10)
                    time.sleep(0.05)
                if command == 'C':
                    #mhArm.getMotor(2).setSpeed(127)
                    #mhArm.getMotor(2).run(Adafruit_MotorHAT.FORWARD)
                    incrementArmServo(2, 10)
                    time.sleep(0.05)
                if command == 'FIRE':
                    print("processing fire")
                    if pingPongEnabled:
                        print("fire was enabled")
                        pingPongNumActive += 1
                        print("ping pong number active", pingPongNumActive)
                        pingPongMotor = mhPingPong.getMotor(1)
                        pingPongMotor.setSpeed(255)
                        pingPongMotor.run(Adafruit_MotorHAT.FORWARD)
                        time.sleep(2.8)
                        pingPongNumActive -= 1
                        print("ping pong number active", pingPongNumActive)

                        # if nobody has the cannon active anymore, release
                        if pingPongNumActive == 0:
                            pingPongMotor.run(Adafruit_MotorHAT.RELEASE)


                



                

            

# routing

#{"F": forward, "B": back, "L": left, "R": right}
