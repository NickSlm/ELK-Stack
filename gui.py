from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWindow, QPixmap
from PyQt5.QtWidgets import *
import sys
from utils import Instances

def open_file():
    """
    Returns selected file
    """
    file, check = QFileDialog.getOpenFileName(None,"Choose File","","All Files (*);;Python Files (*.py);;Text Files (*.txt)")
    if check:
        return file

class UI_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "ELK Setup"
        self.WIDTH = 720
        self.HEIGHT = 576

        self.setGeometry(500,250,self.WIDTH,self.HEIGHT)
        self.setWindowTitle(self.title)

        self.tab_widget = TabWidgets()
        self.setCentralWidget(self.tab_widget)

        self.show()

class TabWidgets(QWidget):
    def __init__(self):
        super(TabWidgets, self).__init__()
        self.layout = QVBoxLayout(self)
        # Init tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tabs.resize(300,300)

        # Tabs
        self.tabs.addTab(self.tab1,"Instances")
        self.tabs.addTab(self.tab2,"Env variables")
        self.tabs.addTab(self.tab3,"Create certs")
        self.tabs.addTab(self.tab4,"Docker compose")
        self.tabs.addTab(self.tab5,"Finalize")

        # Create first tab
        self.instances_form = InstancesForm()
        self.tab1.layout = self.instances_form.grid
        self.tab1.setLayout(self.tab1.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class InstancesForm(QDialog):
    def __init__(self):
        super(InstancesForm,self).__init__()
        # Instances file
        self.instances_file = Instances()

        # GUI elements
        self.grid = QGridLayout()
        self.form_instance_group_box = QGroupBox("Add host manually")
        self.form_upload_group_box = QGroupBox("Upload hosts file")
        self.instruction_group_box = QGroupBox("Instruction")

        self.name_input = QLineEdit()
        self.name_input.setFixedWidth(160)
        self.dns_input = QLineEdit()
        self.dns_input.setFixedWidth(160)
        self.ip_input = QLineEdit()
        self.ip_input.setFixedWidth(160)
        self.file_lb = QLabel("Choose your hosts file:")
        self.file_lb.setFixedWidth(250)

        self.button_add = QPushButton('Add', self)
        self.button_add.setFixedWidth(160)
        self.button_add.clicked.connect(self.add_instance)

        self.button_clear = QPushButton('clear', self)
        self.button_clear.setFixedWidth(160)
        self.button_clear.clicked.connect(self.clear_fields)

        self.button_upload = QPushButton("Upload",self)
        self.button_upload.clicked.connect(self.upload_file)
  
        self.create_instance_form()
        self.create_upload_layout()
        self.create_instruction_layout()
        self.create_logs_layout()

        self.grid.addWidget(self.form_instance_group_box,0,0)
        self.grid.addWidget(self.form_upload_group_box,0,1)
        self.grid.addWidget(self.scroll,1,0)
        self.grid.addWidget(self.instruction_group_box,1,1)

    def clear_fields(self):
        self.name_input.clear()
        self.dns_input.clear()
        self.ip_input.clear()
    def create_instance_form(self):
        layout = QFormLayout()
        layout.addRow(QLabel("Name:"),self.name_input)
        layout.addRow(QLabel("DNS:"),self.dns_input)
        layout.addRow(QLabel("IP address:"), self.ip_input)
        layout.addRow(self.button_clear,self.button_add)
        self.form_instance_group_box.setLayout(layout)
    def create_upload_layout(self):
        layout = QFormLayout()
        layout.addRow(self.file_lb,self.button_upload)
        self.form_upload_group_box.setLayout(layout)
    def create_instruction_layout(self):
        layout = QVBoxLayout()
        img_lb = QLabel()
        img_pixmap = QPixmap(r"D:\ELK docker-compose script\Image\Capture.JPG")
        img_lb.setPixmap(img_pixmap)
        instruction_lb = QLabel("* Add all the hosts that will be in the ELK stack.\n   You can add host by host manually or upload a txt/json/csv file\n   with a list of hosts.\n* You can add hosts through file AND manually.\n* If adding through file, file format should look like the image below:")
        instruction_lb.setWordWrap(True)
        layout.addWidget(instruction_lb)
        layout.addWidget(img_lb)
        self.instruction_group_box.setLayout(layout)
    def create_logs_layout(self):
        self.scroll = QScrollArea()
        widget = QWidget()
        self.log_box = QVBoxLayout()
        widget.setLayout(self.log_box)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(widget)
    def upload_file(self):
        file_name = open_file()
        if file_name:
            self.file_lb.setText(file_name)
            self.instances_file.add_host_file(file_name)   
            self.log_box.addWidget(QLabel("- Successfully added: {0}".format(file_name)))        
    def add_instance(self):
        if self.name_input.text() and self.dns_input.text() and self.ip_input.text():
            host_dict = {"name":self.name_input.text(),"dns":[self.dns_input.text()],"ip":[self.ip_input.text()]}
            self.instances_file.add_host(host_dict)
            self.log_box.addWidget(QLabel(f"- Host: {self.name_input.text()} - {self.ip_input.text()} was successfully added"))

class EnvForm(QDialog):
    def __init__(self):
        super(EnvForm,self).__init__()
        pass
class CertsForm(QDialog):
    def __init__(self):
        super(CertsForm,self).__init__()
        pass
class DockerComposeForm(QDialog):
    def __init__(self):
        super(DockerComposeForm,self).__init__()
        pass


