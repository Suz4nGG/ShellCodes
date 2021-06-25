#from shellCodeServer import FIN_COMANDO, atender_cliente, inicializar_servidor
import socket 
import sys
# * Definimos el final del comando
FIN_COMANDO = b'#00#'

def leer_respuesta(socket):
    """
    ! Lee el canal de comunicacion del servidor y reconstruye el comando asociado
    """
    salida = socket.recv(2048)
    while not salida.endswith(FIN_COMANDO):
        salida += salida.recv(2048)
    quitar_caracteres = len(FIN_COMANDO)
    return salida[:-quitar_caracteres]

def mandar_comando(comando, socket):
    # ! Espera la respuesta del servidor y la regresa
    comando = comando.encode('UTF-8') # * Es convertida a binario
    comando += FIN_COMANDO
    socket.send(comando)
    salida = leer_respuesta(socket)
    return salida 

def desplegar_salida_comando(salida):
    # ! Vienen en binario, espera la respuesta del servidor y despliega la salida
    salida = salida.decode('UTF-8') # * Convierte a str
    print(salida)

def leer_comandos(socket):
     # ! Interfaz
    comando = ''
    while comando != b'exit':
        comando = input('$> ') # * Prompt lee un str no binario
        respuesta = mandar_comando(comando, socket)
        desplegar_salida_comando(respuesta) 

def inicializar_conexion(host, puerto):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((host, puerto))
    except:
        print('No se entablo la conexion')
        exit(1)
    return cliente
    
if __name__ == '__main__':
    host = sys.argv[1]
    puerto = int(sys.argv[2])
    socket = inicializar_conexion(host, puerto)
    leer_comandos(socket)