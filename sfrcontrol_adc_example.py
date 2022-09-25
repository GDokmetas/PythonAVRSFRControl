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
    return ser.read(1)

def sfr_write(sfr, val):
    seri_gonder = bayt_yaz + sfr + (val.to_bytes(1, 'big'))
    ser.write(seri_gonder)

def sfr_bit_set(sfr, bit):
    sfr_deger = int.from_bytes(sfr_read(sfr), "big")
    sfr_deger = sfr_deger | (1<<bit)
    sfr_write(sfr, sfr_deger)

def sfr_bit_reset(sfr, bit):
    sfr_deger = int.from_bytes(sfr_read(sfr), "big")
    sfr_deger = sfr_deger & ~(1<<bit)
    sfr_write(sfr, sfr_deger)

def adc_init():
    sfr_write(ADCSRA, ((1<<ADPS2) | (1<<ADPS1) | (1<<ADPS0))) # ADC prescaler 128
    sfr_write(ADMUX, (1<<REFS0)) # ADC referans voltaji AVCC
    sfr_bit_set(ADCSRA, ADEN) # ADC enable
    sfr_bit_set(ADCSRA, ADSC) # ADC start conversion

def read_adc(channel):
    admux_okuma = int.from_bytes(sfr_read(ADMUX), "big")
    admux_okuma = admux_okuma & 0xF0
    admux_okuma = admux_okuma | channel
    sfr_write(ADMUX, admux_okuma)
    sfr_bit_set(ADCSRA, ADSC) # okumayi baslat
    while (int.from_bytes(sfr_read(ADCSRA), "big") & (1<<ADSC)): # okuma bitene kadar bekle
        continue
    return int.from_bytes(sfr_read(ADCL), "big") | (int.from_bytes(sfr_read(ADCH), "big") << 8)

adc_init()
while True:
    print("Okunan Deger:", read_adc(0))
    time.sleep(0.5)




