#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port, Color, Stop, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from ev3muxdevices import MuxTouchSensor, MuxColorSensor, MuxInfraredSensor, MuxGyroSensor, MuxUltrasonicSensor


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
StartingPoint=None
DogFound = False
DogPos = 0
RoomCounter = 0
WallDistance=250

def isWall(sensor):
    return sensor.distance() <=WallDistance

def LocateRoomEntrance():
    return color_sensor.color == Color.GREEN

def room_counter():
    global RoomCounter
    RoomCounter += 1
    robot.turn(180)
    wait(500)
    robot.straight(100)


def get_start_pos():
    global StartingPoint,DogFound,DogPos
    
    # Если стена справа значит находимся на А
    if isWall(us_right):
       StartingPoint=1
        # Если к тому же слева препятствие то нашли собаку 
        if isWall(us_left):
            DogFound = True
            DogPos = 1
    
    # Если стены справа нет значит развернемся
    elif not isWall(us_right):
        StartingPoint=2
        # Если к тому же перед роботом препятствие то смотрим на собаку
        if isWall(us_front):
            DogFound = True
            DogPos = 1
        robot.turn(90)
        gyro.reset_angle(0)

    Main()


def Main():
    TURN_ANGLE = 45
    # Главный алгоритм 
    #Operating priority: Right > Left > Front > 180Degrees rotation
    while True:
        if not(isWall(us_right)):
            while gyro.angle() <= 90:
                robot.drive(500, TURN_ANGLE)
            robot.stop()
            robot.straight(100)
            gyro.reset_angle(0)
            
        elif not(isWall(us_left)):
            while gyro.angle() >= -90:
                robot.drive(500, -TURN_ANGLE)
            robot.stop()
            robot.straight(100)
            gyro.reset_angle(0)
        
        elif not(isWall(us_front)):
            robot.straight(100)
        
        else:
            stabilization()


def stabilization():
    ANGLE = 5

    while isWall(us_right):

        if us_right.distance() <= 200:
            robot.drive(500, -ANGLE)
        elif us_left.distance() <= 200:
            robot.drive(500, ANGLE)
        else:
           robot.drive(500, 0)

def ReturnToStartingPoint():
    # Возвращение на стартовую точку
    pass

get_start_pos()



