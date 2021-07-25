class Simulacion():
    def __init__(self, datos, datos_tabla):
        self.datos = datos # Lista
        self.datos_tabla = datos_tabla # Lista de diccionarios
        print('Lectura Datos')
        print(datos_tabla)

        # Creacion de Objetos Programa
        self.programa = Programa(self.datos['tiempo_inicio_programa'],self.datos['duracion_programa'],40)
        
        # Cantidad de Peticiones no repetidas
        self.listado_peticiones_unicas = self.get_interrupciones_unicas(self.datos_tabla) # diccionario
        #print(self.listado_peticiones_unicas)
        # Cantidad de columnas tabla
        columnas = len(self.listado_peticiones_unicas)


        # Creacion de Objetos Dispositivos
        self.dispositivos = []
        self.listado_nombre_dispositivos = []
        for dispositivo in self.listado_peticiones_unicas:
            self.dispositivos.append(Dispositivo(dispositivo['dispositivo'],dispositivo['prioridad']))
            self.listado_nombre_dispositivos.append(dispositivo['dispositivo'])
        #print(self.dispositivos)


        #Creacion de Objetos Interrupcion
        self.interrupciones = []
        for dato in self.datos_tabla:
            dispositivo = self.buscar_dispositivo(dato['nombre']) # objeto Dispositivo
            self.interrupciones.append(Interrupcion(dispositivo,dato['tiempo_inicio'],dato['duracion']))
        #print(self.interrupciones)

        self.simular()

    def simular(self):
        # Inicializacion de la Simulacion
        proceso_actual = self.programa # Puede ser el programa o interrupcion
        self.tiempo_start = self.programa.tiempo_inicio
        self.tiempo = self.programa.tiempo_inicio
        indice_interrupcion = 0

        while self.programa.duracion >= 0:
            print(self.tiempo)
            if proceso_actual == self.programa:
                print(proceso_actual)
            else:
                print(proceso_actual.dispositivo.nombre)

            indice_interrupcion = self.buscar_tiempo(self.tiempo)
            if indice_interrupcion != "":
                #Revisar si hay algun proceso en cola de mayor prioridad
                interrupcion_actual = self.cambiar_proceso(indice_interrupcion)
                # proceso_actual
                revision_prioridad = self.revisar_prioridad(proceso_actual, interrupcion_actual)
                # Verificar que la interrupcion actual puede detener al proceso
                # = self.cambiar_prioridad(self.tiempo, interrupcion_actual)

                if interrupcion_actual == revision_prioridad:
                    #Cambiar Proceso por inicio de interrupcion
                    if proceso_actual == self.programa:

                        self.addBitacora(proceso_actual,self.tiempo_start, self.tiempo)
                    else:
                        self.addBitacora(proceso_actual.dispositivo,self.tiempo_start, self.tiempo)
                    # Enviar a cola el tiempo que falta
                    if proceso_actual == self.programa:
                        self.addCola(proceso_actual,proceso_actual.duracion)
                    else:
                        self.addCola(proceso_actual.dispositivo,proceso_actual.duracion)
                    proceso_actual = interrupcion_actual
                    #Actualizar tiempo de inicio
                    self.tiempo_start = self.tiempo
                else:
                    #self.addCola(proceso_actual.dispositivo,proceso_actual.duracion)
                    self.addCola(interrupcion_actual.dispositivo,interrupcion_actual.duracion)
                    #.addBitacora(proceso_actual.dispositivo,self.tiempo_start, self.tiempo)
                    #proceso_actual = proceso_cola
                    #Actualizar tiempo de inicio
                    #self.tiempo_start = self.tiempo
                    
                   
            if proceso_actual.duracion == 0:
                # Cambiar de Proceso por finalizacion de Proceso  usar prioridades Ver Prioridad)
                #Actualizar tiempo de inicio
              
                if proceso_actual == self.programa:
                    self.addBitacora(proceso_actual,self.tiempo_start, self.tiempo)
                else:
                    self.addBitacora(proceso_actual.dispositivo,self.tiempo_start, self.tiempo)
                # Enviar a cola el tiempo que falta
                if proceso_actual == self.programa:
                    self.addCola(proceso_actual,proceso_actual.duracion)
                else:
                    self.addCola(proceso_actual.dispositivo,proceso_actual.duracion)
                    proceso_actual = self.cambiar_prioridad(self.tiempo, self.programa)
                    self.tiempo_start = self.tiempo
                #print(proceso_actual)
            self.tiempo += 1
            proceso_actual.duracion -= 1

        print('BITACORA PROGRAMA')
        print(self.programa.bitacora)
        for dispositivo in self.dispositivos:
            print(f"BITACORA {dispositivo.nombre}\n")
            print(dispositivo.bitacora)
        print('colas')
        print('COLA PROGRAMA')
        print(self.programa.cola)
        for dispositivo in self.dispositivos:
            print(f"COLA {dispositivo.nombre}\n")
            print(dispositivo.cola)

    def revisar_prioridad(self, proceso1, proceso2):
        if proceso1 == self.programa:
            proceso1_prioridad = proceso1.prioridad
        else:
            proceso1_prioridad = proceso1.dispositivo.prioridad
        
        if proceso2 == self.programa:
            proceso2_prioridad = proceso2.prioridad
        else:
            proceso2_prioridad = proceso2.dispositivo.prioridad

        if proceso1_prioridad <= proceso2_prioridad:
            return proceso1
        else:
            return proceso2

    def cambiar_prioridad(self,tiempo_actual, proceso):
        elemento_actual = proceso
        # Obterner prioridad de programa
        if elemento_actual == self.programa:
            prioridad = elemento_actual.prioridad
        else:
            prioridad = elemento_actual.dispositivo.prioridad

        # Buscar interrupciones con tiempos de inicio menores al tiempo actual y duraciones mayor a cero
        lista_dispositivos_cola = []
        for interrupcion in self.interrupciones:
            if (interrupcion.tiempo_inicio < tiempo_actual and interrupcion.duracion > 0):
                lista_dispositivos_cola.append(interrupcion)
        if tiempo_actual == 17:
            print('tiempo 17')
            print(elemento_actual.dispositivo.nombre)

        if lista_dispositivos_cola:
            # Usar el que tenga menor prioridad
            #prioridad = lista_dispositivos_cola[0].dispositivo.prioridad
            for interrupcion in lista_dispositivos_cola:
                if interrupcion.dispositivo.prioridad <= prioridad:
                    prioridad = interrupcion.dispositivo.prioridad
                    elemento_actual = interrupcion
            if tiempo_actual == 17:
                print('tiempo 17')
                print(elemento_actual.dispositivo.nombre)
            return elemento_actual

        else:
            return elemento_actual


    def buscar_tiempo(self,tiempo):
        indice = ""
        for interrupcion in self.interrupciones:
            if tiempo == interrupcion.tiempo_inicio:
                indice = self.interrupciones.index(interrupcion)
        return indice

    def interrumpir(self,tiempo,indice_interrupcion):
        return indice_interrupcion + 1

    def addBitacora(self, dispositivo,tiempo_inicial,tiempo_final):
        data = {
            'tiempo_inicio':tiempo_inicial,
            'tiempo_end': tiempo_final,
            'duracion': tiempo_final - tiempo_inicial
        }
        dispositivo.bitacora.append(data)

    def addCola(self,proceso,residuo_tiempo):
        proceso.cola.append(residuo_tiempo)


    def cambiar_proceso(self, indice_interrupcion):
        dispositive = self.interrupciones[indice_interrupcion] # Objeto dispositivo
        return dispositive


    def buscar_dispositivo(self, nombre):
        for dispositivo in self.dispositivos:
            if dispositivo.nombre == nombre:
                resultado = dispositivo
        return resultado # objeto dispositivo


    def get_interrupciones_unicas(self, interrupciones):
        # interrupciones es una lista de objetos interrupcion
        lista_dispositivos = []
        for interrupcion in interrupciones:
            data = {
                    'dispositivo':interrupcion['nombre'],
                    'prioridad': interrupcion['prioridad']
                }
            if data not in lista_dispositivos:
                lista_dispositivos.append(data)
        return lista_dispositivos

  

    def verificar_interrupcion(self,time,indice_interrupcion):
        mensaje = 'no'
        if indice_interrupcion < len(self.interrupciones):
            if time == self.interrupciones[indice_interrupcion].tiempo_inicio:
                mensaje = 'si'
        return mensaje


class Dispositivo():
    def __init__(self,nombre,prioridad):
        self.nombre = nombre
        self.prioridad = int(prioridad)
        self.cola = []
        self.bitacora = []


class Interrupcion():
    def __init__(self,dispositivo, tiempo_inicio, duracion):
        self.dispositivo = dispositivo # Objeto Dispositivo
        self.tiempo_inicio = int(tiempo_inicio)
        self.duracion = int(duracion)

    
    def addCola(self,residuo_tiempo):
        self.cola.append(residuo_tiempo)


class Programa():
    def __init__(self, tiempo_inicio, duracion, prioridad):
        self.tiempo_inicio = int(tiempo_inicio)
        self.duracion = int(duracion)
        self.prioridad = int(prioridad)
        self.cola = []
        self.bitacora = []


    def addCola(self,residuo_tiempo):
        self.cola.append(residuo_tiempo)