import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCalendarWidget, QPushButton
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat, QColor

class CalendarApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set up the window
        self.setWindowTitle('Calendar UI')
        self.setGeometry(100, 100, 400, 300)
        
        # Set up the layout
        layout = QVBoxLayout()
        
        # Set up the calendar widget
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.toggle_date_selection)
        
        # Set up the button to clear selections
        # self.clear_button = QPushButton("Clear Selections", self)
        # self.clear_button.clicked.connect(self.clear_selections)

        self.OK_button = QPushButton("OK", self)
        self.OK_button.clicked.connect(self.hide_widget)
        
        # Add widgets to the layout
        layout.addWidget(self.calendar)
        # layout.addWidget(self.clear_button)
        layout.addWidget(self.OK_button)
        
        # Set the layout to the window
        self.setLayout(layout)
        
        # Initialize the list of selected dates
        self.selected_dates = []
        self.start_date = None
        self.duration = 0
    
    def hide_widget(self):
        self.close()
        # print("Printing from calender")
        # for date in self.selected_dates:
        #     print(date)

    def toggle_date_selection(self):
        # Get the selected date
        selected_date = self.calendar.selectedDate()
        
        # Toggle the date selection
        if selected_date in self.selected_dates:
            self.selected_dates.remove(selected_date)
            self.update_date_format(selected_date, remove=True)
            
            # Automatically select additional dates to maintain the duration
            if self.start_date and self.duration:
                while len(self.selected_dates) < self.duration:
                    last_date = max(self.selected_dates) if self.selected_dates else self.start_date
                    new_date = last_date.addDays(1)
                    while new_date.dayOfWeek() in (Qt.Saturday, Qt.Sunday):
                        new_date = new_date.addDays(1)
                    self.selected_dates.append(new_date)
                    self.update_date_format(new_date)
        else:
            if len(self.selected_dates) >= self.duration:
                # Deselect the last date to maintain the duration
                self.update_date_format(self.selected_dates[-1], remove=True)
                self.selected_dates.pop()
            self.selected_dates.append(selected_date)
            self.update_date_format(selected_date)
        
        # Update the label to display the selected dates
        # dates_text = ", ".join([date.toString() for date in self.selected_dates])
        # print(f"Selected Dates: {dates_text if dates_text else 'None'}")  # For debugging purposes
    
    def update_date_format(self, date, remove=False):
        # Create a text format object
        format = QTextCharFormat()
        
        # Set the background color based on selection
        if remove:
            format.setBackground(QColor("white"))
        else:
            format.setBackground(QColor("yellow"))
        
        # Apply the format to the selected date
        self.calendar.setDateTextFormat(date, format)
        
    def clear_selections(self):
        # Clear all selected dates
        for date in self.selected_dates:
            self.update_date_format(date, remove=True)
        self.selected_dates.clear()
    
    def select_dates_from(self, start_date: QDate, duration: int):
        # Clear current selections
        self.clear_selections()
        
        # Track start date and duration
        self.start_date = start_date
        self.duration = duration
        
        # Select dates from start_date for the duration, skipping Saturdays and Sundays
        selected_count = 0
        current_date = start_date
        
        while selected_count < duration:
            if current_date.dayOfWeek() not in (Qt.Saturday, Qt.Sunday):
                self.selected_dates.append(current_date)
                self.update_date_format(current_date)
                selected_count += 1
            current_date = current_date.addDays(1)

if __name__ == '__main__':
    # Create the application
    app = QApplication(sys.argv)
    
    # Create the calendar window
    calendar_window = CalendarApp()
    calendar_window.show()
    
    # Example: Select dates from today for the next 10 days, skipping weekends
    # start_date = QDate.currentDate()
    # duration = 10
    # calendar_window.select_dates_from(start_date, duration)
    
    # Execute the application
    sys.exit(app.exec_())