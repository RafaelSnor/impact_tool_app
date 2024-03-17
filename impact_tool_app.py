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
            return "No se ha encontrado la raíz."
        return self.imprimir_arbol(self.raiz)

    def imprimir_arbol(self, dispositivo, nivel=0):
        resultado = "Estado de la Red y Circuitos Afectados:\n----------------------------------------\n"
        resultado += "  " * nivel + dispositivo.nombre + ": " + self.obtener_estado(dispositivo.estado) + \
                     f" (IPT afectados = {dispositivo.ipt}, CLARO afectados = {dispositivo.claro}, IAO afectados = {dispositivo.iao})\n"
        for hijo in dispositivo.hijos:
            resultado += self.imprimir_arbol(hijo, nivel + 1)
        return resultado

    def listar_circuitos_afectados(self, dispositivo):
        afectados_ipt = dispositivo.ipt if dispositivo.estado in [1, 2] else 0
        afectados_claro = dispositivo.claro if dispositivo.estado in [1, 2] else 0
        afectados_iao = dispositivo.iao if dispositivo.estado in [1, 2] else 0
        for hijo in dispositivo.hijos:
            hijo_afectados_ipt, hijo_afectados_claro, hijo_afectados_iao = self.listar_circuitos_afectados(hijo)
            afectados_ipt += hijo_afectados_ipt
            afectados_claro += hijo_afectados_claro
            afectados_iao += hijo_afectados_iao
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

def mostrar_resultado():
    resultado_monitoreo = noc.monitorear_red()
    afectados_ipt, afectados_claro, afectados_iao = noc.listar_circuitos_afectados(noc.raiz)
    resultado = f"\nIPT afectados = {afectados_ipt}, CLARO afectados = {afectados_claro}, IAO afectados = {afectados_iao}" + resultado_monitoreo
    cotizacion.config(text=resultado)

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

# Crear la red NOC
noc = NOC()
noc.raiz = raiz

# Configurar la interfaz gráfica
janela = Tk()
janela.title('Monitor de Red')

texto = Label(janela, text='Estado de la Red y Circuitos Afectados:')
texto.grid(column=0, row=0)

boton = Button(janela, text='Monitorear Red', command=mostrar_resultado)
boton.grid(column=0, row=1)

cotizacion = Label(janela, text='')
cotizacion.grid(column=0, row=2)

janela.mainloop()
