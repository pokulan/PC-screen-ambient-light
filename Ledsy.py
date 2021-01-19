from infi.systray import SysTrayIcon
from win32api import GetSystemMetrics
import serial
import math
import easygui
import colorsys
from PIL import ImageGrab
import time

PORT = 'COM12'          # !ARDUINO SERIAL PORT!
running = True

leds_x = 9              # LEDS COUNT IN ROW
leds_y = 5              # LEDS COUNT IN COLULMN
block_x = int(GetSystemMetrics(0) / leds_x) - 1
block_y = int(GetSystemMetrics(1) / leds_y) - 1
blocks_active = []

hue = 0
flag = 0

# SETTINGS
power = 1
pattern = 3
speed = 50
R_PC = 0
G_PC = 0
B_PC = 255
R_AMB = 0
G_AMB = 0
B_AMB = 255

scr_point = []
last_values = {}

amb_on = 1
s = serial.Serial()

print("Width =", block_x)
print("Height =", block_y)

for j in range(leds_y):
    blocks_active.append([])
    for i in range(leds_x):
        if (j == 0 or j == leds_y - 1) or (i == 0 or i == leds_x - 1):
            blocks_active[j].append(True)
        else:
            blocks_active[j].append(False)

for i in range(leds_x - 1, -1, -1):
    scr_point.append([i * block_x, block_y * (leds_y - 1), flag])
    flag += 1
for i in range(leds_y - 1, -1, -1):
    scr_point.append([0, i * block_y, flag])
    flag += 1
for i in range(0, leds_x):
    scr_point.append([i * block_x, 0, flag])
    flag += 1
for i in range(0, leds_y):
    scr_point.append([block_x * (leds_x - 1), i * block_y, flag])
    flag += 1

for px in scr_point:
    last_values[px[2]] = [0, 0, 0]


def save_settings():
    global power
    global pattern
    global speed
    global R_PC
    global G_PC
    global B_PC
    global amb_on
    f = open("config.cfg", "w")
    f.write(str(power) + "\n" + str(pattern) + "\n" + str(speed) + "\n" + str(R_PC) + "\n" + str(G_PC) + "\n" + str(B_PC) + "\n" + str(amb_on)
            + "\n" + str(R_AMB) + "\n" + str(G_AMB) + "\n" + str(B_AMB)  + "\n" + str(PORT))
    f.close()


def load_settings():
    global power
    global pattern
    global speed
    global R_PC
    global G_PC
    global B_PC
    global R_AMB
    global G_AMB
    global B_AMB
    global amb_on
    global PORT
    try:
        f = open("config.cfg", "r")
        data = f.readlines()
        power = int(data[0])
        pattern = int(data[1])
        speed = int(data[2])
        R_PC = int(data[3])
        G_PC = int(data[4])
        B_PC = int(data[5])
        amb_on = int(data[6])
        R_AMB = int(data[7])
        G_AMB = int(data[8])
        B_AMB = int(data[9])
        PORT = data[10]
        f.close()
    except:
        pass


def on(systray):
    global power
    power = 1
    save_settings()


def off(systray):
    global power
    power = 0
    save_settings()

def color(systray):
    global R_PC
    global G_PC
    global B_PC
    R_PC = easygui.enterbox("RED 0-255")
    G_PC = easygui.enterbox("GREEN 0-255")
    B_PC = easygui.enterbox("BLUE 0-255")
    save_settings()


def amb(systray):
    global amb_on
    amb_on = 1
    save_settings()

def amb_off(systray):
    global amb_on
    amb_on = 0
    save_settings()


def amb_red(systray):
    global amb_on
    global R_AMB
    global G_AMB
    global B_AMB
    R_AMB = 255
    G_AMB = 0
    B_AMB = 0
    amb_on = 2
    save_settings()


def amb_green(systray):
    global amb_on
    global R_AMB
    global G_AMB
    global B_AMB
    R_AMB = 0
    G_AMB = 255
    B_AMB = 0
    amb_on = 2
    save_settings()


def amb_blue(systray):
    global amb_on
    global R_AMB
    global G_AMB
    global B_AMB
    R_AMB = 0
    G_AMB = 0
    B_AMB = 255
    amb_on = 2
    save_settings()


def amb_cyan(systray):
    global amb_on
    global R_AMB
    global G_AMB
    global B_AMB
    R_AMB = 0
    G_AMB = 255
    B_AMB = 255
    amb_on = 2
    save_settings()


def amb_purple(systray):
    global amb_on
    global R_AMB
    global G_AMB
    global B_AMB
    R_AMB = 140
    G_AMB = 0
    B_AMB = 255
    amb_on = 2
    save_settings()


def amb_yellow(systray):
    global amb_on
    global R_AMB
    global G_AMB
    global B_AMB
    R_AMB = 255
    G_AMB = 255
    B_AMB = 0
    amb_on = 2
    save_settings()


def amb_white(systray):
    global amb_on
    global R_AMB
    global G_AMB
    global B_AMB
    R_AMB = 255
    G_AMB = 255
    B_AMB = 255
    amb_on = 2
    save_settings()


def amb_warm(systray):
    global amb_on
    global R_AMB
    global G_AMB
    global B_AMB
    R_AMB = 255
    G_AMB = 130
    B_AMB = 130
    amb_on = 2
    save_settings()


def RED(systray):
    global R_PC
    global G_PC
    global B_PC
    R_PC = 255
    G_PC = 0
    B_PC = 0
    save_settings()


def GREEN(systray):
    global R_PC
    global G_PC
    global B_PC
    R_PC = 0
    G_PC = 255
    B_PC = 0
    save_settings()


def BLUE(systray):
    global R_PC
    global G_PC
    global B_PC
    R_PC = 0
    G_PC = 0
    B_PC = 255
    save_settings()


def CYAN(systray):
    global R_PC
    global G_PC
    global B_PC
    R_PC = 0
    G_PC = 255
    B_PC = 255
    save_settings()


def PURPLE(systray):
    global R_PC
    global G_PC
    global B_PC
    R_PC = 140
    G_PC = 0
    B_PC = 255
    save_settings()

def YELLOW(systray):
    global R_PC
    global G_PC
    global B_PC
    R_PC = 255
    G_PC = 255
    B_PC = 0
    save_settings()


def WHITE(systray):
    global R_PC
    global G_PC
    global B_PC
    R_PC = 255
    G_PC = 255
    B_PC = 255
    save_settings()


def speed25(systray):
    global speed
    speed = 25
    save_settings()


def speed40(systray):
    global speed
    speed = 50
    save_settings()


def speed70(systray):
    global speed
    speed = 100
    save_settings()


def pattern0(systray):
    global pattern
    pattern = 0
    save_settings()


def amb_rainbow(systray):
    global pattern
    global amb_on
    amb_on = 3
    pattern = 1
    save_settings()


def pattern1(systray):
    global pattern
    pattern = 1
    save_settings()


def pattern2(systray):
    global pattern
    pattern = 2
    save_settings()


def pattern3(systray):
    global pattern
    pattern = 3
    save_settings()


def on_quit_callback(systray):
    global s
    global running
    running = False
    while s.isOpen():
        pass


if __name__ == "__main__":
    load_settings()
    menu_options = (
                    ('Ambient', "amb.ico", (('OFF', None, amb_off),
                                             ('- ACTIVE -', None, amb),
                                             ('UNICORN!', None, amb_rainbow),
                                             ('WHITE COLD', None, amb_white),
                                             ('WHITE WARM', None, amb_warm),
                                             ('RED', None, amb_red),
                                             ('GREEN', None, amb_green),
                                             ('BLUE', None, amb_blue),
                                             ('CYAN', None, amb_cyan),
                                             ('YELLOW', None, amb_yellow),
                                             ('PURPLE', None, amb_purple),
                                             )),
                    ('Patterns', "led.ico", (('ON', None, on),
                                              ('OFF', None, off),
                                              ('UNICORN!', None, amb_rainbow),
                                              ('Meteor', None, pattern0),
                                              ('Solid', None, pattern1),
                                              ('Bounce', None, pattern2),
                                              ('Breath', None, pattern3),
                                              )),
                    ('Speed', "clock.ico", (('Fast', None, speed70),
                                             ('Normal', None, speed40),
                                             ('Slow', None, speed25),
                                             )),
                    ('Color', "color-circle.ico", (('RED', None, RED),
                                            ('GREEN', None, GREEN),
                                            ('BLUE', None, BLUE),
                                            ('CYAN', None, CYAN),
                                            ('YELLOW', None, YELLOW),
                                            ('PURPLE', None, PURPLE),
                                            ('WHITE', None, WHITE),
                                            ('UNICORN!', None, amb_rainbow),
                                            ('Custom...', None, color),
                                            )),
                    )
    systray = SysTrayIcon("led.ico", "PC Led driver", menu_options, default_menu_index=1, on_quit=on_quit_callback)
    systray.start()

    while running:
        try:
            data = []
            if amb_on == 1:
                px = ImageGrab.grab().load()
                for pix in scr_point:
                    R = 0
                    G = 0
                    B = 0
                    for a in range(7):
                        for b in range(7):
                            R += px[pix[0] + a * int(block_x / 6), pix[1] + b * int(block_y / 6)][0] * px[pix[0] + a * int(block_x / 6), pix[1] + b * int(block_y / 6)][0]
                            G += px[pix[0] + a * int(block_x / 6), pix[1] + b * int(block_y / 6)][2] * px[pix[0] + a * int(block_x / 6), pix[1] + b * int(block_y / 6)][2]
                            B += px[pix[0] + a * int(block_x / 6), pix[1] + b * int(block_y / 6)][1] * px[pix[0] + a * int(block_x / 6), pix[1] + b * int(block_y / 6)][1]
                    R = int(math.sqrt(R / 49))
                    G = int(math.sqrt(G / 49))
                    B = int(math.sqrt(B / 49))
                    R = int(math.sqrt((R * R + last_values[pix[2]][0] * last_values[pix[2]][0]) / 2))
                    G = int(math.sqrt((G * G + last_values[pix[2]][1] * last_values[pix[2]][1]) / 2))
                    B = int(math.sqrt((B * B + last_values[pix[2]][2] * last_values[pix[2]][2]) / 2))
                    hsv = colorsys.rgb_to_hsv(R / 255, G / 255, B / 255)
                    if hsv[2] > 0.2:
                        pass
                    else:
                        R = 0
                        G = 0
                        B = 0

                    data.append(R)
                    data.append(G)
                    data.append(B)
                    last_values[pix[2]] = [R, G, B]
            elif amb_on == 2:
                for i in range(28):
                    data.append(R_AMB)
                    data.append(B_AMB)
                    data.append(G_AMB)
            elif amb_on == 3:
                R_AMB = int(colorsys.hsv_to_rgb(hue/360.0, 1, 1)[0] * 255)
                G_AMB = int(colorsys.hsv_to_rgb(hue / 360.0, 1, 1)[1] * 255)
                B_AMB = int(colorsys.hsv_to_rgb(hue / 360.0, 1, 1)[2] * 255)
                hue += 2
                R_PC = R_AMB
                G_PC = G_AMB
                B_PC = B_AMB
                print(str(R_AMB) + " " + str(G_AMB) + " " + str(B_AMB))
                for i in range(28):
                    data.append(R_AMB)
                    data.append(B_AMB)
                    data.append(G_AMB)
            else:
                for i in range(84):
                    data.append(0)
            data.append(power)
            data.append(pattern)
            data.append(speed)
            data.append(R_PC)
            data.append(G_PC)
            data.append(B_PC)
            values = bytearray(data)
            s = serial.Serial(PORT, 115200, timeout=0)
            s.write(values)
            s.close()
        except Exception as e:
            print(e)
            data = []
            for i in range(84):
                data.append(0)
            data.append(power)
            data.append(pattern)
            data.append(speed)
            data.append(R_PC)
            data.append(G_PC)
            data.append(B_PC)
            values = bytearray(data)
            try:
                s = serial.Serial(PORT, 115200, timeout=0)
                s.write(values)
                s.close()
            except:
                pass
        time.sleep(0.02)
