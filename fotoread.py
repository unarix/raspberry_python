import usb.core
import usb.util
import time
import requests
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import json
from time import sleep

# ****************************************************************************************
# Registro de cambios
# nhtello 25/6/2020: initial
# nhtello 13/8/2020: demo onsite
#****************************************************************************************

GPIO.setwarnings(False) # Ignore warning
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input of fotopoc sensor, if pin 10 is HIGH a person is located between the way
GPIO.setup(11, GPIO.OUT) # Set pin 11 to be an output, this is only for test, turn on a led.

# Load fpoc config from conf.json file, example:
# {
#     "url":"http://sample.com.ar/GetBoardingDataPOC?line=",
#     "params":"&idPoc=10.218.0.58&idarpt=EZE/C&usuario=NTELLO&movtp=I&tasap=I&idpocDesc=NTELLO",
# }
with open("config.json") as conf_file:
    conf = json.load(conf_file)

def callFotopoc(boarding):
    # Call API fotopoc
    try:
        url = conf["url"] + boarding + conf["params"]
        payload = {}
        headers = {
        'key': 'TOKEN'
        }
        response = requests.request("GET", url, headers=headers, data = payload)
        print(response.text.encode('utf8'))
        return ("DiaJuliano" in response.text.encode('utf8'))
    except:
        print("Error en la llamada fotopoc")
        return False

def hid2ascii(lst):
    try:
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
    except:
        return '#'

# Find our device using the VID (Vendor ID) and PID (Product ID)
dev = usb.core.find(idVendor=0x05e0, idProduct=0x1200)
if dev is None:
    raise ValueError('No esta conectado el dispositivo USB')

# Disconnect it from kernel
needs_reattach = False
if dev.is_kernel_driver_active(0):
    needs_reattach = True
    dev.detach_kernel_driver(0)
    print "Listo \n"
    
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
    if GPIO.input(10) == GPIO.LOW: # Si el sensor no me advierte de que hay una persona, entonces puedo operar.
        try:
            data = ep.read(1000, 500)  # Espero 0.5 segundos antes de lanzar el except de nodata.
            ch = hid2ascii(data) # Convierto lo que viene del scanner a caracter
            line += ch # lo sumo a la linea
        except KeyboardInterrupt:
            print "Frenando el programa..."
            dev.reset()
            if needs_reattach:
                dev.attach_kernel_driver(0)
                print "Reatachando dispositivo USB al controlador del kernel"
            break
        except usb.core.USBError: # Timed out. se termino el stream de datos, paso la linea escaneada
            if len(line)>10: # Si es mayor a 10 (cant) de caracteres aparentemente no es basura, me fijo si empieza con M1/M2/M3.
                print "Codigo leido: " + line
                print "  > Largo: " + str(len(line))
            
            if (line.startswith('M1') or line.startswith('M1') or line.startswith('M3') or line.startswith('M4')): # Si empieza bien formado lo tengo en cuenta
                if len(line)>16: # todo: si es mayor a x cant de caracteres es un boarding valido.
                    print "Codigo leido: " + line
                    print "  > Largo: " + str(len(line)) + ". Llamando a fotopoc... "
                    
                    # Si la respuesta contiene OK entonces abro la puerta, de lo contrario enciendo luz roja
                    if (callFotopoc(line)==True):
                        print "    > OK, abriendo puerta."
                        GPIO.output(11,GPIO.HIGH) # envio senal al 11 que abra la puerta
                        sleep(1)
                        GPIO.output(11,GPIO.LOW) # apago la senal
                    else:
                        print "    > OK, no habilitado."
                else:
                    print "    > Rechazado, la cantidad de caracteres es menor a la de un boarding."
            line = ''
        except:
            print "Error desconocido, debe reiniciar el thread por completo."