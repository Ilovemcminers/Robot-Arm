import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)

motor_pins = {
    "motor1": {"in1": 17, "in2": 18, "en": 22},
    "motor2": {"in1": 23, "in2": 24, "en": 25}
}

for m in motor_pins.values():
    gpio.setup(m["in1"], gpio.OUT)
    gpio.setup(m["in2"], gpio.OUT)
    gpio.setup(m["en"], gpio.OUT)

pwm = {}
for name, m in motor_pins.items():
    pwm[name] = gpio.PWM(m["en"], 100)
    pwm[name].start(0)

def move(name, speed, direction):
    m = motor_pins[name]
    if direction == "forward":
        gpio.output(m["in1"], True)
        gpio.output(m["in2"], False)
    else:
        gpio.output(m["in1"], False)
        gpio.output(m["in2"], True)
    pwm[name].ChangeDutyCycle(speed)

try:
    while True:
        move("motor1", 50, "forward")
        move("motor2", 50, "forward")
        time.sleep(2)
        move("motor1", 50, "backward")
        move("motor2", 50, "backward")
        time.sleep(2)
except KeyboardInterrupt:
    pass

for p in pwm.values():
    p.stop()
gpio.cleanup()
