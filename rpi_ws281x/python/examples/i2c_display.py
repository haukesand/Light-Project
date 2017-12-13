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

bus = smbus.SMBus(1)
bus.write_byte_data(DEVICE,IODIRA,0x00)
bus.write_byte_data(DEVICE,IODIRB,0x00)
bus.write_byte_data(DEVICE,GPIOA,0x00)
bus.write_byte_data(DEVICE,GPIOB,0x00)

LCD_INIT = [0x33, 0x32, 0x38, 0x0C, 0x06, 0x01]
for i in LCD_INIT:
  lcd_byte(i,LCD_CMD)
  time.sleep(INIT)

while True:
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string(time.asctime())
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string("IP:" + subprocess.check_output(["hostname","-I"])[:-2])
  time.sleep(pause)

