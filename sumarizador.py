import csv
from tkinter import *

class Dispositivo:
    def __init__(self, nombre, estado, padre, ipt, claro, iao):
        self.nombre = nombre
        self.estado = estado
        self.padre = padre
        self.ipt = ipt
        self.claro = claro
        self.iao = iao
        self.hijos = []

class NOC:
    def __init__(self):
        self.raiz = None

    def monitorear_red(self):
        if self.raiz is None:
            print("No se ha encontrado la raíz.")
            return
        print("Estado de la Red y Circuitos Afectados:")
        print("----------------------------------------")
        self.imprimir_arbol(self.raiz)
        print()  # Agregar una línea en blanco para separar los ciclos de monitoreo
        self.listar_circuitos_afectados(self.raiz)

    def imprimir_arbol(self, dispositivo, nivel=0):
        print("  " * nivel + dispositivo.nombre + ": " + self.obtener_estado(dispositivo.estado) +
              f" (IPT afectados = {dispositivo.ipt}, CLARO afectados = {dispositivo.claro}, IAO afectados = {dispositivo.iao})")
        for hijo in dispositivo.hijos:
            self.imprimir_arbol(hijo, nivel + 1)

    def listar_circuitos_afectados(self, dispositivo):
        afectados_ipt = dispositivo.ipt if dispositivo.estado in [1, 2] else 0
        afectados_claro = dispositivo.claro if dispositivo.estado in [1, 2] else 0
        afectados_iao = dispositivo.iao if dispositivo.estado in [1, 2] else 0
        for hijo in dispositivo.hijos:
            hijo_afectados_ipt, hijo_afectados_claro, hijo_afectados_iao = self.listar_circuitos_afectados(hijo)
            afectados_ipt += hijo_afectados_ipt
            afectados_claro += hijo_afectados_claro
            afectados_iao += hijo_afectados_iao
        print(f"{dispositivo.nombre}: IPT afectados = {afectados_ipt}, CLARO afectados = {afectados_claro}, IAO afectados = {afectados_iao}")
        return afectados_ipt, afectados_claro, afectados_iao

    def obtener_estado(self, estado):
        if estado == 0:
            return "ONLINE"
        elif estado == 1:
            return "OFFLINE"
        elif estado == 2:
            return "UNREACHABLE"
        else:
            return "DESCONOCIDO"

# Leer datos desde el archivo CSV
dispositivos = []
with open('datos.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(reader)  # Saltar la primera fila (cabecera)
    for row in reader:
        nombre = row[0].strip()  # Eliminar espacios en blanco alrededor del nombre
        estado = int(row[1])
        padre = row[2].strip()  # Eliminar espacios en blanco alrededor del nombre del padre
        ipt = int(row[3])
        claro = int(row[4])
        iao = int(row[5])
        dispositivo = Dispositivo(nombre, estado, padre, ipt, claro, iao)
        dispositivos.append(dispositivo)

# Construir la jerarquía de dispositivos
dispositivos_dict = {dispositivo.nombre: dispositivo for dispositivo in dispositivos}
raiz = None
for dispositivo in dispositivos:
    if dispositivo.padre == 'RAIZ':
        raiz = dispositivo
        continue
    if dispositivo.padre in dispositivos_dict:
        dispositivo_padre = dispositivos_dict[dispositivo.padre]
        dispositivo_padre.hijos.append(dispositivo)

# Crear la red NOC y monitorearla
noc = NOC()
noc.raiz = raiz
import time
while True:
    noc.monitorear_red()
    time.sleep(5)  # Esperar 5 segundos antes de volver a monitorear
