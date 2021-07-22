import sys

from simulacion import Simulacion

from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
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
                            QTableWidgetItem
)

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


        width = 500
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


        


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.w = None # No hay ventana secundaria de resultados todavia

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
        grid_layout.addWidget(self.txt_duracion_programa, 0, 1)
        lbl_tiempo_inicio = QLabel('Tiempo de Inicio ')
        grid_layout.addWidget(lbl_tiempo_inicio, 1, 0)
        self.txt_tiempo_inicio = QLineEdit()
        grid_layout.addWidget(self.txt_tiempo_inicio,1,1)

        lbl_tiempo = QLabel('Tiempo ')
        peticiones_grid.addWidget(lbl_tiempo, 0, 0)
        self.txt_tiempo = QLineEdit()
        peticiones_grid.addWidget(self.txt_tiempo,1, 0)
        lbl_peticion = QLabel('Peticion')
        peticiones_grid.addWidget(lbl_peticion, 0, 1)
        self.cbo_peticion = QComboBox()
        self.cbo_peticion.addItems(lista_dispositivos)
        peticiones_grid.addWidget(self.cbo_peticion,1, 1)
        lbl_duracion = QLabel('Duracion')
        peticiones_grid.addWidget(lbl_duracion, 0, 2)
        self.txt_duracion = QLineEdit()
        peticiones_grid.addWidget(self.txt_duracion, 1, 2)
        self.btn_eliminar_peticion = QPushButton("Eliminar\n Peticion\n Seleccionada")
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
        # Lectura de Datos
        tiempo = self.txt_tiempo.text()
        print(tiempo)
        peticion = self.cbo_peticion.currentText()
        print(peticion)
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



def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()

if __name__ == '__main__':
    main()