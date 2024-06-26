# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mockupRegistrar.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1098, 828)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/background/icon_goldenAi.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(39, 39, 991, 721))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(80, 40, 421, 661))
        self.label.setStyleSheet("border-image: url(:/image/background/background_register.jpg);\n"
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
        self.label_3.setGeometry(QtCore.QRect(640, 170, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.Email = QtWidgets.QPlainTextEdit(self.widget)
        self.Email.setGeometry(QtCore.QRect(570, 400, 311, 31))
        self.Email.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.Email.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border: none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"")
        self.Email.setObjectName("Email")
        self.Contra = QtWidgets.QPlainTextEdit(self.widget)
        self.Contra.setGeometry(QtCore.QRect(570, 460, 311, 31))
        self.Contra.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.Contra.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border: none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"")
        self.Contra.setObjectName("Contra")
        self.bCrear = QtWidgets.QPushButton(self.widget)
        self.bCrear.setGeometry(QtCore.QRect(610, 570, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.bCrear.setFont(font)
        self.bCrear.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bCrear.setStyleSheet("            QPushButton {\n"
"                background: qlineargradient(\n"
"                    spread:pad, x1:0, y1:0, x2:1, y2:0,\n"
"                    stop:0 #6dd5fa, stop:0.5 #8e44ad, stop:1 #bf55ec\n"
"                );\n"
"                color: white;\n"
"                border: none;\n"
"                padding: 10px 20px;\n"
"                border-radius: 10px;\n"
"                font-size: 16px;\n"
"                transition: background-color 0.3s ease; /* Transición suave */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background: qlineargradient(\n"
"                    spread:pad, x1:0, y1:0, x2:1, y2:0,\n"
"                    stop:0 #6dd5fa, stop:0.5 rgba(0, 0, 0, 0.3), stop:1 #bf55ec\n"
"                );\n"
"            }")
        self.bCrear.setObjectName("bCrear")
        self.Nombre = QtWidgets.QPlainTextEdit(self.widget)
        self.Nombre.setGeometry(QtCore.QRect(570, 280, 311, 31))
        self.Nombre.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.Nombre.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border: none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"")
        self.Nombre.setObjectName("Nombre")
        self.Apellido = QtWidgets.QPlainTextEdit(self.widget)
        self.Apellido.setGeometry(QtCore.QRect(570, 340, 311, 31))
        self.Apellido.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.Apellido.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border: none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"")
        self.Apellido.setObjectName("Apellido")
        self.bSalir = QtWidgets.QPushButton(self.widget)
        self.bSalir.setGeometry(QtCore.QRect(840, 70, 51, 51))
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
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/image/background/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bSalir.setIcon(icon1)
        self.bSalir.setObjectName("bSalir")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Registrar"))
        self.label_3.setText(_translate("MainWindow", "Register"))
        self.Email.setPlaceholderText(_translate("MainWindow", "Email"))
        self.Contra.setPlaceholderText(_translate("MainWindow", "Contraseña"))
        self.bCrear.setText(_translate("MainWindow", "Crear Usuario"))
        self.Nombre.setPlaceholderText(_translate("MainWindow", "Nombre"))
        self.Apellido.setPlaceholderText(_translate("MainWindow", "Apellido"))
import res_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
