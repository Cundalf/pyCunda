import os, shutil, datetime, configparser
from os import scandir, getcwd, path, stat, stat_result, unlink

###################################################
# Autor: Agustin U. Cundari.
# Ver: 0.1.
# Testeado en Python 3.6.6 y 3.7.0
###################################################

# def
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def ls(ruta = getcwd()):
    return [arch for arch in scandir(ruta) if arch.is_file()]

def getOldDate():
    dToday = datetime.datetime.now().date()
    dDays = datetime.timedelta(days = oldRange)
    return (dToday - dDays)

def createDirs():
    listDir = list()
    bRet = True
    
    if cfgImage:
        listDir.append(path + '\\' + nmImage)

    if cfgZip:
        listDir.append(path + '\\' + nmZip)
        
    if cfgAudio:
        listDir.append(path + '\\' + nmAudio)

    if cfgVideo:
        listDir.append(path + '\\' + nmVideo)

    if cfgIso:
        listDir.append(path + '\\' + nmIso)

    if cfgExec:
        listDir.append(path + '\\' + nmExec)
    
    if cfgProg:
        listDir.append(path + '\\' + nmProg)
    
    if cfgDocs:
        listDir.append(path + '\\' + nmDocs)

    if cfgModel:
        listDir.append(path + '\\' + nmModel)

    for sDir in listDir:
        if(not os.path.isdir(sDir)):
            try:
                os.mkdir(sDir, 755)
                print('Created:', sDir)
            except Exception as e:
                print('Error:', e.args)
                bRet = False

    return bRet

# configparser
Config = configparser.ConfigParser()
Config.read(r'config.ini')

# general
configData = ConfigSectionMap('general')
path = os.environ['USERPROFILE'] + '\\Downloads'
oldRange = int(configData["daysold"])

# config - ban
configData = ConfigSectionMap('ban')
cfgImage  = (True if configData['image'] == '1' else False)
cfgZip    = (True if configData['zip'] == '1' else False)
cfgAudio  = (True if configData['audio'] == '1' else False)
cfgVideo  = (True if configData['video'] == '1' else False)
cfgIso    = (True if configData['iso'] == '1' else False)
cfgExec   = (True if configData['exec'] == '1' else False)
cfgProg   = (True if configData['prog'] == '1' else False)
cfgDocs   = (True if configData['docs'] == '1' else False)
cfgModel  = (True if configData['model'] == '1' else False)
cfgDelOld = (True if configData['delold'] == '1' else False)

# config - name
configData = ConfigSectionMap('names')
nmImage = configData['image']
nmZip   = configData['zip']
nmAudio = configData['audio']
nmVideo = configData['video']
nmIso   = configData['iso']
nmExec  = configData['exec']
nmProg  = configData['prog']
nmDocs  = configData['docs']
nmModel = configData['model']

# array
arrImage = ['.jpg', '.png', '.jpeg', '.tiff', '.ico', '.gif']
arrZip   = ['.zip', '.rar', '.tar', '.gz', '.7z']
arrAudio = ['.mp3', '.wav', '.ogg']
arrVideo = ['.mp4', '.avi', '.wmv']
arrIso   = ['.iso', '.dmg']
arrExec  = ['.exe', '.bat', '.msi', '.msu', '.apk', '.torrent']
arrProg  = ['.js', '.css', '.py', '.cs', '.unitypackage', '.db', '.sql']
arrDocs  = ['.doc', '.docx', '.xls', '.xlsx', '.pdf', '.txt', '.html']
arrModel = ['.stl', '.blend', '.psd']


# program
print("=== Agustin Cundari ===")
print("= It's not bad but it's not fabulous =")

if oldRange == 0: cfgDelOld = False
if nmImage == '': exit()
if nmZip   == '': exit()
if nmAudio == '': exit()
if nmVideo == '': exit()
if nmIso   == '': exit()
if nmExec  == '': exit()
if nmProg  == '': exit()
if nmDocs  == '': exit()
if nmModel == '': exit()

b = createDirs()
if (not b):
    exit()

if cfgDelOld:
    fecOld = getOldDate()

# old files
files = ls(path)
for file in files:
    if cfgDelOld:
        dateFile = datetime.datetime.fromtimestamp(stat(file).st_mtime).date()
        if dateFile <= fecOld:
            unlink(file.path)
            print('Deleted:', file.name)

# moving files
files = ls(path)
for file in files:
    sNewDir = ''
    sSub = ''
    i = 0
    sFileExt = os.path.splitext(file.name)[1]
    sBasename = os.path.splitext(file.name)[0]

    # set directory
    if cfgImage:
        if sFileExt in arrImage:
            sNewDir = path + '\\' + nmImage + '\\'

    if cfgZip:
        if sFileExt in arrZip:
            sNewDir = path + '\\' + nmZip + '\\'

    if cfgAudio:
        if sFileExt in arrAudio:
            sNewDir = path + '\\' + nmAudio + '\\'
			
    if cfgVideo:
        if sFileExt in arrVideo:
            sNewDir = path + '\\' + nmVideo + '\\'

    if cfgIso:
        if sFileExt in arrIso:
            sNewDir = path + '\\' + nmIso + '\\' 

    if cfgExec:
        if sFileExt in arrExec:
            sNewDir = path + '\\' + nmExec + '\\'

    if cfgProg:
        if sFileExt in arrProg:
            sNewDir = path + '\\' + nmProg + '\\'

    if cfgDocs:
        if sFileExt in arrDocs:
            sNewDir = path + '\\' + nmDocs + '\\'

    if cfgModel:
        if sFileExt in arrModel:
            sNewDir = path + '\\' + nmModel + '\\'

    # move file
    if(sNewDir != ''):
        try:
            while os.path.isfile(sNewDir + sBasename + sSub + sFileExt):
                i += 1
                sSub = '(' + str(i) + ')'

            sNewDir = sNewDir + sBasename + sSub + sFileExt
                
            shutil.move(file.path, sNewDir )
            print(file.name, ' moved to', sNewDir)
        except Exception as e:
            print('Error:', e.args)

print("Ready!")
input()

