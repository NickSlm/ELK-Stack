from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import *
import sys

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

        self.tab1.layout = self.instances_form.main_layout
        self.tab1.setLayout(self.tab1.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class InstancesForm(QDialog):
    def __init__(self):
        super(InstancesForm,self).__init__()
        self.main_layout = QVBoxLayout()
        self.form_group_box = QGroupBox("Add Instance")
        self.name_input = QLineEdit()
        self.dns_input = QLineEdit()
        self.ip_input = QLineEdit()
        
        self.button_box = QPushButton('Add', self)
        self.button_box.clicked.connect(self.add_instance)
  
        self.create_form()
        self.main_layout.addWidget(self.form_group_box)

    def create_form(self):
        layout = QFormLayout()
        layout.addRow(QLabel("Name:"),self.name_input)
        layout.addRow(QLabel("DNS:"),self.dns_input)
        layout.addRow(QLabel("IP address:"), self.ip_input)
        layout.addRow(self.button_box)
        self.form_group_box.setLayout(layout)

    def add_instance(self):
        # TODO: CHECK IF NOT EMPTY

        print("Successfully added: \nName: {0}\nDNS: {1}\nIP address: {2}".format(self.name_input.text(),self.dns_input.text(),self.ip_input.text()))


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


