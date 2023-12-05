import hid

SERIAL_NUMBER = '30-31-7d-32-c9-9d'
gamepad = hid.device()
#gamepad.open(serial_number=SERIAL_NUMBER)
gamepad.open(0x057e, 0x2009)
gamepad.set_nonblocking(True)

try:
    while True:
        input = gamepad.read(14)
        if input:
            print(input[3:10])
finally:
    gamepad.close()

