#!/usr/bin/python
import time, smbus, subprocess, threading

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
E_PULSE = 0.00005 # 0.00005
E_DELAY = 0.00005
INIT  = 0.01
pause = 2

class Display(object):
    def __init__(self):
        thread = threading.Thread(name='display', target=self.start, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
        print "Start display thread"
        
    def start(self):
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(DEVICE,IODIRA,0x00)
        self.bus.write_byte_data(DEVICE,IODIRB,0x00)
        self.bus.write_byte_data(DEVICE,GPIOA,0x00)
        self.bus.write_byte_data(DEVICE,GPIOB,0x00)

        LCD_INIT = [0x33, 0x32, 0x38, 0x0C, 0x06, 0x01]
        for i in LCD_INIT:
            self.lcd_byte(i,LCD_CMD)
            time.sleep(INIT)
        self.write_line(1, "Autopilot")
        self.write_line(2, "is active")
        # self.write_line(1, time.asctime())
        # self.write_line(2, "IP:" + subprocess.check_output(["hostname","-I"])[:-2])

        # time.sleep(pause)
    
    def restart(self):
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(DEVICE,IODIRA,0x00)
        self.bus.write_byte_data(DEVICE,IODIRB,0x00)
        self.bus.write_byte_data(DEVICE,GPIOA,0x00)
        self.bus.write_byte_data(DEVICE,GPIOB,0x00)

        LCD_INIT = [0x33, 0x32, 0x38, 0x0C, 0x06, 0x01]
        for i in LCD_INIT:
            self.lcd_byte(i,LCD_CMD)
            time.sleep(INIT)

        self.display.write_line(1, "Autopilot")
        self.display.write_line(2, "is active")


    def lcd_byte(self, bits, mode):
        self.bus.write_byte_data(DEVICE,GPIOB,LCD_RS*mode)
        self.bus.write_byte_data(DEVICE,GPIOA,bits)
        time.sleep(E_DELAY)
        self.bus.write_byte_data(DEVICE,GPIOB,LCD_E+LCD_RS*mode)
        time.sleep(E_PULSE)
        self.bus.write_byte_data(DEVICE,GPIOB,LCD_RS*mode)
        time.sleep(E_DELAY)

    def lcd_string(self, message):
        message = message.ljust(LCD_WIDTH," ")
        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[i]),LCD_CHR)

    def write_line(self, nr, message):
        if nr == 1:
            self.lcd_byte(LCD_LINE_1, LCD_CMD)
        elif nr == 2:
            self.lcd_byte(LCD_LINE_2, LCD_CMD)
        self.lcd_string(message)
        time.sleep(E_DELAY)

    def create_message(self, type):
        if type == "turn_left":
            self.write_line(1, "About to: ")
            self.write_line(2, "Turn left")

        elif type == "turn_right":
            self.write_line(1, "About to: ")
            self.write_line(2, "Turn right")

        elif type == "start_moving":
            self.write_line(1, "")
            self.write_line(2, "Start moving")

        elif type == "move_backwards":
            self.write_line(1, "Driving")
            self.write_line(2, "backwards")

        elif type == "lane_left":
            self.write_line(1, "Into:")
            self.write_line(2, "left lane")

        elif type == "lane_right":
            self.write_line(1, "Into:")
            self.write_line(2, "right lane")

        elif type == "depart_todestination":
            self.write_line(1, "Have a ")
            self.write_line(2, "good ride!")

        elif type == "arrive_destination":
            self.write_line(1, "")
            self.write_line(2, "You arrived!")

        elif type == "highway_enter":
            self.write_line(1, "Entering:")
            self.write_line(2, "left")

        elif type == "highway_leave":
            self.write_line(1, "Exiting:")
            self.write_line(2, "right")

        elif type == "wait_trafficlight":
            self.write_line(1, "Waiting for:")
            self.write_line(2, "traffic lights")

        elif type == "wait_pedestrian":
            self.write_line(1, "Waiting for:")
            self.write_line(2, "pedestrian")

        elif type == "uneven_road":  # Needs a special animation type to "rattle"
            self.write_line(1, "")
            self.write_line(2, "Uneven road!")

        elif type == "swerve_left":
            self.write_line(1, "Obstacle ahead:")
            self.write_line(2, "Swerve left!")


        elif type == "brake_now":
            self.write_line(1, "")
            self.write_line(2, "Braking")


        elif type == "slow_down":
            self.write_line(1, "")
            self.write_line(2, "Slowing down")


        elif type == "speed_up":  # TODO use strength for either speed of animation or visibility
            self.write_line(1, "")
            self.write_line(2, "Speeding up")

        elif type == "speed_keep":  # TODO use strength for either speed of animation or visibility
            self.write_line(1, "")
            self.write_line(2, "Driving")

    