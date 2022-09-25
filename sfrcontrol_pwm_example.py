#Örnek PWM Uygulaması 

from sfrcontrol_registers328p import *
import serial 
import time
ser = serial.Serial('COM4', 115200, timeout = 0.10, parity=serial.PARITY_NONE,
stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, rtscts = 0)
time.sleep(2) # Arduino'da bootloader ve reset gecikmesi olmakta!

# seri port komutlar
bayt_oku = b'\x00'
bayt_yaz = b'\x01'


def sfr_read(sfr):
    seri_gonder = bayt_oku + sfr 
    ser.write(seri_gonder)
    return int.from_bytes(ser.read(1), "big")

def sfr_write(sfr, val):
    seri_gonder = bayt_yaz + sfr + (val.to_bytes(1, 'big'))
    ser.write(seri_gonder)

def sfr_bit_set(sfr, bit):
    sfr_deger = sfr_read(sfr)
    sfr_deger = sfr_deger | (1<<bit)
    sfr_write(sfr, sfr_deger)

def sfr_bit_reset(sfr, bit):
    sfr_deger = sfr_read(sfr)
    sfr_deger = sfr_deger & ~(1<<bit)
    sfr_write(sfr, sfr_deger)

def pwm_init():
    sfr_write(TCCR1A, 0)
    sfr_write(TCCR1B, 0)
    sfr_write(TCCR1C, 0)
    sfr_write(TCNT1L, 0)
    sfr_write(TCNT1H, 0)
    sfr_write(OCR1AL, 0)
    sfr_write(OCR1AH, 0)
    sfr_write(OCR1BL, 0)
    sfr_write(OCR1BH, 0)
    sfr_write(ICR1H, 0)
    sfr_write(ICR1L, 0)
    sfr_bit_set(DDRB, DDB1)
    sfr_bit_set(TCCR1A, COM1A1)
    sfr_bit_set(TCCR1B, WGM13)
    sfr_bit_set(TCCR1B, CS10)
    icr1_deger = 1000
    sfr_write(ICR1H, (icr1_deger & 0xFF))
    sfr_write(ICR1L, ((icr1_deger >> 8) & 0xFF))
    ocr1a_deger = 10
    sfr_write(OCR1AH, (ocr1a_deger & 0xFF))
    sfr_write(OCR1AL, ((ocr1a_deger >> 8) & 0xFF))

ocr1a_deger = 0
pwm_init()
while True:
    ocr1a_deger = ocr1a_deger + 1
    if ocr1a_deger > 500:
        ocr1a_deger = 0
    sfr_write(OCR1AH, (ocr1a_deger & 0xFF))
    sfr_write(OCR1AL, ((ocr1a_deger >> 8) & 0xFF))
    time.sleep(0.01)

