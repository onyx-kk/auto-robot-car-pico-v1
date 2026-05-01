from machine import Pin, PWM
import time

# ========== DRV8833 电机引脚设置 ==========
# 左马达 (通道A)
AIN1 = PWM(Pin(8))
AIN2 = PWM(Pin(9))
# 右马达 (通道B)
BIN1 = PWM(Pin(12))
BIN2 = PWM(Pin(13))
# 待机控制脚 (STBY)
STBY = Pin(10, Pin.OUT)

# 初始化PWM频率
for motor in [AIN1, AIN2, BIN1, BIN2]:
    motor.freq(1000)

# 使能电机驱动
STBY.value(1)

def left_motor(speed):
    """左马达控制。speed: -1.0~1.0, 正数前进, 负数后退, 0停止"""
    if speed > 0:
        AIN1.duty_u16(0)
        AIN2.duty_u16(int(speed * 65535))
    elif speed < 0:
        AIN1.duty_u16(int(-speed * 65535))
        AIN2.duty_u16(0)
    else:
        AIN1.duty_u16(0)
        AIN2.duty_u16(0)

def right_motor(speed):
    """右马达控制。speed: -1.0~1.0, 正数前进, 负数后退, 0停止"""
    if speed > 0:
        BIN1.duty_u16(0)
        BIN2.duty_u16(int(speed * 65535))
    elif speed < 0:
        BIN1.duty_u16(int(-speed * 65535))
        BIN2.duty_u16(0)
    else:
        BIN1.duty_u16(0)
        BIN2.duty_u16(0)

def forward(sp=0.6):
    left_motor(sp)
    right_motor(sp)

def backward(sp=0.6):
    left_motor(-sp)
    right_motor(-sp)

def turn_left(sp=0.6):
    left_motor(-sp)
    right_motor(sp)

def turn_right(sp=0.6):
    left_motor(sp)
    right_motor(-sp)

def stop():
    left_motor(0)
    right_motor(0)

# ========== 超声波测距 ==========
TRIG = Pin(2, Pin.OUT)
ECHO = Pin(3, Pin.IN)

def get_distance():
    """返回离障碍物的距离（cm），如果超时返回 200"""
    TRIG.low()
    time.sleep_us(2)
    TRIG.high()
    time.sleep_us(10)
    TRIG.low()

    start = time.ticks_us()
    timeout = start + 30000
    while ECHO.value() == 0:
        start = time.ticks_us()
        if start > timeout:
            return 200
    while ECHO.value() == 1:
        end = time.ticks_us()
        if end > timeout:
            return 200
    
    duration = time.ticks_diff(end, start)
    dist = (duration * 0.0343) / 2
    return dist

# ========== 避障主循环 ==========
SAFE = 25
print("避障小车启动！")

while True:
    distance = get_distance()
    print("前方距离:", distance, "cm")

    if distance < SAFE:
        stop()
        time.sleep(0.1)
        backward(0.5)
        time.sleep(0.4)
        # 随机转向
        if (time.ticks_us() % 2) == 0:
            turn_left(0.6)
        else:
            turn_right(0.6)
        time.sleep(0.5)
        stop()
        time.sleep(0.1)
    else:
        forward(0.6)
    
    time.sleep(0.1)
