from os import scandir, getcwd, path, stat, stat_result, unlink
import sys, subprocess, re, datetime, time, shutil, logging

try:
    import requests
    import json
except:
    print("Falta lib: requests (pip install requests)")
    exit()

def convert2PDF(sPath):
    args = [libreoffice_path, '--headless', '--convert-to', 'pdf', sPath]
    
    process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=vTimeout)
    filename = re.search('-> (.*?) using filter', process.stdout.decode())
    
    if filename is None:
        logging.warning("soffice. Error al convertir: " + sPath)
        print(process.stdout.decode())
        return ""
    else:
        logging.info("soffice. Archivo generado: " + filename.group(1))
        print("Archivo generado: " + filename.group(1))
        return filename.group(1)

def getWS():
    return ["localhost", "8085"]

def executeCache(sMServer, sMNamespace, arrDatos, sFunction, sGlobal, sGlobalIndex):
    
    #print(os.path.basename(your_path))
    
    server = getWS()
    vdata=[("P0", arrDatos[0]),("P1", arrDatos[1]),("P2", arrDatos[2]),("P3", arrDatos[3]),("P4", arrDatos[4]),
        ("P5", arrDatos[5]) ,("P6", arrDatos[6]),("P7", arrDatos[7]),("P8", arrDatos[8]),("P9", arrDatos[9]),
        ("code", sFunction),("global", sGlobal), ("mserver", sMServer),
        ("namespace", sMNamespace),("global_index", sGlobalIndex)]
 
    try:
        time.sleep(1)
        r = requests.post("http://" + server[0] + ":" + server[1] + "/Ejecutar", data=vdata, timeout=15)
        
        if (r.status_code == 200):
            r.encoding
            res = r.text.replace("\\","\\\\")
            return json.loads(res)
        else:
            logging.warning("WS ERROR. executeCache: Response Error. (" + r.status_code + ")")
            print("executeCache: Response Error. " + r.status_code)
            return []
    except:
        logging.warning("WS ERROR. executeCache: Internal Error.")
        print("executeCache: Internal Error.")
        return []

def checkFile(path):
    sPath = path.dirname(path)
    sName = path.basename(path)
    sExt = path.splitext(sName)[-1].lower()
    i = 0
    sNewPath = sPath + sName + sExt

    while not path.isfile(sNewPath):
        i += 1
        sNewPath = sPath + sName +  "_" + str(i) + sExt
    
    return sNewPath

# Program
print("--- pyDemonPDF ---")

logging.basicConfig(filename='pyDemonPDF.log', level=logging.DEBUG)
logging.info("Script iniciado")

# Vars - General
libreoffice_path = "C:\\Program Files\\LibreOffice\\program\\soffice.exe"
vTimeout = None
allowedExt = [".doc", ".docx", ".xls", ".xlsx", ".pdf"]
bStarted = False
sEmpresaActual = "SLL"

# Vars - Fileserver
BKPPATH = "\\\\SERVER\\estudios-doc\\"
ESTPATH = "\\\\SERVER\\Estudios\\"

# Vars - Web Service
server = "LOCALHOST"
namespace = "TEST"

while True:
    if bStarted:
        time.sleep(1200)
    else:
        time.sleep(5)
        bStarted = True

    sGlobalIndex = "PYDEMONPDF"
    arr = [sGlobalIndex, "", "", "", "", "", "", "", "", ""]
    sFunction = "D DEPURADORADJ^CUNDA(P0,.P9)"
    sGlobal = "^CUNDA"
    jResponse = executeCache(server, namespace, arr, sFunction, sGlobal, sGlobalIndex)
    
    if(len(jResponse) == 0):
        logging.warning("(DEPURADORADJ) DB Warning. No data response")
        print("(DEPURADORADJ) DB Warning. No data response")
        continue
    else:
        if(jResponse["errors"]["errorname"] != ""):
            logging.warning("(DEPURADORADJ) DB Error: " + jResponse["error"]["errorname"])
            print("(DEPURADORADJ) DB Error: " + jResponse["error"]["errorname"])
            continue

        if(jResponse["params"]["P9"] != "0"):
            logging.warning("(DEPURADORADJ) DB Warning. No data response")
            print("(DEPURADORADJ) DB Warning. No data response")
            continue

        if(jResponse["global"] == None):
            logging.warning("(DEPURADORADJ) No data response.")
            print("(DEPURADORADJ) No data response.")
            continue

    dataGlobal = jResponse["global"]

    for pacFile in dataGlobal:
        sID = pacFile[0]
        sSaf = pacFile[1]
        sIdPrepaga = pacFile[2]
        sAfiliado = pacFile[3]
        sFile = pacFile[4]

        sExt = path.splitext(sFile)[-1].lower()

        # Valido la extension
        if not sExt in allowedExt:
            print("Ignorado: " + sFile)
            continue

        # Controlo que exista
        if not path.isfile(sFile):
            print("No se encontro archivo " + sFile)

            # Lo anulo en la DB
            arr = [sID, "ANULADO^" + sFile, "", "", "", "", "", "", "", ""]
            sFunction = "D MARCARADJ^CUNDA(P0,P1)"
            sGlobal = ""
            sGlobalIndex = ""
            jResponse = executeCache(server, namespace, arr, sFunction, sGlobal, sGlobalIndex)
            
            if(jResponse["errors"]["errorname"] != ""):
                logging.warning("(MARCARADJ) DB Error: " + jResponse["error"]["errorname"])
                print("(MARCARADJ) DB Error: " + jResponse["error"]["errorname"])

            continue

        # Determino nuevos Path
        # Directorio primario
        sDestinoPRY =  sFile.replace(sExt, ".pdf")
        # Backup
        sDestinoBKP = BKPPATH + sIdPrepaga + "-" + sAfiliado + "-" + sSaf + sExt
        sDestinoBKP = checkFile(sDestinoBKP)
        # Estudios
        sDestinoEST = ESTPATH + path.basename(sFile)
        sDestinoEST = checkFile(sDestinoEST)

        if sExt != ".pdf":
            # Lo convierto a PDF
            sNewPDF = convert2PDF(sFile)
            
            # Controlo que se haya generado correctamente
            if not path.isfile(sNewPDF):
                logging.warning("No se encontro archivo PDF generado.")
                print("No se encontro archivo PDF generado.")
                continue

            # Solo en la conversion me fijo si ya existe el pdf
            sDestinoPRY = checkFile(sDestinoPRY)
        else:
            sNewPDF = sDestinoPRY

        try:
            if sExt != ".pdf":
                # Copio el pdf generado al mismo directorio que el archivo original
                shutil.copyfile(sNewPDF, sDestinoPRY)
                
                if not path.isfile(sDestinoPRY):
                    raise Exception('No se pudo copiar archivo al directorio primario.')

                # Copio un backup del original y lo elimino del repositorio
                shutil.copyfile(sNewPDF, sDestinoBKP)

                if path.isfile(sDestinoBKP):
                    logging.info("Archivo eliminado: " + sFile)
                    unlink(sFile)

            # Copio el PDF al repositorio de estudios
            shutil.copyfile(sNewPDF, sDestinoEST)
            
            if not path.isfile(sDestinoEST):
                raise Exception('No se pudo copiar archivo al directorio de estudios.')
            
            # Si llegamos hasta aca es que todo salio muy bien, o muy mal. Esperando que todo haya salido bien... Grabo en la DB
            arr = [sID, sDestinoEST + "^" + sDestinoPRY, "", "", "", "", "", "", "", ""]
            sFunction = "D MARCARADJ^CUNDA(P0,P1)"
            sGlobal = ""
            sGlobalIndex = ""
            jResponse = executeCache(server, namespace, arr, sFunction, sGlobal, sGlobalIndex)
            
            if(jResponse["errors"]["errorname"] != ""):
                raise Exception("(MARCARADJ) DB Error: " + jResponse["error"]["errorname"])
            else:
                unlink(sNewPDF)
                logging.info("Archivo eliminado: " + sNewPDF)

        except Exception as error:
            logging.error(repr(error))
            print(repr(error))
            if not path.isfile(sNewPDF):
                unlink(sNewPDF)
                logging.info("Archivo eliminado: " + sNewPDF)
                continue