#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  phishingnemesis.py
#
#  Copyright 2012 alex ricardo rincon silva
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
import urllib2
import json
import bz2
import socks
import socket
fuente = open('clients.txt')
listacruda = fuente.readlines()
clientes = []
for gg in listacruda:
    clientes.append(gg.strip())
clientes = filter(lambda paso: paso != "", clientes)


def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock


socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

# patch the socket module
socket.socket = socks.socksocket
socket.create_connection = create_connection


def obtenerjson():
    dictamen, aaa = {}, 0
    listacompletajson = json.loads(
        bz2.decompress(
            urllib2.urlopen(
                "http://data.phishtank.com/data/d36cbdb437d93a6e20d8b59b77" +
                "24a7aeaddd397d06f03150a2c1d4504f794944/online-valid.json.bz2"
            ).read()
        )
    )
    for i in listacompletajson:
        if len(i["details"]) < 1:
            print i['target']
            dictamen[i['url']] = [i["details"], i["target"]]
            aaa = aaa + 1
        else:
            dictamen[i['url']] = [i["details"][0]['ip_address'], i["target"]]
    print "registros en mal estado --- ", aaa
    del(listacompletajson)
    return dictamen


def identificar(ruta, clientes):
    try:
        peticion = urllib2.Request(ruta)
        peticion.add_header('User-agent', 'Mozilla/5.0 (Windows NT 10.0; ' +
                            'WOW64; rv:56.0) Gecko/20100101 Firefox/56.0')
        fijar = urllib2.urlopen(peticion)
        contenido = fijar.read().lower()
        for paso in clientes:
            if contenido.find(paso.lower()) >= 0:
                ubicacion = contenido.find(paso.lower())
                coecion = str(contenido[ubicacion-3:ubicacion+len(paso)+3])
                fijo = coecion+"<=|@|ALERTA|@|=|@|ALERTA|@|==|"
                # print
                break
            else:
                fijo = "Seguro"
    except Exception, ex:
        contenido = "nada", ex
        print "error", ruta
        fijo = "nada "+str(ex)
    return fijo


if __name__ == '__main__':
    print "procesando fuente..."
    estructura = obtenerjson()
    print "terminada la descarga procesando registros..."
    targets = len(estructura)
    print "son ", targets, "-registros iniciando revision"
    print "......"
    contador = 0
    resultado = open('resultado.txt', 'w')
    for i in estructura:
        contador = contador + 1
        progreso = str(float(contador*100.00/targets))
        estructura[i][1] = identificar(i, clientes)
        tipourl = estructura[i][1]
        if tipourl != 'Seguro':
            tipourl = str(estructura[i][0]) + tipourl
            resultado.write(i+" -- "+tipourl+"\n")
            print progreso, i, tipourl
        else:
            print str(progreso)[0:5]+"%", i[0:20], tipourl