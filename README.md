# raspberry_python

## Uso de ds9208 zebra scanner en Raspberry PI 1
Este proyecto permite el uso del scanner zebra symbol DS9208 con un raspberry pi1 (sobre debian linux).
This project allows to use a scanner zebra symbol DS9208 with a raspberry pi1 (for debian linux).

### Features:
- Barcode Zebra scanner PDF417 support -> OK
- Decode barcode ascii -> OK 
- Suppont for GPIO interface -> OK
- Obtener estado del sensor de ocupación -> OK
- Permitir el paso (abrir puerta) -> OK
- Call Fotopoc api REST -> OK

## GPIO Connections:
- Puerta / Gate:
>N: PIN 6
>P: PIN 11

- Ocupación / Sensor:
>N: PIN 1
>P: PIN 10

## Referencia de conectores:

![alt text](https://raspberrypihq.com/wp-content/uploads/2018/01/a-and-b-physical-pin-numbers.png)

## Script de inicializaion:

**Crear el script y agregar al archivo:**

>$ nano launcher.sh
```
    #!/bin/sh
    # launcher.sh
    cd /
    cd home/pi/
    python fotoread.py
    cd/
```
**Permitir que sea ejecutable:**

>$ chmod 755 launcher.sh

**Iniciar en el startup:**

>$ sudo nano /home/pi/.bashrc

```
    echo Iniciando fotopoc
    sh /home/pi/launcher.sh
```

## Links:

    Gpio:
    https://thepihut.com/blogs/raspberry-pi-tutorials/27968772-turning-on-an-led-with-your-raspberry-pis-gpio-pins

    Scanner model:
    https://www.zebra.com/content/dam/zebra_new_ia/en-us/manuals/barcode-scanners/ds9208-prg-en.pdf

    BarcodeReader:
    https://github.com/vpatron/barcode_scanner_python