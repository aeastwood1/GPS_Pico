from machine import UART, Pin, I2C
import ssd1306
from micropyGPS import MicropyGPS



#Hardware Setup:
#Connection to GPS
uart = UART(0, baudrate = 9600, tx=Pin(16), rx=Pin(17))
#Display
i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=400000)
display = ssd1306.SSD1306_I2C(128, 32, i2c)


#Function for processing UART feed
rx_buff = []
sentences = []

def on_uart_rx():
    global rx_buff
    global sentences
    char = uart.read(1)
    rx_buff.append(char)
    if char == b'\n':
        sentences.append(b''.join(rx_buff))
        rx_buff = []


#Main loop
my_gps = MicropyGPS()

while True:
    if uart.any():
        on_uart_rx()

    if len(sentences) > 0:
        sentence = sentences.pop(0).decode().strip('\r\n')
        print(sentence)
        split_sentence = sentence.strip('$').split(',')
        if split_sentence[0] == "GPRMC":
            # print(split_sentence[3])
            for x in sentence:
                my_gps.update(x)
            lat = my_gps.latitude
            lon = my_gps.longitude
            display.init_display()
            display.text(str(lat).strip('[]'), 0,0)
            display.text(str(lon).strip('[]'), 0, 10)
            display.show()
            

        



