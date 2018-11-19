#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""
import sys
import socketserver
import os

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            linea_decod = line.decode('utf-8').split(" ")
            if (len(linea_decod) != 3 or not 'sip:' in linea_decod[1]
                or not '@' in linea_decod[1] or not 'SIP/2.0\r\n\r\n' in linea_decod[2]):
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
                break
            metodo = linea_decod[0]
            print (metodo)
            if metodo == 'INVITE':
                self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
                self.wfile.write(b"SIP/2.0 180 Ringing\r\n\r\n")
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                break

            if metodo == 'ACK':
                aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + sys.argv[3]
                print("Vamos a ejecutar", aEjecutar)
                os.system(aEjecutar)
                break

            if metodo == 'BYE':
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                break

            else:
                self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
                break
            # Si no hay más líneas salimos del bucle infinito
            if not line  :
                break


if __name__ == "__main__":
    try:
        port = int(sys.argv[2])
        serv = socketserver.UDPServer(('', port), EchoHandler)
        print('Listening...')
        try:
            serv.serve_forever()
        except KeyboardInterrupt:
            print("Finalizado servidor")
    except (IndexError, ValueError, PermissionError):
        print("Usage: phython3 server.py IP port audio_file")
