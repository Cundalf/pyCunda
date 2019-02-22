#!/usr/bin/python
import time, os, socket, sys, datetime
from subprocess import call

# import lib: ConfigParser
try:
    import configparser
except:
    print("Falta lib: requests. Probar: pip install configparser")
    try:
        input()
    except:
        exit()
    exit()

# import lib: psutil
try:
    import psutil
except:
    print("Falta lib: requests. Probar: pip install psutil")
    try:
        input()
    except:
        exit()
    exit()

# import lib: request
try:
    import requests
    import json
except:
    print("Falta lib: requests. Probar: pip install requests")
    try:
        input()
    except:
        exit()
    exit()

#config
Config = configparser.ConfigParser()
Config.read(r"config.ini") # path

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def checkProcess():
    return (process in (p.name() for p in psutil.process_iter()))

def reiniciarServicio(): # Finaliza los procesos y los ejecuta nuevamente.

    # Cierra procesos
    for x in range(0, 3):
        os.system("taskkill /f /im " + process)
        time.sleep(2)
        if checkProcess():
            print(str(datetime.datetime.now()) + " No se cerraron los procesos.")
        else:
            print(str(datetime.datetime.now()) + " Procesos cerrados.")
            break

    # Ejecuta
    call(execPath) 
    print(str(datetime.datetime.now()) + " Ejecucion realizada.")

def controlaWS(): # Controla el estado de los WS
    bRes = True
    for port in arrPort:

        arr=[("P0", ipServer),("P1", port),("P2", "KILLPY"),("P3", ""),("P4", ""),
             ("P5", "") ,("P6", ""),("P7", ""),("P8", ""),("P9", ""),
             ("code", "D TESTWS^CUNDA(P0,P1,P2,.P9)"),("global", ""),
             ("mserver", servercache), ("namespace", namespace),("global_index", "")]

        try:
            r = requests.post("http://" + ipServer + ":" + port + "/Ejecutar", data=arr, timeout=30)

            if (r.status_code == 200):
                res = r.json()
                if (res["params"]["P9"] != "OK"):
                    print("Puerto: " + port)
                    bRes = False
            else:
                print("Puerto: " + port)
                print(str(datetime.datetime.now()) + " Respuesta negativa: ", r.status_code)
                bRes = False
        except:
            print("Puerto: " + port)
            print(str(datetime.datetime.now()) + " Se produjo un error al comprobar el WS. ", sys.exc_info()[0])
            bRes = False

        time.sleep(1)

        if(not bRes):
            break

    return bRes

configData = ConfigSectionMap("general")
# config - general
execPath = configData['batpath']
process = configData["processname"]
iTiempo = int(configData["interval"])
iCantMax = int(configData["intentos"])
arrPort=configData["arrports"].split(",")

# config - VisM
servercache = "localhost"
namespace = "TEST"

# Declaraciones
iCantReset = 0
iCantIntentos = 0
bEstado = False
ipServer = socket.gethostbyname(socket.gethostname())

# Code
print(datetime.datetime.now())
print(ipServer)
print("Bienvenido! Leer:")
print("--> Una vez abierto NO TOCAR NADA al menos que se lo pida explicitamente este Script.")
print("--> Para finalizar el script realice una interrupcion (ej: CTRL+C) y espere unos instantes.")
print("--> Usar con responsabilidad.")
print("--> Lok'tar ogar")
print("-")
print("Configuracion cargada:")
print("--> Server: " + ipServer)
print("--> Path: " + execPath)
print("--> Process: " + process)
print("--> Intervalo: " + str(iTiempo))
print("--> Intentos: " + str(iCantMax))
print("--> Puertos: ", arrPort)
print("-")

try:
    while True:
        time.sleep(iTiempo)
        bEstado = controlaWS()
        if(bEstado):
            print(str(datetime.datetime.now()) + " Servicio OK.")
            iCantIntentos = 0
        else:
            iCantIntentos += 1
            if(iCantIntentos >= iCantMax):
                reiniciarServicio()
                iCantReset += 1
                
except KeyboardInterrupt:
    print("Se reinciciaron los servicios: " + str(iCantReset) + " veces.")
    print("Hasta la proxima!")
    print(datetime.datetime.now())
    try:
        input()
    except:
        exit()
