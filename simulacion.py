class Simulacion():
    def __init__(self, datos, datos_tabla):
        self.datos = datos
        self.datos_tabla = datos_tabla
        print('Lectura Datos')
        print(datos_tabla)

class Dispositivo():
    def __init__(self,nombre, tiempo_inicial, duracion, prioridad):
        self.nombre = nombre
        self.tiempo_inicial = tiempo_inicial
        self.duracion = duracion
        self.prioridad = prioridad
        self.cola = []

class Programa():
    def __init__(self, tiempo_inicial, duracion, prioridad):
        self.tiempo_inicial = tiempo_inicial
        self.duracion = duracion
        self.prioridad = prioridad
