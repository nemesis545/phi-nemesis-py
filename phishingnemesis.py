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
#  .
#  
import urllib2
from xml.dom import minidom
import os
clientes = ('Banco','Bancolombia','Falabela','Positiva','Davivienda')
def obtenerxml():
    os.system("wget -qO- /tmp/online-valid.xml.bz2 http://data.phishtank.com/data/d36cbdb437d93a6e20d8b59b7724a7aeaddd397d06f03150a2c1d4504f794944/online-valid.xml.bz2 | bzip2 -d > /tmp/online-valid.xml")
    listacompletaxml = minidom.parse('/tmp/online-valid.xml')
    listaentradas = listacompletaxml.getElementsByTagName( 'entry' )
    dictamen = { x.getElementsByTagName( 'url' )[0].firstChild.nodeValue:[listaentradas[y].getElementsByTagName( 'ip_address' )[0].firstChild.nodeValue,"texto"] for y,x in enumerate(listaentradas) }
    del(listacompletaxml)
    #del(listaentradas)
    return dictamen
def identificar(ruta,clientes):
    try:
        fijar = urllib2.urlopen(ruta)
        contenido = fijar.read().lower()
    except Exception, ex:
        contenido = "nada"
        print "error",ruta
    for paso in clientes:
        if contenido.find(paso.lower()) >= 0:
            ubicacion = contenido.find(paso.lower())
            coecion = str(contenido[ubicacion-3:ubicacion+len(paso)+3])
            fijo = coecion+"<====|@|ALERTA|@|============|@|ALERTA|@|==========="
            #print 
            break
        else:
            fijo = "Seguro"
    return fijo


if __name__ == '__main__':
    os.system("clear")
    print "procesando xml..."
    estructura = obtenerxml()
    print "terminada la descarga procesando registros..."
    targets = len(estructura)
    print "son ",targets,"-registros iniciando revision"    
    print "......"
    contador = 0
    for i in estructura :
        contador = contador + 1
        progreso = str(float(contador*100.00/targets))
        estructura[i][1] = identificar(i,clientes)
        tipourl = estructura[i][1]
        if tipourl !='Seguro':
            tipourl = str(estructura[i][0]) + tipourl
            print progreso,i,tipourl
        else:
            print str(progreso)[0:5]+"%",i[0:20],tipourl
