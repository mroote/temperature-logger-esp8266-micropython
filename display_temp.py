import dht
import ssd1306
import time
import urequests
import webrepl
from machine import I2C, Pin

webrepl.start(password='micro')

# Wait for network to start up
time.sleep(2)

i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(64, 48, i2c)

d = dht.DHT22(Pin(2))

display.fill(0)
display.show()

db = 'http://10.42.100.1:8086/write?db=temperature'
location = 'apartment'

while True:
    # Measure current temperature
    d.measure()
    temp, humi = d.temperature(), d.humidity()

    # Display temperature on OLED screen
    display.fill(0)
    display.text('T: {}'.format(temp), 0, 0)
    display.text('H: {}'.format(humi), 0, 15)
    display.show()

    # POST data to influxdb
    try:
        resp_data = 'temperature,location={0} value={1} \n humidity,location={0} value={2}'.format(location,temp,humi)
        resp = urequests.post(db, data=resp_data)
        print('response: {}'.format(resp.status_code))
        if resp.status_code == 204:
            display.text('TX: {}'.format('OK'), 0, 30)
            display.show()
        else:
            display.text('TX: {}'.format('ERR'), 0, 30)
            display.show()
    except Exception as e:
        print('Error: {}'.format(e))
    time.sleep(10)

