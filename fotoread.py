import usb.core
import usb.util
import time

from gpiozero import LED
from time import sleep

# ****************************************************************************************
# Registro de cambios
# nhtello 25/6/2020: initial
#****************************************************************************************

led = LED(17)
def hid2ascii(lst):
    
    assert len(lst) == 8, 'Invalid data length (needs 8 bytes)'
    conv_table = {
        0:['', ''],
        4:['a', 'A'],
        5:['b', 'B'],
        6:['c', 'C'],
        7:['d', 'D'],
        8:['e', 'E'],
        9:['f', 'F'],
        10:['g', 'G'],
        11:['h', 'H'],
        12:['i', 'I'],
        13:['j', 'J'],
        14:['k', 'K'],
        15:['l', 'L'],
        16:['m', 'M'],
        17:['n', 'N'],
        18:['o', 'O'],
        19:['p', 'P'],
        20:['q', 'Q'],
        21:['r', 'R'],
        22:['s', 'S'],
        23:['t', 'T'],
        24:['u', 'U'],
        25:['v', 'V'],
        26:['w', 'W'],
        27:['x', 'X'],
        28:['y', 'Y'],
        29:['z', 'Z'],
        30:['1', '!'],
        31:['2', '@'],
        32:['3', '#'],
        33:['4', '$'],
        34:['5', '%'],
        35:['6', '^'],
        36:['7' ,'&'],
        37:['8', '*'],
        38:['9', '('],
        39:['0', ')'],
        40:['\n', '\n'],
        41:['\x1b', '\x1b'],
        42:['\b', '\b'],
        43:['\t', '\t'],
        44:[' ', ' '],
        45:['_', '_'],
        46:['=', '+'],
        47:['[', '{'],
        48:[']', '}'],
        49:['\\', '|'],
        50:['#', '~'],
        51:[';', ':'],
        52:["'", '"'],
        53:['`', '~'],
        54:[',', '<'],
        55:['.', '>'],
        56:['/', '?'],
        100:['\\', '|'],
        103:['=', '='],
        }

    # A 2 in first byte seems to indicate to shift the key. For example
    # a code for ';' but with 2 in first byte really means ':'.
    if lst[0] == 2:
        shift = 1
    else:
        shift = 0
        
    # The character to convert is in the third byte
    ch = lst[2]
    if ch not in conv_table:
        print "Warning: data not in conversion table"
        return ''
    return conv_table[ch][shift]



# Find our device using the VID (Vendor ID) and PID (Product ID)
dev = usb.core.find(idVendor=0x05e0, idProduct=0x1200)
if dev is None:
    raise ValueError('USB device not found')

# Disconnect it from kernel
needs_reattach = False
if dev.is_kernel_driver_active(0):
    needs_reattach = True
    dev.detach_kernel_driver(0)
    print "Desatachando el dispositivo USB del kernel driver"

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first IN endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_IN)

assert ep is not None, "Endpoint del dispositivo USB no encontrado. Algo esta mal."

# Loop through a series of 8-byte transactions and convert each to an
# ASCII character. Print output after 0.5 seconds of no data.
line = ''
while True:
    try:
        # Wait up to 0.5 seconds for data. 500 = 0.5 second timeout.
        data = ep.read(1000, 500)  
        ch = hid2ascii(data)
        line += ch
    except KeyboardInterrupt:
        print "Frenando el programa..."
        dev.reset()
        if needs_reattach:
            dev.attach_kernel_driver(0)
            print "Reattachando dispositivo USB al controlador del kernel"
        break
    except usb.core.USBError:
        # Timed out. End of the data stream. Print the scan line.
        if len(line) > 0:
            print " >> Codigo leido: " + line
            print "   >> Largo: " + str(len(line)) + ". Llamando a fotopoc... "
            if len(line)>16:
                print "      >> OK, abriendo puerta."
                led.on()
                sleep(3)
                led.off()
            else:
                print "      >> Rechazado, la cantidad de caracteres es menor al de un boarding."
                led.on()
                sleep(0.2)
                led.off()
                sleep(0.2)
                led.on()
                sleep(0.2)
                led.off()
                sleep(0.2)
                led.on()
                sleep(0.2)
                led.off()
                sleep(0.2)
            line = ''