# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DaqUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 386)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 22, 54, 20))
        self.label.setObjectName("label")
        self.comboBox_1 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_1.setGeometry(QtCore.QRect(90, 20, 69, 22))
        self.comboBox_1.setObjectName("comboBox_1")
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(20, 60, 51, 23))
        self.refreshButton.setObjectName("refreshButton")
        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        self.openButton.setGeometry(QtCore.QRect(110, 60, 61, 23))
        self.openButton.setObjectName("openButton")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(90, 100, 69, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 61, 20))
        self.label_2.setObjectName("label_2")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(30, 130, 141, 51))
        self.lcdNumber.setObjectName("lcdNumber")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(60, 212, 75, 31))
        self.startButton.setObjectName("startButton")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(60, 260, 75, 31))
        self.saveButton.setObjectName("saveButton")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(190, 10, 591, 351))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.plot_layout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.plot_layout.setContentsMargins(0, 0, 0, 0)
        self.plot_layout.setObjectName("plot_layout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "采集串口："))
        self.refreshButton.setText(_translate("MainWindow", "刷新"))
        self.openButton.setText(_translate("MainWindow", "打开串口"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "1路电流"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "2路电流"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "typc电流"))
        self.label_2.setText(_translate("MainWindow", "采集通道："))
        self.startButton.setText(_translate("MainWindow", "开始采集"))
        self.saveButton.setText(_translate("MainWindow", "图表清除"))
