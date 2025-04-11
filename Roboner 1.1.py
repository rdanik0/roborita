#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.iodevices import I2CDevice
from pybricks.parameters import Port
from pybricks.tools import wait

# Подключение к SMUX, который на S2
smux = I2CDevice(Port.S2, 0x10)

# Адрес ультразвукового датчика по I2C
ULTRASONIC_ADDR = 0x02
ultra = I2CDevice(Port.S2, ULTRASONIC_ADDR)

# Битовые маски для портов A (0), B (1), C (2)
mux_ports = {
    "C1": 0x01,  # порт A (бит 0)
    "C2": 0x02,  # порт B (бит 1)
    "C3": 0x04,  # порт C (бит 2)
}

def read_ultrasonic(mux_mask):
    # Включить только один порт
    smux.write(bytes([0x70, mux_mask]))
    wait(100)  # Ждём стабилизации

    try:
        ultra.write(b'\x42')           # Регистр с расстоянием
        data = ultra.read(1)           # Чтение 1 байта
        return data[0]                 # Возвращаем расстояние
    except:
        return None  # Если что-то пошло не так

while True:
    for name, mask in mux_ports.items():
        dist = read_ultrasonic(mask)
        if dist is not None:
            ev3.screen.print(name, dist)
        else:
            ev3.screen.print(1)
    wait(1000)  