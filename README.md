# micropython-leds

This project demonstrates basic LED concepts.  it's meant as a next step after the traditional "blink" sketches.

Basic steps:

1. Copy boot.py.sample to boot.py and update with WiFi, MQTT, and NTP settings.
2. [Set WebREPL password](#webrepl).
3. Push all Python files using [ampy](#ampy) (assumes MicroPython already [flashed](#flash-micropython)).

For simple testing, just run the following once the board is flashed to avoid having to reboot and work with the console on every update.  Another file could be used instead of main.py.

```bash
ampy --port /dev/ttyUSB0 --baud 115200 run main.py
```

## Diagram

![wiring diagram](/img/esp32_motion_sensor_oled.png)

As detailed below, I experienced continuous false positive events without the resistor.

## Flash MicroPython

https://micropython.org/download/esp32/

Use firmware built with ESP-IDF v4.x

```bash
$ esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py v3.1
Serial port /dev/ttyUSB0
Connecting........_____....._____.....__
Detecting chip type... ESP32
Chip is ESP32-D0WDQ6 (revision 1)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
Crystal is 40MHz
MAC: 4c:11:ae:73:de:54
Uploading stub...
Running stub...
Stub running...
Erasing flash (this may take a while)...
Chip erase completed successfully in 9.6s
Hard resetting via RTS pin...
```

```bash
$ esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 ~/Downloads/esp32-20210902-v1.17.bin
0800 write_flash -z 0x1000 ~/Downloads/esp32-20210902-v1.17.bin
esptool.py v3.1
Serial port /dev/ttyUSB0
Connecting........___
Chip is ESP32-D0WDQ6 (revision 1)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
Crystal is 40MHz
MAC: 4c:11:ae:73:de:54
Uploading stub...
Running stub...
Stub running...
Changing baud rate to 460800
Changed.
Configuring flash size...
Flash will be erased from 0x00001000 to 0x00175fff...
Compressed 1527504 bytes to 987584...
Wrote 1527504 bytes (987584 compressed) at 0x00001000 in 22.8 seconds (effective 536.1 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
```

## ampy

Make sure user is in the dialout group to have write permissions to the /dev/ttyUSB0 device.


Install Python modules for ampy (can use Python virtualenv or install globally since it shouldn't conflict with anything else)

```bash
pip3 install adafruit-ampy
pip3 install rshell
```

```bash
ampy --port /dev/ttyUSB0 --baud 115200 put boot.py
ampy --port /dev/ttyUSB0 --baud 115200 put main.py
```

## screen

The screen command is used to connect to the serial port.  It's important to know that you cannot upload with ampy while attached to the serial port with screen so this process gets pretty repetitive.  WebREPL might work around some of this, but it seems a little more clunky than mastering these steps.

```bash
sudo apt-get install -y screen
```

### Attach to USB port

```bash
screen /dev/ttyUSB0 115200
```

After attaching to USB port, press "Enter" to get Python shell (see [Python shell help](#python-shell-help) below).

Once in the screen session and in the python shell (not screen command), press Ctrl-D to soft-reboot after uploading a file.  You cannot upload a file with ampy if screen is also attached via the serial port.

### Exit screen (kill screen).

This command kills the screen session to free up the serial port.

The Ctrl-a is the default escape key to send the command to screen (not for Python shell).
```
Ctrl-a, k
```

## Python shell help

```
>>> help()
Welcome to MicroPython on the ESP32!

For generic online docs please visit http://docs.micropython.org/

For access to the hardware use the 'machine' module:

import machine
pin12 = machine.Pin(12, machine.Pin.OUT)
pin12.value(1)
pin13 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
print(pin13.value())
i2c = machine.I2C(scl=machine.Pin(21), sda=machine.Pin(22))
i2c.scan()
i2c.writeto(addr, b'1234')
i2c.readfrom(addr, 4)

Basic WiFi configuration:

import network
sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
sta_if.scan()                             # Scan for available access points
sta_if.connect("<AP_name>", "<password>") # Connect to an AP
sta_if.isconnected()                      # Check for successful connection

Control commands:
  CTRL-A        -- on a blank line, enter raw REPL mode
  CTRL-B        -- on a blank line, enter normal REPL mode
  CTRL-C        -- interrupt a running program
  CTRL-D        -- on a blank line, do a soft reset of the board
  CTRL-E        -- on a blank line, enter paste mode

For further help on a specific object, type help(obj)
For a list of available modules, type help('modules')
>>> 
```

## WebREPL

webrepl is not enabled by default.  Most online documentation says to run import webrepl from a REPL shell and follow the prompts.  It seems to work better this way.  WebREPL is great for remotely managing a MicroPython controller connected to the network without the need for a serial port connection.

```
echo "PASS = 'password'" > webrepl_cfg.py
ampy --port /dev/ttyUSB0 --baud 115200 put webrepl_cfg.py
```

At the top of main.py with other import statements:

```
import webrepl
```

Add the following to main.py after a place where `print(station.ifconfig())` runs successfully:

```
webrepl.start()
```

The client tool is hosted at http://micropython.org/webrepl/.  It runs locally from the browser.

It's recommended to make a DHCP reservation for the MAC/IP so the IP address can be consistently used for remote connections.

## References

- https://randomnerdtutorials.com/getting-started-micropython-esp32-esp8266/
- https://randomnerdtutorials.com/esp32-esp8266-pwm-micropython/
- https://makeabilitylab.github.io/physcomp/arduino/led-blink2.html
