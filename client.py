#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente que abre un socket a un servidor."""
import sys
import socket

# Cliente UDP simple.

# Dirección IP del servidor.
SERVER = 'localhost'
method = sys.argv[1]
sip_address = sys.argv[2].split(':')[0]
port = int(sys.argv[2].split(':')[1])

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_socket.connect((SERVER, port))
        if method == 'INVITE' or method == 'BYE':
            line = (method + ' sip:' + sip_address + ' SIP/2.0\r\n\r\n')
            print(line)
            my_socket.send(bytes(line, 'utf-8'))
            data = my_socket.recv(1024)
            print(data.decode('utf-8'))
        else:
            print("Solo puedes enviar Métodos INVITE o BYE")

        if method == 'INVITE' and data.decode('utf-8').split()[-2] == '200':
            linea = ('ACK' + ' sip:' + sip_address + ' SIP/2.0\r\n\r\n')
            my_socket.send(bytes(linea, 'utf-8'))
            data = my_socket.recv(1024)
            print(data.decode('utf-8'))
    print("Socket terminado.")

except (IndexError, ValueError):
    print("Usage: python3 client.py method receiver@IP:SIPport")

except ConnectionRefusedError:
    print("Servidor apagado / Error de puerto. ")
