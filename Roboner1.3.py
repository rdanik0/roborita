#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port, Color, Stop, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from ev3muxdevices import MuxTouchSensor, MuxColorSensor, MuxInfraredSensor, MuxGyroSensor, MuxUltrasonicSensor
#IDEA FOR COMMUNICATION ARD>LEGO BULB|LEGO>ARD EV3 SOUNDS 

ev3 = EV3Brick()
#Movement
left_motor = Motor(Port.D, positive_direction=Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
robot = DriveBase(left_motor, right_motor, wheel_diameter=32, axle_track=185)

#Sensors (port S3 available)
gyro = GyroSensor(Port.S1)
color_sensor = ColorSensor(Port.S2)
us_front = MuxUltrasonicSensor(4,1)
us_right = MuxUltrasonicSensor(4,2)
us_left = MuxUltrasonicSensor(4,3)
gyro.reset_angle(0)

#General Variables
RoomCounter = 0
WallDistance=350
CandleFound=False

def isWall(sensor):
    return sensor.distance() <=WallDistance

def LocateRoomEntrance():
    return color_sensor.color == Color.GREEN #in competition make it WHITE!

def room_encountered():
    global RoomCounter
    RoomCounter += 1
    robot.straight(250)
    #Tell the arduino in room
    wait(500)
    robot.turn(180)


def ResetFacing():
    if(us_front.distance()>us_right and us_front.distance > us_left.distance):
        pass
    elif(us_right.distance()>us_front.distance() and us_right.distance > us_left):
        robot.turn(90)
        gyro.reset_angle(0)
    elif(us_left.distance()>us_front.distance() and us_left.distance > us_right):
        robot.turn(-90)
        gyro.reset_angle(0)

    if not isWall(us_right):
        pass
        #turn to start facing th long hall

def MovementBefore():
    #Operating priority: Right > Front > Left >180 Degrees rotation
    if not(isWall(us_right)):
        while gyro.angle() <= 90:
            robot.drive(500, 45)
        robot.stop()
        robot.straight(100)
        gyro.reset_angle(0)
                
    elif not(isWall(us_front)):
        while isWall(us_right):
            if us_right.distance() <= 200:
                robot.drive(500, -5)
            elif us_left.distance() <= 200:
                robot.drive(500, 5)
            else:
                robot.straight(100)

    elif not(isWall(us_left)):
        while gyro.angle() >= -90:
            robot.drive(500, -45)
        robot.stop()
        robot.straight(100)
        gyro.reset_angle(0) 

def MovementAfter():
    #Operating priority: Left > Front >Right> 180 Degrees rotation

    if not(isWall(us_left)):
        while gyro.angle() >= -90:
            robot.drive(500, -45)
        robot.stop()
        robot.straight(100)
        gyro.reset_angle(0)
    elif not(isWall(us_front)):        
        while isWall(us_left):
            if us_right.distance() <= 200:
                robot.drive(500, -5)
            elif us_left.distance() <= 200:
                robot.drive(500, 5)
            else:
                robot.straight(100)
    elif not(isWall(us_right)):
        while gyro.angle() <= 90:
            robot.drive(500, 45)
        robot.stop()
        robot.straight(100)
        gyro.reset_angle(0)
                        
def Main():  
    ResetFacing()
    while True:
        if(CandleFound):
            MovementAfter()
            ReturnToStartingPoint()
        elif(LocateRoomEntrance()):
            room_encountered
        else:
            MovementBefore()
            
def ReturnToStartingPoint():
    pass

Main()


