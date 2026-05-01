from machine import Pin
import time

# 假设GPIO 0接超声波Trig，GPIO 1接Echo
trig = Pin(0, Pin.OUT)
echo = Pin(1, Pin.IN)

def get_distance():
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()
    while echo.value() == 0:
        pulse_start = time.ticks_us()
    while echo.value() == 1:
        pulse_end = time.ticks_us()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 0.034 / 2
    return distance

while True:
    dist = get_distance()
    print("Distance:", dist)
    time.sleep(0.5)
