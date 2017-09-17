#!/usr/bin/env python
# -*- coding: utf-8 -*-
# importamos el modulo socket
from __future__ import unicode_literals
import socket
import json
from StringIO import StringIO



class grabarRFID:

    def grabar(self, puerto, dni):
        try:
            # instanciamos un objeto para trabajar con el socket
            #a= socket.settimeout(10)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM,)
            #s.settimeout(1000)
            print("Entro en socket")
            s.bind(("", puerto))
            # Con el metodo bind le indicamos que puerto debe escuchar y de que servidor esperar conexiones
            # Es mejor dejarlo en blanco para recibir conexiones externas si es nuestro caso


            # Aceptamos conexiones entrantes con el metodo listen, y ademas aplicamos como parametro
            # El numero de conexiones entrantes que vamos a aceptar
            s.listen(1)

            # Instanciamos un objeto sc (socket cliente) para recibir datos, al recibir datos este
            # devolvera tambien un objeto que representa una tupla con los datos de conexion: IP y puerto
            sc, addr = s.accept()

            # Recibimos el mensaje, con el metodo recv recibimos datos y como parametro
            # la cantidad de bytes para recibi",r

            try:
                recibido = json.loads(sc.recv(1024))
                print recibido
                estado = recibido["estado"]

                if estado == "OK":
                    enviado = "{\"accion\":\"1\",\"dni\":\""+ dni +"\"}"
                    sc.send(enviado)
                    print "datos enviados: " + enviado
                    enviado = json.loads(enviado)
                    recibido2 = json.loads(sc.recv(1024))
                    print recibido2
                    if enviado["dni"] == recibido2["dni"]:
                        print "entra"
                        enviado = '{"estado":"OK"}'
                        sc.send(enviado)
                        sc.close()
                        s.close()
                        recibido2=str(recibido2["uid"])
                        return recibido2
                    else:
                        enviado = '{"estado":"FAIL"}'
                        sc.send(enviado)
                        sc.close()
                        s.close()
                        return None
                else:

                    sc.close()
                    s.close()
                    return None

                # Cerramos la instancia del socket cliente y servidor
                sc.close()
                s.close()
            except:
                return None
        except:
            return None

