# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_chart.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os
import shutil
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from typing_1 import critical_path_both2, find_longest_path, critical_path_both, visualize_aoa2
import sys

class Ui_MainWindow(object):
    def __init__(self):
        self.starting=None
        self.late_first_pixmap = None
        self.critical_late_first_pixmap = None
        self.critical_pixmap=None
        self.Nun_pixmap=None
        self.spreadsheet=None

    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def save(self):
        pixmap = self.label_5.pixmap()
        if pixmap:
            options = QtWidgets.QFileDialog.Options()
            save_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, 
                                                                 "Save Image", 
                                                                 "", 
                                                                 "PNG Files (*.png);;All Files (*)", 
                                                                 options=options)
            if not save_path:
                return
            
            if not save_path.endswith('.png'):
                save_path += '.png'
            pixmap.save(save_path, 'PNG')

    def export(self):
      pixmap = self.label_5.pixmap()
      if pixmap:
        # Set the options for the file dialog
        options = QtWidgets.QFileDialog.Options()
        
        # Get the save path from the file dialog
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, 
                                                             "Save Image", 
                                                             "", 
                                                             "PNG Files (*.png);;All Files (*)", 
                                                             options=options)
        if not save_path:
            # User canceled the dialog
            return
        
        # Ensure the save path ends with '.png'
        if not save_path.endswith('.png'):
            save_path += '.png'
        
        # Create the 'aa' directory if it does not exist
        base_name = os.path.splitext(os.path.basename(save_path))[0]
        
        # Create the directory with the same name as the base name
        directory_path = os.path.join(os.path.dirname(save_path), base_name)
        os.makedirs(directory_path, exist_ok=True)
        
        # Construct the full save path within the 'aa' directory
        base_name = os.path.basename(save_path)
        save_path_in_directory = os.path.join(directory_path, os.path.basename(save_path))
        
        # Save the pixmap to the specified path
        pixmap.save(save_path_in_directory, 'PNG')
        folder_name = "Downloads/application"
        folder_path = os.path.expanduser(f"~/{folder_name}")
        
        # List all files in the folder and find the newest Excel file
        newest_file = None
        newest_time = None
        for filename in os.listdir(folder_path):
            if filename.endswith('.xlsx'):
                file_path = os.path.join(folder_path, filename)
                file_time = os.path.getmtime(file_path)
                if newest_time is None or file_time > newest_time:
                    newest_time = file_time
                    newest_file = file_path
        
        if newest_file:
            # Copy the newest Excel file to the newly created directory
            shutil.copy(newest_file, directory_path)

    def check_checkboxes(self):
        if self.critical.isChecked() and self.late_first.isChecked():
            self.both_checkbox()
        if self.critical.isChecked()==False and self.late_first.isChecked():
            self.check2()
        if self.critical.isChecked() and self.late_first.isChecked()==False:
            self.check1()
        if self.critical.isChecked()==False and self.late_first.isChecked()==False:
            self.nun()

    def both_checkbox(self):
        if self.critical_pixmap:
            self.label_5.setPixmap(self.critical_pixmap)
        else:
            # self.late_first_pixmap = self.label_5.pixmap().copy()
            longest_path,longest_duration= find_longest_path(self.starting)
            dot = critical_path_both(self.starting, longest_path)
            png_data = dot.pipe(format='png')
            pixmap = QPixmap()
            pixmap.loadFromData(png_data)
            self.label_5.setPixmap(pixmap)
            self.critical_pixmap= self.label_5.pixmap().copy()
            # Restore the previous pixmap
            # if self.late_first_pixmap:
            #     self.label_5.setPixmap(self.late_first_pixmap)

    def check2(self):
        if self.Nun_pixmap:
            self.label_5.setPixmap(self.Nun_pixmap)
        else:
            if self.late_first_pixmap is None:
                self.late_first_pixmap = self.label_5.pixmap().copy()
            dot = visualize_aoa2(self.starting)
            png_data = dot.pipe(format='png')
            pixmap = QPixmap()
            pixmap.loadFromData(png_data)
            self.label_5.setPixmap(pixmap)
            self.Nun_pixmap= self.label_5.pixmap().copy()

    def check1(self):
        if self.critical_late_first_pixmap:
            self.label_5.setPixmap(self.critical_late_first_pixmap)
        else:
            if self.late_first_pixmap is None:
                self.late_first_pixmap = self.label_5.pixmap().copy()
            longest_path,longest_duration= find_longest_path(self.starting)
            dot = critical_path_both2(self.starting, longest_path)
            png_data = dot.pipe(format='png')
            pixmap = QPixmap()
            pixmap.loadFromData(png_data)
            self.label_5.setPixmap(pixmap)
            self.critical_late_first_pixmap= self.label_5.pixmap().copy()

    def nun(self):
        self.label_5.setPixmap(self.late_first_pixmap)

    def backing(self):
        self.spreadsheet.show()
        self.spreadsheet.showMaximized()
        # QtWidgets.QApplication.instance().activeWindow().close()
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)  # Informative icon
        msg.setText("If you make changes in the sheet, you will again have to give start date in calender to implement the changes")
        msg.setWindowTitle("Information Box")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
        self.main_window.close()

    def setupUi(self, MainWindow):
        self.main_window = MainWindow
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(screen_width, screen_height)
        MainWindow.setStyleSheet("background-color: rgb(85, 255, 255);")

        ## central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.centralwidget.setLayout(self.verticalLayout)

        ## top menu
        self.top=QtWidgets.QWidget(self.centralwidget)
        self.verticalLayout.addWidget(self.top)
        self.toplayout=QtWidgets.QHBoxLayout(self.top)
        self.top.setLayout(self.toplayout)

        self.back = QtWidgets.QPushButton(self.top)
        self.back.setGeometry(QtCore.QRect(0, 0, 21, 21))
        self.back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.resource_path("Spreadsheet_images/logout.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back.setIcon(icon)
        self.back.setObjectName("back")
        self.back.clicked.connect(self.backing)

        # self.Save = QtWidgets.QPushButton(self.top)
        # self.Save.setGeometry(QtCore.QRect(30, 0, 21, 21))
        # self.Save.setText("")
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(self.resource_path("Spreadsheet_images/diskette.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.Save.setIcon(icon)
        # self.Save.setObjectName("Save")

        ## Upper menus
        self.menu = QtWidgets.QWidget(self.centralwidget)
        self.menu.setStyleSheet("background-color: rgb(79, 207, 207);")
        self.verticalLayout.addWidget(self.menu)
        self.menuvertical=QtWidgets.QVBoxLayout(self.menu)
        self.menu.setLayout(self.menuvertical)

        ## menu1
        self.menu1=QtWidgets.QWidget(self.menu)
        self.menuvertical.addWidget(self.menu1)
        self.menu1horizontal=QtWidgets.QHBoxLayout(self.menu1)
        self.menu1.setLayout(self.menu1horizontal)

        self.menu11=QtWidgets.QWidget(self.menu1)
        self.menu1horizontal.addWidget(self.menu11)
        self.critical = QtWidgets.QCheckBox(self.menu11)
        self.critical.setStyleSheet("background-color: rgb(154, 147, 147);")
        self.critical.setObjectName("checkBox_6")
        self.critical.stateChanged.connect(self.check_checkboxes)
        self.menu11vertical = QtWidgets.QVBoxLayout(self.menu11)
        self.menu11.setLayout(self.menu11vertical)
        self.menu11vertical.addWidget(self.critical)

        self.menu12=QtWidgets.QWidget(self.menu1)
        self.menu1horizontal.addWidget(self.menu12)

        self.menu13=QtWidgets.QWidget(self.menu1)
        self.menu1horizontal.addWidget(self.menu13)
        self.save_button = QtWidgets.QPushButton(self.menu13)
        self.save_button.setStyleSheet("background-color: rgb(154, 147, 147);")
        # self.pushButton_5.clicked.connect(self.save)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/images/icons8-save-16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_button.setIcon(icon1)
        self.save_button.setObjectName("pushButton_5")
        self.save_button.clicked.connect(self.save)
        self.menu13vertical = QtWidgets.QVBoxLayout(self.menu13)
        self.menu13.setLayout(self.menu13vertical)
        self.menu13vertical.addWidget(self.save_button)

        ## menu2
        self.menu2=QtWidgets.QWidget(self.menu)
        self.menuvertical.addWidget(self.menu2)
        # self.menu.resize(QtCore.QSize(int(self.centralwidget.size().width()), int(self.centralwidget.size().width() * 0.2)))
        self.menu2horizontal=QtWidgets.QHBoxLayout(self.menu2)
        self.menu2.setLayout(self.menu2horizontal)
        self.menu21=QtWidgets.QWidget(self.menu2)
        self.menu2horizontal.addWidget(self.menu21)
        self.late_first = QtWidgets.QCheckBox(self.menu21)
        self.late_first.setStyleSheet("background-color: rgb(154, 147, 147);")
        self.late_first.setObjectName("pushButton_2")
        self.late_first.stateChanged.connect(self.check_checkboxes)
        self.menu21vertical = QtWidgets.QVBoxLayout(self.menu21)
        self.menu21.setLayout(self.menu21vertical)
        self.menu21vertical.addWidget(self.late_first)

        self.menu22=QtWidgets.QWidget(self.menu2)
        self.menu2horizontal.addWidget(self.menu22)

        self.menu23=QtWidgets.QWidget(self.menu2)
        self.menu2horizontal.addWidget(self.menu23)
        self.export_button = QtWidgets.QPushButton(self.menu23)
        self.export_button.setStyleSheet("background-color: rgb(154, 147, 147);")
        # self.export_button.clicked.connect(self.export)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/images/icons8-export-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.export_button.setIcon(icon)
        self.export_button.setObjectName("pushButton_4")
        self.export_button.clicked.connect(self.export)
        self.menu23vertical = QtWidgets.QVBoxLayout(self.menu23)
        self.menu23.setLayout(self.menu23vertical)
        self.menu23vertical.addWidget(self.export_button)

        ## lower network
        self.network = QtWidgets.QWidget(self.centralwidget)
        self.network.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.network.setObjectName("widget_2")
        self.verticalLayout.addWidget(self.network)

        self.verticalLayout.setStretchFactor(self.top, 2)
        self.verticalLayout.setStretchFactor(self.menu, 25)
        self.verticalLayout.setStretchFactor(self.network, 100)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.network)
        self.network.setLayout(self.horizontalLayout)

        self.written = QtWidgets.QWidget(self.network)
        self.written.setStyleSheet("background-color: rgb(79, 207, 207);")
        self.written.setObjectName("widget_3")
        self.writtenhorizontal=QtWidgets.QVBoxLayout(self.written)
        self.written.setLayout(self.writtenhorizontal)
        self.horizontalLayout.addWidget(self.written)

        self.diagram = QtWidgets.QWidget(self.network)
        self.diagram.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.diagram.setObjectName("widget_2")
        self.horizontalLayout.addWidget(self.diagram)
        self.diagramhorizontal=QtWidgets.QHBoxLayout(self.diagram)
        self.diagram.setLayout(self.diagramhorizontal)

        self.label_5 = QtWidgets.QLabel(self.diagram)
        # self.label_5.setGeometry(QtCore.QRect(0, 100, 751, 371))
        self.label_5.setText("")
        self.label_5.setStyleSheet("background-color: white")
        self.label_5.setObjectName("label_5")
        self.diagramhorizontal.addWidget(self.label_5)

        self.scrollArea = QtWidgets.QScrollArea(self.diagram)
        # self.scrollArea.setGeometry(QtCore.QRect(21, 155, 751, 416))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setWidget(self.label_5)
        self.diagramhorizontal.addWidget(self.scrollArea)

        self.verticalScrollBar = QtWidgets.QScrollBar(self.diagram)
        # self.verticalScrollBar.setGeometry(QtCore.QRect(770, 10, 20, 411))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.scrollArea.setVerticalScrollBar(self.verticalScrollBar)
        
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.diagram)
        # self.horizontalScrollBar.setGeometry(QtCore.QRect(10, 430, 751, 20))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.scrollArea.setHorizontalScrollBar(self.horizontalScrollBar)

        self.verticalScrollBar.valueChanged.connect(self.scroll_vertically)
        self.horizontalScrollBar.valueChanged.connect(self.scroll_horizontally)

        self.horizontalLayout.setStretchFactor(self.written, 1)
        self.horizontalLayout.setStretchFactor(self.diagram,100)
        self.N = QtWidgets.QLabel(self.written)
        # self.N.setGeometry(QtCore.QRect(0, 50, 20, 21))
        self.N.setStyleSheet("background-color: rgb(79, 207, 207);")
        self.N.setObjectName("label")
        self.writtenhorizontal.addWidget(self.N)
        self.E = QtWidgets.QLabel(self.written)
        # self.E.setGeometry(QtCore.QRect(0, 70, 20, 21))
        self.E.setStyleSheet("background-color: rgb(79, 207, 207);")
        self.E.setObjectName("label_2")
        self.writtenhorizontal.addWidget(self.E)
        self.T = QtWidgets.QLabel(self.written)
        # self.T.setGeometry(QtCore.QRect(0, 90, 20, 21))
        self.T.setStyleSheet("background-color: rgb(79, 207, 207);")
        self.T.setObjectName("label_3")
        self.writtenhorizontal.addWidget(self.T)
        self.W = QtWidgets.QLabel(self.written)
        # self.W.setGeometry(QtCore.QRect(0, 110, 20, 21))
        self.W.setStyleSheet("background-color: rgb(79, 207, 207);")
        self.W.setObjectName("label_4")
        self.writtenhorizontal.addWidget(self.W)
        self.O = QtWidgets.QLabel(self.written)
        # self.O.setGeometry(QtCore.QRect(0, 130, 20, 21))
        self.O.setStyleSheet("background-color: rgb(79, 207, 207);")
        self.O.setObjectName("label_10")
        self.writtenhorizontal.addWidget(self.O)
        self.R = QtWidgets.QLabel(self.written)
        # self.R.setGeometry(QtCore.QRect(0, 150, 20, 21))
        self.R.setStyleSheet("background-color: rgb(79, 207, 207);")
        self.R.setObjectName("label_9")
        self.writtenhorizontal.addWidget(self.R)
        self.K = QtWidgets.QLabel(self.written)
        # self.K.setGeometry(QtCore.QRect(0, 170, 20, 21))
        self.K.setStyleSheet("background-color: rgb(79, 207, 207);")
        self.K.setObjectName("label_8")
        self.writtenhorizontal.addWidget(self.K)
        self.D = QtWidgets.QLabel(self.written)
        # self.D.setGeometry(QtCore.QRect(0, 220, 20, 21))
        self.D.setStyleSheet("background-color: rgb(79, 207, 207);")
        self.D.setObjectName("label_11")
        self.writtenhorizontal.addWidget(self.D)
        self.I = QtWidgets.QLabel(self.written)
        # self.I.setGeometry(QtCore.QRect(0, 300, 20, 21))
        self.I.setStyleSheet("background-color: rgb(79, 207, 207);")
        self.I.setObjectName("label_12")
        self.writtenhorizontal.addWidget(self.I)
        self.A1 = QtWidgets.QLabel(self.written)
        # self.A1.setGeometry(QtCore.QRect(0, 320, 20, 21))
        self.A1.setStyleSheet("background-color: rgb(79, 207, 207);")
        self.A1.setObjectName("label_13")
        self.writtenhorizontal.addWidget(self.A1)
        self.G = QtWidgets.QLabel(self.written)
        # self.G.setGeometry(QtCore.QRect(0, 280, 20, 21))
        self.G.setStyleSheet("background-color: rgb(79, 207, 207);")
        self.G.setObjectName("label_14")
        self.writtenhorizontal.addWidget(self.G)
        self.R2 = QtWidgets.QLabel(self.written)
        # self.R.setGeometry(QtCore.QRect(0, 340, 20, 21))
        self.R2.setStyleSheet("background-color: rgb(79, 207, 207);")
        self.R2.setObjectName("label_15")
        self.writtenhorizontal.addWidget(self.R2)
        self.A2 = QtWidgets.QLabel(self.written)
        # self.A2.setGeometry(QtCore.QRect(0, 260, 20, 21))
        self.A2.setStyleSheet("background-color: rgb(79, 207, 207);")
        self.A2.setObjectName("label_16")
        self.writtenhorizontal.addWidget(self.A2)
        self.M = QtWidgets.QLabel(self.written)
        # self.M.setGeometry(QtCore.QRect(0, 240, 20, 21))
        self.M.setStyleSheet("background-color: rgb(79, 207, 207);")
        self.M.setObjectName("label_17")
        self.writtenhorizontal.addWidget(self.M)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def scroll_vertically(self, value):
        self.scrollArea.verticalScrollBar().setValue(value)

    def scroll_horizontally(self, value):
        self.scrollArea.horizontalScrollBar().setValue(value)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chart Window"))
        self.late_first.setText(_translate("MainWindow", "Hide E/S, E/F, L/S, L/F"))
        self.export_button.setText(_translate("MainWindow", "EXPORT"))
        self.save_button.setText(_translate("MainWindow", " SAVE"))
        self.critical.setText(_translate("MainWindow", "Show Critical Path"))
        self.N.setText(_translate("MainWindow", " N "))
        self.E.setText(_translate("MainWindow", " E "))
        self.T.setText(_translate("MainWindow", " T"))
        self.W.setText(_translate("MainWindow", " W"))
        self.O.setText(_translate("MainWindow", " O"))
        self.R.setText(_translate("MainWindow", " R"))
        self.K.setText(_translate("MainWindow", " K"))
        self.D.setText(_translate("MainWindow", " D"))
        self.R2.setText(_translate("MainWindow", " R"))
        self.A1.setText(_translate("MainWindow", " A"))
        self.G.setText(_translate("MainWindow", " G"))
        self.M.setText(_translate("MainWindow", " M"))
        self.A2.setText(_translate("MainWindow", " A"))
        self.I.setText(_translate("MainWindow", " I"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    MainWindow.showMaximized()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())