import sys
import requests
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox, QMessageBox, QWidget, QStackedWidget, QFrame, QSpacerItem, QSizePolicy
import configparser

class LoginDialog(QDialog):
    login_successful = pyqtSignal(str, str)  # Signal to emit username and firstName (replace with actual data types as needed

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")

        # Remove the "?" button from the title bar
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        self.setFixedSize( 300, 380)

        # Widgets for login form
        self.username_edit_login = QLineEdit()
        self.password_edit_login = QLineEdit()
        self.password_edit_login.setEchoMode(QLineEdit.EchoMode.Password)
        self.show_password_checkbox_login = QCheckBox("Show Password")
        self.login_button = QPushButton("Login")
        self.go_to_create_acc_button = QPushButton("Create New Account")

        # Widgets for create account form
        self.name_edit_create = QLineEdit()
        self.username_edit_create = QLineEdit()
        self.password_edit_create = QLineEdit()
        self.password_edit_create.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_edit_create = QLineEdit()
        self.confirm_password_edit_create.setEchoMode(QLineEdit.EchoMode.Password)
        self.go_to_login_button = QPushButton("Login")
        self.create_account_button = QPushButton("Create New Account")

        # Layouts for login and create account forms
        self.login_layout = QVBoxLayout()
        self.login_layout.addWidget(QLabel("Username"))
        self.login_layout.addWidget(self.username_edit_login)
        self.login_layout.addWidget(QLabel("Password"))
        self.login_layout.addWidget(self.password_edit_login)
        self.login_layout.addWidget(self.show_password_checkbox_login)
        self.login_layout.addWidget(self.login_button)
        self.login_layout.addWidget(QLabel("Don't have an account?"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.login_layout.addWidget(self.go_to_create_acc_button)

        self.create_account_layout = QVBoxLayout()
        self.create_account_layout.addWidget(QLabel("Name"))
        self.create_account_layout.addWidget(self.name_edit_create)
        self.create_account_layout.addWidget(QLabel("Username"))
        self.create_account_layout.addWidget(self.username_edit_create)
        self.create_account_layout.addWidget(QLabel("Password"))
        self.create_account_layout.addWidget(self.password_edit_create)
        self.create_account_layout.addWidget(QLabel("Confirm Password"))
        self.create_account_layout.addWidget(self.confirm_password_edit_create)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.create_account_layout.addWidget(spacer)  # Vertical spacer
        self.create_account_layout.addWidget(self.create_account_button)
        self.create_account_layout.addWidget(QLabel("Already have an account?"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.create_account_layout.addWidget(self.go_to_login_button)

        # Stacked widget to switch between login and create account layouts
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(QWidget())  # Index 0 for login layout
        self.stacked_widget.addWidget(QWidget())  # Index 1 for create account layout
        self.stacked_widget.widget(0).setLayout(self.login_layout)
        self.stacked_widget.widget(1).setLayout(self.create_account_layout)

        # Main layout for the dialog
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)

        # Connections
        self.login_button.clicked.connect(self.login)
        self.go_to_create_acc_button.clicked.connect(self.switch_to_create_account)
        self.go_to_login_button.clicked.connect(self.switch_to_login)
        self.show_password_checkbox_login.stateChanged.connect(self.toggle_password_visibility)
        self.create_account_button.clicked.connect(self.create_account)

    def login(self):
        username = self.username_edit_login.text()
        password = self.password_edit_login.text()

        # Send login request (replace with actual URL and parameters as needed)
        login_url = "https://dummyjson.com/auth/login"
        payload = {"username": username, "password": password}

        try:
            response = requests.post(login_url, json=payload)
            username = response.json().get("username")
            firstName = response.json().get("firstName")
            token = response.json().get("token")
            if response.status_code == 200:
                # Save username to config file
                config = configparser.ConfigParser()
                config['User'] = {'username': username, 'firstName': firstName, 'token': token}
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
        
                self.login_successful.emit(username, firstName)
                self.accept()  # Close dialog on successful login
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error during login: {e}")
            
    def create_account(self):
        name = self.name_edit_create.text()
        username = self.username_edit_create.text()
        password = self.password_edit_create.text()
        confirm_password = self.confirm_password_edit_create.text()

        # Validate inputs (basic validation)
        if not name or not username or not password or not confirm_password:
            QMessageBox.warning(self, "Create Account", "Please fill in all fields.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Create Account", "Passwords do not match.")
            return

        # Send create account request (replace with actual URL and parameters as needed)
        create_account_url = "https://dummyjson.com/auth/create_account"
        payload = {
            "name": name,
            "username": username,
            "password": password
        }

        try:
            response = requests.post(create_account_url, json=payload)
            username = response.json().get("username")
            firstName = response.json().get("firstName")
            token = response.json().get("token")
            
            if response.status_code == 201:  # Assuming successful account creation status
                QMessageBox.information(self, "Account Created", "Account created successfully.")
                self.stacked_widget.setCurrentIndex(0)  # Switch back to login
                self.username_edit_login.setText(username)  # Optionally fill username in login form
                self.password_edit_login.setText("")  # Clear password field for security

                # Save username to config file
                config = configparser.ConfigParser()
                config['User'] = {'username': username, 'firstName': firstName, 'token': token}
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                
                self.login_successful.emit(username, firstName)
            else:
                QMessageBox.warning(self, "Create Account Failed", "Failed to create account.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error creating account: {e}")
            
    def switch_to_create_account(self):
        self.stacked_widget.setCurrentIndex(1)
        # Optionally retain entered data
        self.username_edit_create.setText(self.username_edit_login.text())  # Uncomment to retain entered username
        self.password_edit_create.setText(self.password_edit_login.text())  # Uncomment to retain entered username

        self.setWindowTitle("Create Account")
        
    def switch_to_login(self):
        self.stacked_widget.setCurrentIndex(0)
        # Optionally retain entered data
        self.username_edit_login.setText(self.username_edit_create.text())  # Uncomment to retain entered username
        self.password_edit_login.setText(self.password_edit_create.text())  # Uncomment to retain entered username

        self.setWindowTitle("Login")

    def toggle_password_visibility(self, state):
        if state == Qt.CheckState.Checked:
            self.password_edit_login.setEchoMode(QLineEdit.Normal)
            self.password_edit_create.setEchoMode(QLineEdit.Normal)
            self.confirm_password_edit_create.setEchoMode(QLineEdit.Normal)
        else:
            self.password_edit_login.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_edit_create.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_password_edit_create.setEchoMode(QLineEdit.EchoMode.Password)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = LoginDialog()
    dialog.show()
    sys.exit(app.exec_())
