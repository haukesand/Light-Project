#!/usr/bin/python
import time, smbus, subprocess

DEVICE = 0x20
IODIRA = 0x00
IODIRB = 0x01
GPIOA  = 0x12
GPIOB  = 0x13

LCD_WIDTH = 16
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
LCD_CHR = 1
LCD_CMD = 0
LCD_RS = 0x02
LCD_E  = 0x01
E_PULSE = 0.00005
E_DELAY = 0.00005
INIT  = 0.01
pause = 2

def lcd_byte(bits, mode):
    bus.write_byte_data(DEVICE,GPIOB,LCD_RS*mode)
    bus.write_byte_data(DEVICE,GPIOA,bits)
    time.sleep(E_DELAY)
    bus.write_byte_data(DEVICE,GPIOB,LCD_E+LCD_RS*mode)
    time.sleep(E_PULSE)
    bus.write_byte_data(DEVICE,GPIOB,LCD_RS*mode)
    time.sleep(E_DELAY)

def lcd_string(message):
    message = message.ljust(LCD_WIDTH," ")
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)

def write_line(nr, message):
    if nr == 1:
        lcd_byte(LCD_LINE_1, LCD_CMD)
    elif nr == 2:
        lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string(message)

def create_message(type):
    if type == "turn_left":
        write_line(1, "About to: ")
        write_line(2, "Turn left")

    elif type == "turn_right":
        write_line(1, "About to: ")
        write_line(2, "Turn left")

    elif type == "start_moving":
        write_line(1, "")
        write_line(2, "Start moving")

    elif type == "move_backwards":
        write_line(1, "Driving")
        write_line(2, "backwards")

    elif type == "lane_left":
        write_line(1, "Into:")
        write_line(2, "left lane")

    elif type == "lane_right":
        write_line(1, "Into:")
        write_line(2, "right lane")

    elif type == "depart_todestination":
        write_line(1, "Have a ")
        write_line(2, "good ride!")

    elif type == "arrive_destination":
        write_line(1, "")
        write_line(2, "You arrived!")

    elif type == "highway_enter":
        write_line(1, "Entering:")
        write_line(2, "left")
    elif type == "highway_leave":
        write_line(1, "Exiting:")
        write_line(2, "right")

    elif type == "wait_trafficlight":
        write_line(1, "Waiting for:")
        write_line(2, "traffic lights")

    elif type == "wait_pedestrian":
        write_line(1, "Waiting for:")
        write_line(2, "pedestrian")

    elif type == "uneven_road":  # Needs a special animation type to "rattle"
        write_line(1, "")
        write_line(2, "Uneven road!")

    elif type == "swerve_left":
        write_line(1, "")
        write_line(2, "Swerve left!")


    elif type == "brake_now":
        write_line(1, "")
        write_line(2, "Braking")


    elif type == "slow_down":
        write_line(1, "")
        write_line(2, "Slowing down")


    elif type == "speed_up":  # TODO use strength for either speed of animation or visibility
        write_line(1, "")
        write_line(2, "Speeding up")

    elif type == "speed_keep":  # TODO use strength for either speed of animation or visibility
        write_line(1, "")
        write_line(2, "Driving")

bus = smbus.SMBus(1)
bus.write_byte_data(DEVICE,IODIRA,0x00)
bus.write_byte_data(DEVICE,IODIRB,0x00)
bus.write_byte_data(DEVICE,GPIOA,0x00)
bus.write_byte_data(DEVICE,GPIOB,0x00)

LCD_INIT = [0x33, 0x32, 0x38, 0x0C, 0x06, 0x01]
for i in LCD_INIT:
    lcd_byte(i,LCD_CMD)
    time.sleep(INIT)

write_line(1, time.asctime())
write_line(2, "IP:" + subprocess.check_output(["hostname","-I"])[:-2])
# time.sleep(pause)
