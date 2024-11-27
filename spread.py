import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtWidgets import QMessageBox
from collections import deque
from chart import Ui_MainWindow
from typing_1 import Activity,NodeState,ArrowTask,DashedArrow, find_longest_path, get_aoa_data_structure, visualize_aoa
import os,sys
from calender import CalendarApp
from collections import deque
from PyQt5.QtCore import QDate

class Ui_Spreadsheet(object):
    def __init__(self):
        self.data_list = []
        self.starting=None
        self.selected_dates=None
        self.dict_emerging=None
        self.dict_terminating=None

    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    
    def populate_table(self, data):
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(6)
        
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(cell_data)))

    def save_to_excel(self):
        import os
        import openpyxl
        # Specify the file path
        folder_name = "Downloads/application"
        name = self.label.text()
        folder_path = os.path.expanduser(f"~/{folder_name}")
        file_path = os.path.join(folder_path, f"{name}.xlsx")
        # Check if the folder exists, if not, create it
        if not os.path.exists(folder_path):
           os.makedirs(folder_path)

        # Collect data from the table widget
        data = self.collect_data()
        if data is None:
            return

        # Create a new Excel workbook and add a worksheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Spreadsheet Data"

        # Define the header
        header = ["Task ID", "Task Name","Duration", "Predecessors"]
        sheet.append(header)

        # Append the data rows
        for activity in data:
           new_pred=[]
           for i in activity.predecessors_indices:
               new_pred.append(i+1)

           row = [activity.id,activity.name, activity.duration, ','.join(map(str, new_pred))]
           sheet.append(row)

        # Save the workbook
        workbook.save(file_path)
        # Save the workbook
        workbook.save(file_path)
        return 1

    def warnings(self,message,title):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)  # Informative icon
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
        return 

    def collect_data(self):
        self.data_list.clear()  # Clear the existing data list
        for row in range(self.tableWidget.rowCount()):
            row_data = []
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, column)
                if item and item.text():
                    row_data.append(item.text())
                else:
                    row_data.append('')  # If the cell is empty, append an empty string
            if any(row_data):  # Only add the row if it has any data
                # self.table_create.append(row_data)
                number_list = row_data[3].split(",")
                int_list = []
                if row_data[3]!='':
                    for number in number_list:
                        try:
                            int_list.append(int(number)-1)
                            if int(number)<=0:
                                return self.warnings("Please enter proper datatypes: Task ID: 'Integer', Task Name: 'String', Duration: 'Integer', Predecessor: 'Integer' List of Task's row number starting from 1.","Wrong data type")
                        except:
                            return self.warnings("Please enter proper datatypes: Task ID: 'Integer', Task Name: 'String', Duration: 'Integer', Predecessor: 'Integer' List of Task's row number starting from 1.","Wrong data type")
                for i in range(3):
                    if row_data[i]=='':
                        # print("LL")
                        return self.warnings("Please enter essential details","Incomplete Information")
                # print(type(row_data[0]),"KK",row_data[0])
                try:
                    row_data[0]=int(row_data[0])
                except:
                    return self.warnings("Please enter proper datatypes: Task ID: 'Integer', Task Name: 'String', Duration: 'Integer', Predecessor: 'Integer' List of Task's row number starting from 1.","Wrong data type")
                try:
                    row_data[2]=int(row_data[2])
                except:
                    return self.warnings("Please enter proper datatypes: Task ID: 'Integer', Task Name: 'String', Duration: 'Integer', Predecessor: 'Integer' List of Task's row number starting from 1.","Wrong data type")
                try:
                    row_data[1]=int(row_data[1])
                    return self.warnings("Please enter proper datatypes: Task ID: 'Integer', Task Name: 'String', Duration: 'Integer', Predecessor: 'Integer' List of Task's row number starting from 1.","Wrong data type")
                except:
                    pass
                self.data_list.append(Activity(row_data[0],row_data[1],row_data[2],int_list))
            else:
                break
        if len(self.data_list)==0:
            return self.warnings("Please enter essential details","Incomplete Information")
        return self.data_list
    
    def open_calendar_app(self):
        # Ask for starting date from user
        start_date, ok = QtWidgets.QInputDialog.getText(self.centralwidget, 'Input Dialog', 'Enter start date (YYYY-MM-DD):')
        if ok and start_date:
            start_date = QDate.fromString(start_date, "yyyy-MM-dd")
            if start_date.isValid():
                # Create the calendar window
                pp=self.save_to_excel()
                if pp is None:
                    return
                
                self.starting,self.dict_emerging,self.dict_terminating = get_aoa_data_structure(self.data_list)
                longest_path,longest_duration= find_longest_path(self.starting)
                self.calendar_window = CalendarApp()
                self.calendar_window.show()
                # Example: Select dates from the provided start date for the next 10 days, skipping weekends
                # self.longest_duration=longest_duration
                # duration = 10
                self.calendar_window.select_dates_from(start_date,longest_duration)
                self.selected_dates=self.calendar_window.selected_dates
            else:
                return self.warnings("Please enter the date in YYYY-MM-DD format.","Invalid date format")

    def early_late(self,start_node: NodeState, dates):
        q=deque()
        q.append(start_node)
        last=None
        while(len(q)!=0):
            size=len(q)
            while(size!=0):
                rem=q.popleft()
                last=rem
                if(rem==start_node):
                    for arrow in rem.emerging_arrows:
                        arrow.early_start=dates[0]
                        arrow.early_finish=dates[arrow.duration-1]
                        self.dict_terminating[arrow.destination_node]=self.dict_terminating[arrow.destination_node]-1
                        if self.dict_terminating[arrow.destination_node]==0:
                            q.append(arrow.destination_node)
                else:
                    max=-1
                    temp_arrow=None
                    for arrow in rem.terminating_arrows:
                        if(max<=dates.index(arrow.early_finish)):
                            max=dates.index(arrow.early_finish)
                            temp_arrow=arrow
                    
                    for arrow in rem.emerging_arrows:
                        self.dict_terminating[arrow.destination_node]=self.dict_terminating[arrow.destination_node]-1
                        if isinstance(temp_arrow,DashedArrow) and isinstance(arrow,DashedArrow):
                            arrow.early_start=dates[max]
                            arrow.early_finish=dates[max]
                            
                        elif isinstance(temp_arrow,DashedArrow) and isinstance(arrow,ArrowTask):
                            arrow.early_start=dates[max]
                            arrow.early_finish=dates[max+arrow.duration-1]
                            
                        elif isinstance(temp_arrow,ArrowTask) and isinstance(arrow,ArrowTask):
                            arrow.early_start=dates[max+1]
                            arrow.early_finish=dates[max+arrow.duration]
                            
                        elif isinstance(temp_arrow,ArrowTask) and isinstance(arrow,DashedArrow):
                            arrow.early_start=dates[max]
                            arrow.early_finish=dates[max]
                            
                        if self.dict_terminating[arrow.destination_node]==0:
                            q.append(arrow.destination_node)
                size=size-1

        q.append(last)
        while(len(q)!=0):
            size=len(q)
            while(size!=0):
                rem=q.popleft()
                if(rem==last):
                    for arrow in rem.terminating_arrows:
                        arrow.late_finish=dates[-1]
                        arrow.late_start=dates[-1]
                        self.dict_emerging[arrow.starting_node]=self.dict_emerging[arrow.starting_node]-1
                        if self.dict_emerging[arrow.starting_node]==0:
                            q.append(arrow.starting_node)
                else:
                    min=len(self.selected_dates)-1
                    temp_arrow=None
                    for arrow in rem.emerging_arrows:
                        if(min>=dates.index(arrow.late_start)):
                            min=dates.index(arrow.late_start)
                            temp_arrow=arrow
                    for arrow in rem.terminating_arrows:
                        self.dict_emerging[arrow.starting_node]=self.dict_emerging[arrow.starting_node]-1
                        if isinstance(temp_arrow,DashedArrow) and isinstance(arrow,DashedArrow):
                            arrow.late_start=dates[min]
                            arrow.late_finish=dates[min]
                            
                        elif isinstance(temp_arrow,DashedArrow) and isinstance(arrow,ArrowTask):
                            arrow.late_finish=dates[min]
                            arrow.late_start=dates[min-arrow.duration+1]
                            
                        elif isinstance(temp_arrow,ArrowTask) and isinstance(arrow,DashedArrow):
                            arrow.late_finish=dates[min]
                            arrow.late_start=dates[min]
                            
                        elif isinstance(temp_arrow,ArrowTask) and isinstance(arrow,ArrowTask):
                            arrow.late_finish=dates[min-1]
                            arrow.late_start=dates[min-arrow.duration]

                        if self.dict_emerging[arrow.starting_node]==0:
                            q.append(arrow.starting_node)
                size=size-1
    
    def create_chart(self):
        if self.selected_dates is None:
            return self.warnings("Enter the starting date from the calendar button.","Missing Starting Date")
        
        self.selected_dates.sort()

        if type(self.selected_dates[0])==QDate:
            for i in range(len(self.selected_dates)):
                self.selected_dates[i]=self.selected_dates[i].toString("yyyy-MM-dd")
        self.early_late(self.starting,self.selected_dates)
        dot1 = visualize_aoa(self.starting)
        png_data1 = dot1.pipe(format='png')
        pixmap1 = QPixmap()
        pixmap1.loadFromData(png_data1)
        self.window =QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.starting=self.starting                 ## storing staring node in create chart
        self.ui.setupUi(self.window)
        # self.ui.spreadsheet=QtWidgets.QApplication.instance().activeWindow()
        self.ui.spreadsheet=self.main_window
        self.window.show()
        self.window.showMaximized()
        self.ui.label_5.setPixmap(pixmap1)
        # QtWidgets.QApplication.instance().activeWindow().hide()
        self.main_window.hide()

    def restart(self):
        self.data_list.clear()
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(["Task ID", "Task Name", "Duration", "Predecessor"])

    def insert_item(self):
        selected_option = self.Insert.currentText()
        selected_range = self.tableWidget.selectedRanges()[0]  # Get the first selected range
        selected_row = selected_range.topRow()
        selected_column = selected_range.leftColumn()

        if selected_option == "Insert Row Up":
            self.tableWidget.insertRow(selected_row)
        elif selected_option == "Insert Row Down":
            self.tableWidget.insertRow(selected_row + 1)
        elif selected_option == "Insert Column Left":
            self.tableWidget.insertColumn(selected_column)
        elif selected_option == "Insert Column Right":
            self.tableWidget.insertColumn(selected_column + 1)
        # Reset the combo box to default option
        self.Insert.setCurrentIndex(0)

    def delete(self):
        selected_option = self.Delete.currentText()
        selected_range = self.tableWidget.selectedRanges()[0]  # Get the first selected range
        if selected_option == "Delete Row":
            self.tableWidget.removeRow(selected_range.topRow())
        elif selected_option == "Delete Column":
            self.tableWidget.removeColumn(selected_range.leftColumn())

        # Reset the combo box to default option
        self.Delete.setCurrentIndex(0)

    def search_table(self):
        search_text = self.Searchlabel.text()
        if not search_text:
            QtWidgets.QMessageBox.warning(self.centralwidget, 'No Input', 'Please enter a search term.')
            return

        found_items = self.tableWidget.findItems(search_text, QtCore.Qt.MatchContains)
        if not found_items:
            QtWidgets.QMessageBox.information(self.centralwidget, 'No Match', 'No matching item found.')
            return

        # Clear previous selections and remove previous custom backgrounds
        for row in range(self.tableWidget.rowCount()):
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, column)
                if item:
                    item.setSelected(False)
                    item.setBackground(QtGui.QColor(238, 255, 255))

        # Set dark blue color for found items
        dark_blue_color = QtGui.QColor(173, 216, 230)

        for item in found_items:
            item.setSelected(True)
            item.setBackground(dark_blue_color)
            self.tableWidget.scrollToItem(item)

    def cut(self):
        clipboard = QtWidgets.QApplication.clipboard()
        selected_items = self.tableWidget.selectedItems()
        
        if not selected_items:
            return
        
        rows = {}
        for item in selected_items:
            row = item.row()
            col = item.column()
            if row not in rows:
                rows[row] = {}
            rows[row][col] = item.text()
            item.setText("")
        
        clipboard_data = ""
        for row in sorted(rows.keys()):
            line = "\t".join(rows[row].get(col, "") for col in range(self.tableWidget.columnCount()))
            clipboard_data += line + "\n"
        
        clipboard.setText(clipboard_data.strip())


    def copy(self):
        clipboard = QtWidgets.QApplication.clipboard()
        selected_items = self.tableWidget.selectedItems()
        
        if not selected_items:
            return
        
        rows = {}
        for item in selected_items:
            row = item.row()
            col = item.column()
            if row not in rows:
                rows[row] = {}
            rows[row][col] = item.text()
        
        clipboard_data = ""
        for row in sorted(rows.keys()):
            line = "\t".join(rows[row].get(col, "") for col in range(self.tableWidget.columnCount()))
            clipboard_data += line + "\n"
        
        clipboard.setText(clipboard_data.strip())

    def paste(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard_text = clipboard.text()
        if not clipboard_text:
            return
        
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            return
        
        start_row = selected_items[0].row()
        start_column = selected_items[0].column()
        
        new_data = [row.split("\t") for row in clipboard_text.split("\n")]
        
        for row in range(len(new_data)):
            for col in range(len(new_data[row])):
                current_row = start_row + row
                current_col = start_column + col
                
                if current_row < self.tableWidget.rowCount() and current_col < self.tableWidget.columnCount():
                    if self.tableWidget.item(current_row, current_col) is None:
                        self.tableWidget.setItem(current_row, current_col, QtWidgets.QTableWidgetItem())
                    self.tableWidget.item(current_row, current_col).setText(new_data[row][col])

    def create_shortcuts(self):
        self.copy_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+C"), self.centralwidget)
        self.copy_shortcut.activated.connect(self.copy)

        self.cut_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+X"), self.centralwidget)
        self.cut_shortcut.activated.connect(self.cut)

        self.paste_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+V"), self.centralwidget)
        self.paste_shortcut.activated.connect(self.paste)
    
    def backing(self):
        from dash import Ui_Dashboard
        self.window =QtWidgets.QMainWindow()
        self.ui = Ui_Dashboard()
        self.ui.setupUi(self.window)
        self.window.show()
        self.window.showMaximized()
        # QtWidgets.QApplication.instance().activeWindow().close()
        self.main_window.close()

    def setupUi(self, Spreadsheet):
        self.main_window = Spreadsheet
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        Spreadsheet.setObjectName("Spreadsheet")
        Spreadsheet.resize(screen_width, screen_height)
        Spreadsheet.setStyleSheet("background-color: rgb(238, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(Spreadsheet)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.centralwidget.setLayout(self.verticalLayout)

        ## Upper menu
        self.upper=QtWidgets.QWidget(self.centralwidget)
        self.verticalLayout.addWidget(self.upper)
        self.upperlayout=QtWidgets.QHBoxLayout(self.upper)
        self.upper.setLayout(self.upperlayout)

        self.back = QtWidgets.QPushButton(self.upper)
        self.back.setGeometry(QtCore.QRect(0, 0, 21, 21))
        self.back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.resource_path("Spreadsheet_images/logout.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back.setIcon(icon)
        self.back.setObjectName("back")
        self.back.clicked.connect(self.backing)

        self.Save = QtWidgets.QPushButton(self.upper)
        self.Save.setGeometry(QtCore.QRect(30, 0, 21, 21))
        self.Save.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.resource_path("Spreadsheet_images/diskette.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Save.setIcon(icon)
        self.Save.setObjectName("Save")

        self.Undo = QtWidgets.QPushButton(self.upper)
        self.Undo.setGeometry(QtCore.QRect(60, 0, 21, 21))
        self.Undo.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.resource_path("Spreadsheet_images/undo.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Undo.setIcon(icon1)
        self.Undo.setObjectName("Undo")

        self.Redo = QtWidgets.QPushButton(self.upper)
        self.Redo.setGeometry(QtCore.QRect(85, 0, 21, 21))
        self.Redo.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.resource_path("Spreadsheet_images/redo.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Redo.setIcon(icon2)
        self.Redo.setObjectName("Redo")

        self.Restart = QtWidgets.QPushButton(self.upper)
        self.Restart.setGeometry(QtCore.QRect(110, 0, 21, 21))
        self.Restart.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(self.resource_path("Spreadsheet_images/restart.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Restart.setIcon(icon3)
        self.Restart.setObjectName("Restart")
        self.create_shortcuts()
        self.Restart.clicked.connect(self.restart)

        self.label = QtWidgets.QLabel(self.upper)
        self.label.setGeometry(QtCore.QRect(180, 0, 61, 21))
        self.label.setObjectName("label")

        ## Middle menu
        self.middle=QtWidgets.QWidget(self.centralwidget)
        self.verticalLayout.addWidget(self.middle)
        self.middle.setStyleSheet("background-color: rgb(182, 182, 182);")
        self.middlehorizontallayout=QtWidgets.QHBoxLayout(self.middle)
        self.middle.setLayout(self.middlehorizontallayout)

        ## middle left
        self.middleleft=QtWidgets.QWidget(self.middle)
        self.middlehorizontallayout.addWidget(self.middleleft)
        self.middlelefthorizontallayout=QtWidgets.QHBoxLayout(self.middleleft)
        self.middleleft.setLayout(self.middlelefthorizontallayout)

        self.Paste = QtWidgets.QPushButton(self.middleleft)
        self.Paste.setEnabled(True)
        # self.Paste.setGeometry(QtCore.QRect(10, 10, 41, 51))
        self.Paste.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(self.resource_path("Spreadsheet_images/paste.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Paste.setIcon(icon4)
        self.Paste.setIconSize(QtCore.QSize(80, 100))
        self.Paste.setObjectName("Paste")
        self.middlelefthorizontallayout.addWidget(self.Paste)
        self.Paste.clicked.connect(self.paste)

        self.Cut = QtWidgets.QPushButton(self.middleleft)
        # self.Cut.setGeometry(QtCore.QRect(60, 10, 31, 21))
        self.Cut.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(self.resource_path("Spreadsheet_images/cutting.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Cut.setIcon(icon5)
        self.Cut.setIconSize(QtCore.QSize(80, 100))
        self.Cut.setObjectName("Cut")
        self.middlelefthorizontallayout.addWidget(self.Cut)
        self.Cut.clicked.connect(self.cut)

        self.Copy = QtWidgets.QPushButton(self.middleleft)
        # self.Copy.setGeometry(QtCore.QRect(60, 40, 31, 21))
        self.Copy.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(self.resource_path("Spreadsheet_images/files.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Copy.setIcon(icon6)
        self.Copy.setIconSize(QtCore.QSize(80, 100))
        self.Copy.setObjectName("Copy")
        self.middlelefthorizontallayout.addWidget(self.Copy)
        self.Copy.clicked.connect(self.copy)

        ## middle right
        self.middleright=QtWidgets.QWidget(self.middle)
        self.middlehorizontallayout.addWidget(self.middleright)
        self.middlerightverticallayout=QtWidgets.QVBoxLayout(self.middleright)
        self.middleright.setLayout(self.middlerightverticallayout)

        ## middle right1
        self.middleright1=QtWidgets.QWidget(self.middleright)
        self.middlerightverticallayout.addWidget(self.middleright1)
        self.middleright1horizontallayout=QtWidgets.QHBoxLayout(self.middleright1)
        self.middleright1.setLayout(self.middleright1horizontallayout)

        self.Insert = QtWidgets.QComboBox(self.middleright1)
        # self.Insert.setGeometry(QtCore.QRect(360, 10, 101, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Insert.setFont(font)
        self.Insert.setObjectName("Insert")
        self.Insert.addItem("Insert")
        self.Insert.addItem("Insert Row Up")
        self.Insert.addItem("Insert Row Down")
        self.Insert.addItem("Insert Column Left")
        self.Insert.addItem("Insert Column Right")
        self.middleright1horizontallayout.addWidget(self.Insert)
        self.Insert.currentIndexChanged.connect(self.insert_item)

        self.Createchart = QtWidgets.QPushButton(self.middleright1)
        # self.Createchart.setGeometry(QtCore.QRect(470, 10, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Createchart.setFont(font)
        self.Createchart.setObjectName("Createchart")
        self.middleright1horizontallayout.addWidget(self.Createchart)
        self.Createchart.clicked.connect(self.create_chart)

        self.Calender = QtWidgets.QPushButton(self.middleright1)
        # self.Calender.setGeometry(QtCore.QRect(560, 10, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Calender.setFont(font)
        self.Calender.setObjectName("Calender")
        self.Calender.clicked.connect(self.open_calendar_app)
        self.middleright1horizontallayout.addWidget(self.Calender)

        ## middle right2
        self.middleright2=QtWidgets.QWidget(self.middleright)
        self.middlerightverticallayout.addWidget(self.middleright2)
        self.middleright2horizontallayout=QtWidgets.QHBoxLayout(self.middleright2)
        self.middleright2.setLayout(self.middleright2horizontallayout)

        self.Delete = QtWidgets.QComboBox(self.middleright2)
        # self.Delete.setGeometry(QtCore.QRect(360, 40, 101, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Delete.setFont(font)
        self.Delete.setObjectName("Delete")
        self.Delete.addItem("Delete")
        self.Delete.addItem("Delete Row")
        self.Delete.addItem("Delete Column")
        self.middleright2horizontallayout.addWidget(self.Delete)
        self.Delete.activated.connect(self.delete)

        self.Searchlabel = QtWidgets.QLineEdit(self.middleright2)
        # self.Searchlabel.setGeometry(QtCore.QRect(470, 40, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Searchlabel.setFont(font)
        self.Searchlabel.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Searchlabel.setObjectName("Searchlabel")
        self.middleright2horizontallayout.addWidget(self.Searchlabel)

        self.Search = QtWidgets.QPushButton(self.middleright2)
        # self.Search.setGeometry(QtCore.QRect(530, 40, 21, 21))
        self.Search.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Search.setText("")
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(self.resource_path("Spreadsheet_images/search.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Search.setIcon(icon16)
        self.Search.setObjectName("Search")
        self.middleright2horizontallayout.addWidget(self.Search)
        self.Search.clicked.connect(self.search_table)

        self.Filter = QtWidgets.QPushButton(self.middleright2)
        # self.Filter.setGeometry(QtCore.QRect(560, 40, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Filter.setFont(font)
        self.Filter.setObjectName("Filter")
        self.middleright2horizontallayout.addWidget(self.Filter)

        self.middleright2horizontallayout.setStretchFactor(self.Delete,100)
        self.middleright2horizontallayout.setStretchFactor(self.Searchlabel,80)
        self.middleright2horizontallayout.setStretchFactor(self.Search,20)
        self.middleright2horizontallayout.setStretchFactor(self.Filter,100)

        self.middlehorizontallayout.setStretchFactor(self.middleleft,4)
        self.middlehorizontallayout.setStretchFactor(self.middleright,25)

        ## Lower menu
        self.lower=QtWidgets.QWidget(self.centralwidget)
        self.verticalLayout.addWidget(self.lower)
        self.lowerlayout=QtWidgets.QHBoxLayout(self.lower)
        self.lower.setLayout(self.lowerlayout)
        self.tableWidget = QtWidgets.QTableWidget(self.lower)
        # self.tableWidget.setGeometry(QtCore.QRect(0, 90, 661, 301))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(16)
        self.tableWidget.setRowCount(50)
        self.tableWidget.setHorizontalHeaderLabels(["Task ID", "Task Name", "Duration", "Predecessor"])
        self.lowerlayout.addWidget(self.tableWidget)
        self.tableWidget.verticalScrollBar().valueChanged.connect(self.on_scroll)
        self.tableWidget.itemChanged.connect(self.on_item_changed)

        self.verticalLayout.setStretchFactor(self.upper,2)
        self.verticalLayout.setStretchFactor(self.middle,25)
        self.verticalLayout.setStretchFactor(self.lower,100)

        Spreadsheet.setCentralWidget(self.centralwidget)
        self.retranslateUi(Spreadsheet)
        QtCore.QMetaObject.connectSlotsByName(Spreadsheet)

    def on_scroll(self):
        if self.tableWidget.verticalScrollBar().value() == self.tableWidget.verticalScrollBar().maximum():
            self.add_row()

    def on_item_changed(self, item):
        if item.row() == self.tableWidget.rowCount() - 1:
            self.add_row()

    def add_row(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)

    def retranslateUi(self, Spreadsheet):
        _translate = QtCore.QCoreApplication.translate
        Spreadsheet.setWindowTitle(_translate("Spreadsheet", "Spreadsheet Window"))
        self.label.setText(_translate("Spreadsheet", "Project Title-1"))
        self.Insert.setItemText(0, _translate("Spreadsheet", "Insert"))
        self.Insert.setItemText(1, _translate("Spreadsheet", "Insert Row Down"))
        self.Insert.setItemText(2, _translate("Spreadsheet", "Insert Row Up"))
        self.Insert.setItemText(3, _translate("Spreadsheet", "Insert Column Left"))
        self.Insert.setItemText(4, _translate("Spreadsheet", "Insert Column Right"))
        self.Delete.setItemText(0, _translate("Spreadsheet", "Delete"))
        self.Delete.setItemText(1, _translate("Spreadsheet", "Delete Row"))
        self.Delete.setItemText(2, _translate("Spreadsheet", "Delete Column"))
        self.Createchart.setText(_translate("Spreadsheet", "Create Chart"))
        self.Calender.setText(_translate("Spreadsheet", "Calender"))
        self.Filter.setText(_translate("Spreadsheet", "Filter"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Spreadsheet = QtWidgets.QMainWindow()
    Spreadsheet.showMaximized()
    ui = Ui_Spreadsheet()
    ui.setupUi(Spreadsheet)
    Spreadsheet.show()
    sys.exit(app.exec_())