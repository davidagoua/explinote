#-*- coding:utf-8 -*-

import os
import time
from Tkinter import *
from socket import *
from thread import start_new_thread

app=socket(AF_INET, SOCK_STREAM)
hebergeur=False
cpu=None


def listen():
	if hebergeur:
		msg=cpu.recv(1024)
	else:
		msg=app.recv(1024)
	text.insert(END, time.strftime('#[%H:%M:%S]'))
	text.insert(END, '%s\n'%msg)


def heberger():
	global hebergeur, cpu
	hebergeur=True
	app.bind(('', 4001))
	app.listen(2)
	cpu, info=app.accept()
	text.insert(END,"[{}]Nouvelle connection !\n".format(info[0]))
	while True:
		isOK=True
		if isOK:
			start_new_thread(listen, ())
			isOK=False

def connection():
	host=host_input.get()
	app.connect((host, 4001))
	text.insert(END, 'Connexion etablir\n')
	while True:
		isOK=True
		if isOK:
			start_new_thread(listen, ())
			isOK=False

def send_msg():
	msg=host_input.get()
	if hebergeur:
		buff=cpu.send(msg)
	else:
		buff=app.send(msg)
	text.insert(END, time.strftime('[%H:%M:%S]'))
	text.insert(END, '%s\n'%msg)
	host_input['text']=''


root=Tk()
btn_recv=Button(root, text='Heberger', command=heberger).grid(row=2, column=4)
text=Text(root)
text.grid(row=1, column=1, columnspan=4)
scroll=Scrollbar(root, orient='vertical', command=text.yview)
scroll.grid(row=1, column=5, sticky='ns')
text['yscrollcommand']=scroll.set
text['background']="blue"
text.tag_configure("class", font="red 1")
host=StringVar()
host_input=Entry(root, textvariable=host, width=70)
host_input.grid(row=2, column=1)
btn_conn=Button(root, text='Se connecter', command=connection).grid(row=2, column=3)
btn_send=Button(root, text="**Envoyer**", command=send_msg).grid(column=2, row=2)

if __name__ == '__main__':
	root.mainloop()
