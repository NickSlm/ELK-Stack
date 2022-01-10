from PyQt5 import QtWidgets
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
        self.tab1.layout = QVBoxLayout(self)
        self.l = QLabel()
        self.l.setText("This is the first tab")
        self.tab1.layout.addWidget(self.l)
        self.tab1.setLayout(self.tab1.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class InstancesForm(QDialog):
    def __init__(self):
        super(InstancesForm,self).__init__()
        pass

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


