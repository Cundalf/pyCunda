from os import scandir, getcwd, path, stat, stat_result, unlink
import datetime

def ls(ruta = getcwd()):
    return [arch for arch in scandir(ruta) if arch.is_file()]

path = input("Ingrese ruta: ")

if path == "":
	exit()

print("Path:" + path)

iDias = int(input("Cuantos dias desea consevar (ej: 30): "))
if iDias < 0:
	exit()


hoy = datetime.datetime.now().date()
dias = datetime.timedelta(days=iDias)
fec = hoy-dias
print("Se borrara archivos TXT a partir de: " + str(fec))
confirmacion = int(input("Ingrese 1 para comenzar. otro numero para salir. \n "))
if confirmacion != 1:
	exit()

print("Listando archivos...")
files = ls(path)
#print(files)

print("LA PURGA VA A COMENZAR")
for file in files:
	arr = file.name.split('.')
	if arr[-1].lower() == "txt":
		dateFile = datetime.datetime.fromtimestamp(stat(file).st_mtime).date()
		if dateFile <= fec:
			unlink(file.path)
			print("Borrado: " + file.name)
			
