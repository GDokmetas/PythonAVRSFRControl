import serial 
import time
ser = serial.Serial('COM4', 115200, timeout = 0.10, parity=serial.PARITY_NONE,
stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, rtscts = 0)
time.sleep(2) # Arduino'da bootloader ve reset gecikmesi olmakta!
# seri port komutlar
bayt_oku = b'\x00'
bayt_yaz = b'\x01'

#*GPIO Yazmaçları
#* Bu adresleri datasheetten öğreniyoruz
DDRD = b'\x2A'
PORTD = b'\x2B'
# LED yakma 
kirmizi_led = 3
sari_led = 4 
#GPIO giriş çıkış ayarları

def sfr_read(sfr):
    seri_gonder = bayt_oku + sfr 
    ser.write(seri_gonder)
    return ser.read(1)

def sfr_write(sfr, val):
    seri_gonder = bayt_yaz + sfr + (val.to_bytes(1, 'big'))
    print(seri_gonder)
    ser.write(seri_gonder)

def sfr_bit_set(sfr, bit):
    sfr_deger = int.from_bytes(sfr_read(sfr), "big")
    sfr_deger = sfr_deger | (1<<bit)
    sfr_write(sfr, sfr_deger)

def sfr_bit_reset(sfr, bit):
    sfr_deger = int.from_bytes(sfr_read(sfr), "big")
    sfr_deger = sfr_deger & ~(1<<bit)
    sfr_write(sfr, sfr_deger)

#GPIO Doğrudan değer atama
sfr_write(DDRD, 255)
sfr_write(PORTD, 255)


#GPIO Bit Manüpülasyonu
sfr_write(PORTD, 0)

while True:
    # kirmizi led yakma
    sfr_bit_set(PORTD, kirmizi_led)
    time.sleep(0.2)
    #kirmizi led söndürme
    sfr_bit_reset(PORTD, kirmizi_led)
    time.sleep(0.2)