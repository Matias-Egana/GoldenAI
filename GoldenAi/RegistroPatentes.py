from PyQt5 import QtCore, QtGui, QtWidgets
from database import agregar_patente_permitida, eliminar_patente_permitida, initialize_database, mostrar_patentes_permitidas
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, Qt
import res_rc

class RegistroPatentes(object):
    def setupUi(self, MainWindow, usuario_id=None):
        self.usuario_id = usuario_id
        print(usuario_id)
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1098, 828)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/background/icon_goldenAi.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(39, 39, 991, 721))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(80, 40, 471, 661))
        self.label.setStyleSheet("border-image: url(:/image/background/background_register_plate.jpg);\n"
"background-color: rgba(0, 0, 0, 0.8);\n"
"border-top-left-radius: 50px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(494, 35, 431, 671))
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_2.setStyleSheet("background-color:rgba(255,255,255,255);\n"
"border-bottom-right-radius: 50px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(580, 140, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.Patente = QtWidgets.QPlainTextEdit(self.widget)
        self.Patente.setGeometry(QtCore.QRect(510, 220, 281, 31))
        self.Patente.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.Patente.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border: none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"")
        self.Patente.setObjectName("Patente")
        self.bAgregar = QtWidgets.QPushButton(self.widget)
        self.bAgregar.setGeometry(QtCore.QRect(820, 210, 40, 40))
        font = QtGui.QFont()
        self.bAgregar.setFont(font)
        self.bAgregar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bAgregar.setStyleSheet(" QPushButton {\n"
"    background-color: transparent; \n"
"     border: none;\n"
"}\n"
"QPushButton:hover {\n"
"      background-color: green;\n"
"}")
        self.bAgregar.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/image/background/lista-de-verificacion.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bAgregar.setIcon(icon1)
        self.bAgregar.setIconSize(QtCore.QSize(40, 40))
        self.bAgregar.setObjectName("bAgregar")
        self.bAgregar.clicked.connect(lambda: self.add_patente(usuario_id))
        self.bEliminar = QtWidgets.QPushButton(self.widget)
        self.bEliminar.setGeometry(QtCore.QRect(860, 210, 40, 40))
        font = QtGui.QFont()
        self.bEliminar.setFont(font)
        self.bEliminar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bEliminar.setStyleSheet(" QPushButton {\n"
"    background-color: transparent; \n"
"     border: none;\n"
"}\n"
"QPushButton:hover {\n"
"      background-color: #B22222;\n"
"}")
        self.bEliminar.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/image/background/eliminar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bEliminar.setIcon(icon2)
        self.bEliminar.setIconSize(QtCore.QSize(40, 40))
        self.bEliminar.setObjectName("bEliminar")
        self.bEliminar.clicked.connect(lambda: self.delete_patente(usuario_id))
        self.bAtras = QtWidgets.QPushButton(self.widget)
        self.bAtras.setGeometry(QtCore.QRect(510, 60, 40, 41))
        self.bAtras.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bAtras.setStyleSheet("QPushButton {\n"
"     background-color: transparent; \n"
"      border: none;\n"
" }\n"
" QPushButton:hover {\n"
"      background-color: grey;\n"
" }")
        self.bAtras.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/image/background/hacia-atras.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bAtras.setIcon(icon3)
        self.bAtras.setIconSize(QtCore.QSize(40, 40))
        self.bAtras.setObjectName("bAtras")
        self.bAtras.clicked.connect(lambda: self.openGoldenAi(MainWindow,usuario_id))
        self.bSalir = QtWidgets.QPushButton(self.widget)
        self.bSalir.setGeometry(QtCore.QRect(840, 60, 51, 51))
        self.bSalir.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bSalir.setStyleSheet("\n"
"\n"
"QPushButton {\n"
"     background-color: transparent; \n"
"      border: none;\n"
" }\n"
" QPushButton:hover {\n"
"      background-color: grey;\n"
" }")
        self.bSalir.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/image/background/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bSalir.setIcon(icon4)
        self.bSalir.setObjectName("bSalir")
        self.bSalir.clicked.connect(MainWindow.close)
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setGeometry(QtCore.QRect(510, 270, 391, 401))
        self.tableWidget.setStyleSheet("             QTableWidget {\n"
"                background-color: rgba(245, 245, 255, 255); /* Morado muy claro */\n"
"                color: black;\n"
"                gridline-color: rgba(200, 200, 200, 255);\n"
"                font-size: 14px;\n"
"            }\n"
"            QHeaderView::section {\n"
"                background-color: rgba(220, 220, 255, 255); /* Morado claro */\n"
"                color: black;\n"
"                font-weight: bold;\n"
"                border: 1px solid rgba(200, 200, 200, 255);\n"
"            }\n"
"            QTableWidget::item:selected {\n"
"                background-color: rgba(235, 235, 255, 255); /* Morado muy claro */\n"
"                color: black;\n"
"            }")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)  # Número de columnas
        self.tableWidget.setHorizontalHeaderLabels(['Patentes Permitidas'])  # Nombre de las columnas
        self.tableWidget.setRowCount(0)  # Inicialmente sin filas
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        initialize_database()
        self.start_timer()
    
    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.mostrar_patentes_table)
        self.timer.start(1000)  # Actualiza la tabla cada 1 segundo

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ingresar"))
        self.label_3.setText(_translate("MainWindow", "Register Plate"))
        self.Patente.setPlaceholderText(_translate("MainWindow", "Ingrese su patente"))

    def openGoldenAi(self, MainWindow, usuario_id):
        from GoldenAi import GoldenAi
        MainWindow.hide()
        self.goldenAiWindow = QtWidgets.QMainWindow()
        self.goldenAi = GoldenAi()
        self.goldenAi.setupUi(self.goldenAiWindow,usuario_id)
        self.goldenAiWindow.show()

    def add_patente(self, usuario_id):
        patente = self.Patente.toPlainText().strip()

        if not patente:
            self.show_error_message("Campos vacíos", "Por favor, debe rellenar todos los campos.")
            return
        
        agregar_patente_permitida(patente, usuario_id)
        self.show_confirmation_message("Agregado", "La patente ha sido agregada con éxito.")
        

    def delete_patente(self, usuario_id):
        patente = self.Patente.toPlainText().strip()

        if not patente:
            self.show_error_message("Campos vacíos", "Por favor, debe rellenar todos los campos.")
            return
        
        eliminar_patente_permitida(patente, usuario_id)
        self.show_confirmation_message("Eliminado", "La patente ha sido eliminada con éxito.")
    
    def mostrar_patentes_table(self):
        patentes = mostrar_patentes_permitidas(self.usuario_id)
        self.tableWidget.setRowCount(len(patentes))
        self.tableWidget.setColumnCount(1)  # Una columna para las patentes

        for row_num, row_data in enumerate(patentes):
            patente = row_data[2]  # Suponiendo que el número de patente está en la segunda posición
            item = QTableWidgetItem(patente)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(row_num, 0, item)


    def show_confirmation_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDefaultButton(QMessageBox.Ok)
        msg_box.exec_()

    def show_error_message(self, title, message):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = RegistroPatentes()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
