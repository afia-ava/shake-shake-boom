from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from random import randint
from utime import sleep_ms
import framebuf, sys
import utime

# pins
GATE_PIN = 1
PEDOMETER_PIN = 6
OLED_SDA_PIN = 26
OLED_SCL_PIN = 27
BTN_PIN = 5 

# constants
EXPLODE_TIME = 2000 # ms
SHAKES_MIN = 20
SHAKES_MAX = 40

BUBBLE_X_MIN = 1
BUBBLE_X_MAX = 121
BUBBLE_Y_MIN = 1
BUBBLE_Y_MAX = 57

STARTING_BUBBLES = 3
BUBBLES_PER_SHAKE = 1

RESET_HOLD_TIME = 3000 # ms

def reset_shakes_needed():
    new_shakes_needed = randint(SHAKES_MIN, SHAKES_MAX)
    print(new_shakes_needed)
    return new_shakes_needed

def clamp(val, minval, maxval):
    if val < minval: return minval
    if val > maxval: return maxval
    return val

def draw_bubble_at(display, x, y):
    display.hline(x+2, y, 4, 1)
    display.hline(x+2, y+7, 4, 1)
    display.vline(x, y+2, 4, 1)
    display.vline(x+7, y+2, 4, 1)
    display.pixel(x+1, y+1, 1)
    display.pixel(x+1, y+6, 1)
    display.pixel(x+6, y+1, 1)
    display.pixel(x+6, y+6, 1)
    display.pixel(x+3, y+2, 1)
    display.pixel(x+2, y+3, 1)
    
def draw_bubbles(display, bubbles):
    display.fill(0)
    for b in bubbles:
        draw_bubble_at(display, b[0], b[1])
    display.show()
    
def add_bubbles(bubbles, n=1):
    new_bubbles = bubbles
    for i in range(n):
        new_bubbles.append((randint(BUBBLE_X_MIN, BUBBLE_X_MAX), randint(BUBBLE_Y_MIN, BUBBLE_Y_MAX)))
    return new_bubbles
    
def animate_bubbles(bubbles):
    new_bubbles = [(clamp(b[0]+randint(-1,1), BUBBLE_X_MIN, BUBBLE_X_MAX), 
                    clamp(b[1]+randint(-1,1), BUBBLE_Y_MIN, BUBBLE_Y_MAX)) for b in bubbles]
    return new_bubbles

def main():
    # pin setup
    gate = Pin(GATE_PIN, Pin.OUT)
    pdmet = Pin(PEDOMETER_PIN, Pin.IN, Pin.PULL_UP)
    btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)
    i2c_dev = I2C(1, scl=Pin(OLED_SCL_PIN), sda=Pin(OLED_SDA_PIN), freq=200000)
    oled = SSD1306_I2C(128, 64, i2c_dev)

    # states
    pdmet_state = pdmet.value()
    last_pdmet_state = pdmet_state
    paused = False
    is_started = False

    # setup
    bubbles = []
    gate.value(0)
    btn_last = btn.value()
    shakes_needed = reset_shakes_needed()
    num_shakes = 0
    start_time = utime.ticks_ms()

    bubbles = add_bubbles(bubbles, n=STARTING_BUBBLES)

    while True:
        if not is_started:
            btn_val = btn.value()
            if btn_val != btn_last:
                if btn_val == 0:
                    is_started = True
                btn_last = btn_val
            oled.fill(0)
            oled.text("STARTING SCREEN", 0, 0)
            oled.show()
        else:
            btn_val = btn.value()
            if btn_val != btn_last:
                if btn_val == 0:
                    paused = not paused
                    start_time = utime.ticks_ms()
                btn_last = btn_val
            if paused:
                oled.fill(0)
                oled.text("GAME PAUSED", 0, 0)
                if btn_val == 0:
                    elapsed_time_ms = utime.ticks_diff(utime.ticks_ms(), start_time)
                    if elapsed_time_ms > 1000:
                        oled.text("RESET GAME IN", 0, 20)
                        oled.text(str(((RESET_HOLD_TIME - elapsed_time_ms) // 1000) + 1), 0, 40)
                    if elapsed_time_ms > RESET_HOLD_TIME:
                        oled.fill(0)
                        num_shakes = 0
                        bubbles = add_bubbles([], n=STARTING_BUBBLES)
                        shakes_needed = reset_shakes_needed()
                        oled.text("RESETTING GAME!", 0, 0)
                        paused = False
                        is_started = False
                oled.show()
            else:
                bubbles = animate_bubbles(bubbles)
                draw_bubbles(oled, bubbles)
                pdmet_state = pdmet.value()
                if pdmet_state != last_pdmet_state:
                    if pdmet_state == 0:
                        num_shakes += 1
                        add_bubbles(bubbles, n=BUBBLES_PER_SHAKE)
                    last_pdmet_state = pdmet_state
                if num_shakes >= shakes_needed:
                    gate.value(1)
                    sleep_ms(EXPLODE_TIME)
                    gate.value(0)
                    num_shakes = 0
                    bubbles = add_bubbles([], n=STARTING_BUBBLES)
                    shakes_needed = reset_shakes_needed()


if __name__ == '__main__':
    main()

