#!/usr/bin/env pybricks-micropython

# Библиотеки
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port, Color, Stop, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from ev3muxdevices import MuxTouchSensor, MuxColorSensor, MuxInfraredSensor, MuxGyroSensor, MuxUltrasonicSensor

# S-порт MUX
MUX_PORT = 4

# Инициализация устройств
ev3 = EV3Brick()
left_motor = Motor(Port.D, positive_direction=Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)

gyro = GyroSensor(Port.S1)
color_sensor = ColorSensor(Port.S2)
us_right = MuxUltrasonicSensor(MUX_PORT, 2)
us_front = MuxUltrasonicSensor(MUX_PORT, 1)
us_left = MuxUltrasonicSensor(MUX_PORT, 3)

robot = DriveBase(left_motor, right_motor, wheel_diameter=32, axle_track=185)
gyro.reset_angle(0)

# Переменные
CurrentRoom = 0
DogFound = False
DogPos = 0
SpawnPos = None

WALL_DIST = 250
def isWall(sensor):
    return sensor.distance() <= WALL_DIST


def find_room():
    # Проверка комнаты
    return color_sensor.color == Color.GREEN

def room_check():
    global CurrentRoom
    CurrentRoom += 1
    # Проверка комнаты
    robot.turn(180)
    wait(500)
    robot.straight(100)


def get_start_pos():
    # Если стена справа значит находимся на А
    if isWall(us_right):
        # Если к тому же слева препятствие то нашли собаку
        if isWall(us_left):
            DogFound = True
            DogPos = 1
    
    # Если стены справа нет значит развернемся
    elif not isWall(us_right):
        # Если к тому же перед роботом препятствие то смотрим на собаку
        if isWall(us_front):
            DogFound = True
            DogPos = 1
        robot.turn(90)
        gyro.reset_angle(0)

        algorythm()

def algorythm():
    TURN_ANGLE = 45
    # Главный алгоритм
    while True:
        if isWall(us_front) and not isWall(us_right):
            robot.drive(500, TURN_ANGLE)
        elif isWall(us_front) and not isWall(us_left):
            robot.drive(500, -TURN_ANGLE)

        if not isWall(us_right):
            while gyro.angle() <= 90:
                robot.drive(500, TURN_ANGLE)
            robot.stop()
            robot.straight(100)
            gyro.reset_angle(0)

        else:
            stabilization()


def stabilization():
    ANGLE = 5

    while isWall(us_right):
        right_dist = us_right.distance()
        left_dist = us_left.distance()
        if right_dist <= 200:
            robot.drive(500, -ANGLE)
        elif left_dist <= 200:
            robot.drive(500, ANGLE)
        else:
           robot.drive(500, 0)



def rth():
    # Возвращение на стартовую точку
    pass


get_start_pos()