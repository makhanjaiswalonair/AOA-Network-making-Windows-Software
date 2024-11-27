from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QStackedWidget, QWidget, QLabel
from PyQt5.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setFixedSize(600, 400)  # Setting a fixed size for the modal

        # Main layout
        main_layout = QVBoxLayout()
        
        # Remove the "?" button from the title bar
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        # Left pane with tabs
        left_pane = QListWidget()
        left_pane.addItem("General")
        left_pane.addItem("Account")
        left_pane.addItem("Personalisation")
        left_pane.addItem("Preferences")
        left_pane.addItem("Help")
        left_pane.setFixedWidth(150)  # Set fixed width for the left pane
        left_pane.currentRowChanged.connect(self.display_tab)

        # Right pane with settings
        self.right_pane = QStackedWidget()
        self.right_pane.addWidget(self.general_settings())
        self.right_pane.addWidget(self.account_settings())
        self.right_pane.addWidget(self.personalisation_settings())
        self.right_pane.addWidget(self.preferences_settings())
        self.right_pane.addWidget(self.help_settings())

        # Split layout
        split_layout = QHBoxLayout()
        split_layout.addWidget(left_pane)
        split_layout.addWidget(self.right_pane)
        main_layout.addLayout(split_layout)

        self.setLayout(main_layout)

    def display_tab(self, index):
        self.right_pane.setCurrentIndex(index)

    def general_settings(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("General Settings"))
        widget.setLayout(layout)
        return widget

    def network_settings(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Network Settings"))
        widget.setLayout(layout)
        return widget

    def display_settings(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Display Settings"))
        widget.setLayout(layout)
        return widget
    
    def account_settings(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Account Settings"))
        widget.setLayout(layout)
        return widget
    
    def personalisation_settings(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Personalisation Settings"))
        widget.setLayout(layout)
        return widget
    
    def preferences_settings(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Preferences Settings"))
        widget.setLayout(layout)
        return widget
    
    def help_settings(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Help Settings"))
        widget.setLayout(layout)
        return widget