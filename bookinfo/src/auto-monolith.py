#!/usr/bin/python


#PRACTICA CREATIVA 2



#Andres Emilio Flores Reina


#Luis Trave Renesses


#Alvaro Torroba De Linos



import os, sys, subprocess, json

from subprocess import call

from lxml import etree





#MAIN FUNCTIONS


def prepare ():

	#Obtener working directory

	cwd = os.getcwd()

	path = cwd + "/cdps-vm-base-p1.img"


	#Usar libreria lxml
	
	tree = etree.parse(cwd + "/cdps-vm-base-p1.xml")

	root = tree.getroot()


	#Definir nombre de la imagen

	sourceFile = root.find("./devices/disk/source")

	sourceFile.set("file", path)

	fout = open(cwd + "/cdps-vm-base-monolith.xml", "w")

	fout.write(etree.tounicode(tree, pretty_print = True))

	fout.close()


	#Definir MV

	call(["sudo", "virsh", "define", cwd + "/cdps-vm-base-monolith.xml"])


	#Copiar aplicacion a la MV
	
	path = cwd + "/productpage"

	call(["sudo", "virt-copy-in", "-d", "s1-monolith", path, "/home"])


	#Mensaje

	print("\n¡Servidor creado y aplicacion descargada!\n")



def launch():

	#Arrancar s1-monolith y mostrar su consola

	call(["sudo", "virsh", "start", "s1-monolith"])

	#os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's1-monolith' -e 'sudo virsh console s1-monolith' &")



def stop() :

	#Apagado de la MV

	call(["sudo", "virsh", "shutdown", "s1-monolith"])



def release() :

	#Apagado de la MV

	call(["sudo", "virsh", "shutdown", "s1-monolith"])

	
	#Eliminar MV

	call(["sudo", "virsh", "undefine", "s1-monolith"])



def start() :
	
	#Mensaje

	print("\n     Escribe la contraseña, ejecuta el comando _ sudo python3 /home/productpage/auto-monolith-vm.py start _ y la aplicacion sera accesible desde 192.168.122.100:9080/productpage\n")
	
	call(["ssh", "cdps@192.168.122.100", "-y"])

	#Instalar pip
		
	call(["apt-get", "update"])

	call(["apt-get", "install", "-y", "python3-pip"])

	
	#Instalar las dependencias	
	
	call(["pip3", "install", "-r", "/home/productpage/requirements.txt"])

	
	#Lanzar el servicio en el puerto 9080
	call(["python3", "/home/productpage/productpage_monolith.py", "9080"])



#CONSOLE INPUT


arguments = sys.argv


if len(arguments) >= 2 :

	if arguments[1] == "prepare":
		prepare()


	if arguments[1] == "launch":
		launch()


	if arguments[1] == "stop":
		stop()


	if arguments[1] == "release":
		release()


	if arguments[1] == "start":
		start()


else:


	print("Not enough arguments")




