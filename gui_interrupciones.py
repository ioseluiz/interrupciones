import sys

from simulacion import Simulacion

from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets import(
                            QApplication,
                            QMainWindow,
                            QPushButton,
                            QLabel,
                            QVBoxLayout,
                            QHBoxLayout,
                            QGridLayout,
                            QWidget,
                            QLineEdit,
                            QDialog,
                            QTableWidget,
                            QComboBox,
                            QGroupBox,
                            QHeaderView,
                            QTableWidgetItem,
                            QDialogButtonBox
)

class CustomDialog(QDialog):
    def __init__(self,titulo,mensaje):
        super().__init__()

        self.setWindowTitle(titulo)

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.cerrar_ventana)

        self.layout = QVBoxLayout()
        lbl_mensaje = QLabel(mensaje)
        self.layout.addWidget(lbl_mensaje)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def cerrar_ventana(self):
        self.close()

class ResultadosWindow(QWidget):
    def __init__(self,programa, dispositivos):
        super().__init__()
        self.programa = programa # Objeto Programa
        self.dispositivos = dispositivos # lista de objetos dispositivo

        # columnas = cant_dispositivos + programa
        columnas = len(dispositivos) + 1
        listado_dispositivos = ['Programa']
        for dispositivo in dispositivos:
            listado_dispositivos.append(dispositivo.nombre)

        layout = QVBoxLayout()

        self.lbl_titulo = QLabel('Bitacora de Control de Procesos')
        layout.addWidget(self.lbl_titulo)
        self.table_bitacora = QTableWidget()
        self.table_bitacora.setRowCount(0)
        self.table_bitacora.setColumnCount(columnas)
        self.table_bitacora.setHorizontalHeaderLabels(listado_dispositivos)
        layout.addWidget(self.table_bitacora)

        #Tabla para imprimir la cola de procesos pendientes
        self.lbl_cola = QLabel('Cola de Procesos Pendientes')
        layout.addWidget(self.lbl_cola)
        self.table_cola = QTableWidget()
        self.table_cola.setRowCount(0)
        self.table_cola.setColumnCount(0)
        layout.addWidget(self.table_cola)
        


        # Boton para cerrar la ventana
        self.btn_close = QPushButton("Cerrar")
        self.btn_close.clicked.connect(self.cerrar_ventana)
        layout.addWidget(self.btn_close)

        # Impresion de bitacoras en la 
        # Filas Tabla
        filas_dispositivos = self.max_elementos_bitacora()
        filas_programa = len(programa.bitacora)*2
        filas_tabla = max(filas_dispositivos, filas_programa)
        self.table_bitacora.setRowCount(filas_tabla)
        # Bitacora de Programa
        contador = 0
        for bitacora in programa.bitacora:
            self.table_bitacora.setItem(2* contador, 0, QTableWidgetItem(f"T = {bitacora['tiempo_inicio']}"))
            self.table_bitacora.setItem(2* contador + 1 , 0, QTableWidgetItem(f"T = {bitacora['tiempo_end']}  ({bitacora['duracion']} seg)"))
            contador += 1

        columna = 1
        for dispositivo in dispositivos:
            contador = 0
            for bitacora in dispositivo.bitacora:
                self.table_bitacora.setItem(2*contador,columna, QTableWidgetItem(f"T = {bitacora['tiempo_inicio']}"))
                self.table_bitacora.setItem(2*contador+1,columna,QTableWidgetItem(f"T = {bitacora['tiempo_end']}  ({bitacora['duracion']} seg)"))
                contador += 1
            columna += 1

        # Impresion de colas en la tabla
        # Contabilizar los dispositivos con valores en la cola de pendientes
        # filas
        filas = len(dispositivos) + 1 # dispositivos + programa
        self.table_cola.setRowCount(filas)
        columnas = len(programa.cola) + 1
        self.table_cola.setColumnCount(columnas)
        self.table_cola.setItem(0,0,QTableWidgetItem('Programa'))
        contador = 1
        for elemento in programa.cola:
            if elemento != 0:
                self.table_cola.setItem(0, contador, QTableWidgetItem(f"{elemento}"))
                contador += 1
        # Listar los dispositivos en su fila
        counter = 1
        for dispositivo in dispositivos:
            self.table_cola.setItem(counter,0, QTableWidgetItem(f"{dispositivo.nombre}"))
            # Listar los valores en cola de cada dispositivo
            counter_cola = 1
            for elemento in dispositivo.cola:
                if elemento !=  0:
                    self.table_cola.setItem(counter,counter_cola, QTableWidgetItem(f"{elemento}"))
                    counter_cola += 1
            counter += 1


        width = 600
        height = 640

        self.setFixedWidth(width)
        self.setFixedHeight(height)

        self.setLayout(layout)

    def max_elementos_bitacora(self):
        maximo = 0
        for dispositivo in self.dispositivos:
            cantidad = len(dispositivo.cola)*2
            if maximo <= cantidad:
                maximo = cantidad
        return maximo

    def cerrar_ventana(self):
        self.close()


        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.w = None # No hay ventana secundaria de resultados 
        self.q = None

        self.dispositivos = [
            {
                'dispositivo':'Reloj Sistema',
                'prioridad':1
            },
            {
                'dispositivo': 'Teclado',
                'prioridad': 2
            },
            
            {
                'dispositivo':'Reloj CMOS',
                'prioridad': 3
            },
            {
                'dispositivo':'Sonido',
                'prioridad': 4
            },
            {
                'dispositivo':'Red',
                'prioridad': 4
            },
            {
                'dispositivo':'Puerto SCSI',
                'prioridad': 4
            },
            {
                'dispositivo': 'PS-Mouse',
                'prioridad':7
            },
            {
                'dispositivo': 'Co-procesador Matematico',
                'prioridad':8
            },
            {
                'dispositivo':'Canal IDE Primario',
                'prioridad':9
            },
            {
                'dispositivo':'Disco',
                'prioridad':9
            },
            {
                'dispositivo':'COM 1',
                'prioridad':12,
            },
            {
                'dispositivo': 'COM 2',
                'prioridad': 11
            },
            {
                'dispositivo': 'COM 3',
                'prioridad': 12
            },
            {
                'dispositivo': 'COM 4',
                'prioridad': 11
            },
            {
                'dispositivo': 'Diskette',
                'prioridad': 14
            },
            {
                'dispositivo':'Impresora',
                'prioridad':15
            }
        ]

        lista_dispositivos = self.get_lista_dispositivos()
        print(lista_dispositivos)

        layout = QGridLayout()
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()
        layout_titulo = QVBoxLayout()
        layout_opciones = QGroupBox('Opciones')
        grid_layout = QGridLayout()
        layout_opciones.setLayout(grid_layout)
        layout_opciones.setFixedSize(QSize(340,100))
        layout_peticiones = QGroupBox('Peticiones')
        peticiones_grid = QGridLayout()
        layout_peticiones.setLayout(peticiones_grid)
        layout_peticiones.setFixedSize(QSize(340,180))
        layout_iniciar = QGridLayout()
        #layout_left.setSpacing(20)
        #layout_left.setFixedSize(QSize(200,20))
        #layout_right.setFixedSize(QSize(200,20))
        layout_simulacion = QGroupBox('Simulacion')
        simulacion_grid = QGridLayout()
        layout_simulacion.setLayout(simulacion_grid)


        lbl_titulo = QLabel('Interrupciones')
        lbl_titulo.setFixedSize(QSize(100,20))
        layout_titulo.addWidget(lbl_titulo)
        lbl_logo = QLabel('Hola')
        lbl_logo.setPixmap(QPixmap("microchip.png"))
        lbl_logo.setScaledContents(True)
        lbl_logo.setFixedSize(QSize(60,60))
        layout_titulo.addWidget(lbl_logo)
        


        
        lbl_duracion = QLabel('Duracion del Programa ')
        grid_layout.addWidget(lbl_duracion,0, 0)
        self.txt_duracion_programa = QLineEdit()
        self.txt_duracion_programa.setValidator(QIntValidator())
        grid_layout.addWidget(self.txt_duracion_programa, 0, 1)
        lbl_tiempo_inicio = QLabel('Tiempo de Inicio ')
        grid_layout.addWidget(lbl_tiempo_inicio, 1, 0)
        self.txt_tiempo_inicio = QLineEdit()
        self.txt_tiempo_inicio.setValidator(QIntValidator())
        grid_layout.addWidget(self.txt_tiempo_inicio,1,1)

        lbl_tiempo = QLabel('Tiempo ')
        peticiones_grid.addWidget(lbl_tiempo, 0, 0)
        self.txt_tiempo = QLineEdit()
        self.txt_tiempo.setValidator(QIntValidator())
        peticiones_grid.addWidget(self.txt_tiempo,1, 0)
        lbl_peticion = QLabel('Peticion')
        peticiones_grid.addWidget(lbl_peticion, 0, 1)
        self.cbo_peticion = QComboBox()
        self.cbo_peticion.addItems(lista_dispositivos)
        peticiones_grid.addWidget(self.cbo_peticion,1, 1)
        lbl_duracion = QLabel('Duracion')
        peticiones_grid.addWidget(lbl_duracion, 0, 2)
        self.txt_duracion = QLineEdit()
        self.txt_duracion.setValidator(QIntValidator())
        peticiones_grid.addWidget(self.txt_duracion, 1, 2)
        self.btn_eliminar_peticion = QPushButton("Eliminar\n Peticion\n Seleccionada")
        self.btn_eliminar_peticion.clicked.connect(self.eliminar_fila_seleccionada)
        peticiones_grid.addWidget(self.btn_eliminar_peticion, 2, 2)
        self.btn_eliminar_peticion.setFixedSize(QSize(110,60))
        self.btn_agregar_peticion = QPushButton("Agregar\n Peticion")
        peticiones_grid.addWidget(self.btn_agregar_peticion, 2, 0)
        self.btn_agregar_peticion.setFixedSize(QSize(110,60))

        self.btn_agregar_peticion.clicked.connect(self.agregar_peticion)
        self.table_interrupciones = QTableWidget()
        self.table_interrupciones.setRowCount(0)
        self.table_interrupciones.setColumnCount(4)
        self.table_interrupciones.setHorizontalHeaderLabels(['T', 'Peticiones', 'Duraciones','Prioridad'])
        self.table_interrupciones.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_interrupciones.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        layout_right.addWidget(self.table_interrupciones)

        self.btn_reiniciar = QPushButton('Reiniciar\n Programa')
        self.btn_reiniciar.clicked.connect(self.reiniciar_programa)
        simulacion_grid.addWidget(self.btn_reiniciar, 0, 0)
        self.btn_ejecutar = QPushButton('Ejecutar\n Simulacion')
        self.btn_ejecutar.clicked.connect(self.ejecutar_simulacion)
        simulacion_grid.addWidget(self.btn_ejecutar, 0, 2)
        layout_left.addLayout(layout_titulo)
        layout_left.addWidget(layout_opciones)
        layout_left.addWidget(layout_peticiones)
        layout_left.addWidget(layout_simulacion)
        layout.addLayout(layout_left, 0, 0)
        layout.addLayout(layout_right, 0 ,1)
    

        width = 700
        height = 540

        self.setFixedWidth(width)
        self.setFixedHeight(height)

        self.setWindowIcon(QtGui.QIcon('chip.ico'))
        self.setWindowTitle('Programa de Interrupciones')

                   
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def agregar_peticion(self):

        # Validacion de datos
        blanco = self.validacion_blank(self.txt_tiempo.text())
        if blanco == 'si':
            return

        blanco = self.validacion_blank(self.txt_duracion.text())
        if blanco == 'si':
            return


        numerico = self.validacion_numeric(self.txt_tiempo.text())
        if numerico == 'si':
            return
        
        numerico = self.validacion_numeric(self.txt_duracion.text())
        if numerico == 'si':
            return
        
        # Lectura de Datos
        tiempo = self.txt_tiempo.text()
        peticion = self.cbo_peticion.currentText()
        duracion = self.txt_duracion.text()
            
        #Agregar en tabla la informacion
         # Imprimir resultados en Table
        filas = (self.table_interrupciones.rowCount() + 1)
        print(filas)
        self.table_interrupciones.setRowCount(filas)
        self.table_interrupciones.setItem(filas-1, 0, QTableWidgetItem(tiempo))
        self.table_interrupciones.setItem(filas-1, 1, QTableWidgetItem(peticion))
        self.table_interrupciones.setItem(filas-1, 2, QTableWidgetItem(duracion))
        prioridad = self.get_prioridad(peticion)
        print(prioridad)
        self.table_interrupciones.setItem(filas-1, 3, QTableWidgetItem(str(prioridad)))

        self.limpiar_textos()

    def show_dialog_error(self,titulo, mensaje):
        dlg = CustomDialog(titulo, mensaje)
        return dlg

    def validacion_blank(self,texto):
        if (texto == ""):
            if self.q is None:
                self.q = self.show_dialog_error('Error de Validación','No se puede dejar el campo sin llenar')
                self.q.show()
            else:
                self.q.close()
                self.q = None # Discard reference, close window
            return "si"
        return "no"

    def validacion_numeric(self,texto):
        if (texto.isdecimal() is False):
            if self.q is None:
                self.q = self.show_dialog_error('Error de Validación','Solamente se admiten numeros')
                self.q.show()
            else:
                self.q.close()
                self.q = None # Discard reference, close window
            return

        


    def get_lista_dispositivos(self):
        lista = []
        for dispositivo in self.dispositivos:
            lista.append(dispositivo['dispositivo'])
        return lista

    def get_prioridad(self, _dispositivo):
        _prioridad = 0
        for dispositivo in self.dispositivos:
            if dispositivo['dispositivo'] == _dispositivo:
                _prioridad = dispositivo['prioridad']
                return _prioridad
        return _prioridad

    def leer_tabla(self):
        # cantidad de dispositivos
        filas = self.table_interrupciones.rowCount()
        print(f'Existen {filas} en la tabla')
        # Lectura de elementos en la tabla
        datos_tabla = []
        for fila in range(filas):
            dispositivo = {
                'tiempo_inicio': self.table_interrupciones.item(fila,0).text(),
                'nombre': self.table_interrupciones.item(fila,1).text(),
                'duracion': self.table_interrupciones.item(fila,2).text(),
                'prioridad': self.table_interrupciones.item(fila,3).text()
                }
            datos_tabla.append(dispositivo)

        return datos_tabla

    def ejecutar_simulacion(self):
        self.w = None # No hay ventana secundaria de resultados todavia
        # Lectura de datos ingresados
        duracion_programa = self.txt_duracion_programa.text()
        tiempo_inicio_programa = self.txt_tiempo_inicio.text()

        datos = {
            'duracion_programa': duracion_programa,
            'tiempo_inicio_programa': tiempo_inicio_programa
        }
        datos_tabla = self.leer_tabla()
        simulacion = Simulacion(datos, datos_tabla)

        if self.w is None:
            self.w = ResultadosWindow(simulacion.programa,simulacion.dispositivos)
            self.w.show()

        else:
            self.w.close()
            self.w = None # Discard reference, close window

    def limpiar_textos(self):
        self.txt_duracion.setText("")
        self.txt_tiempo.setText("")

    def reiniciar_programa(self):
        #limpiar datos de entrada
        self.txt_duracion_programa.setText("")
        self.txt_duracion.setText("")
        self.txt_tiempo.setText("")
        self.txt_tiempo_inicio.setText("")

        # Limpieza de la tabla_interrupciones
        self.table_interrupciones.setRowCount(0)

    def eliminar_fila_seleccionada(self):
        self.table_interrupciones.removeRow(self.table_interrupciones.currentRow())
        





def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()

if __name__ == '__main__':
    main()