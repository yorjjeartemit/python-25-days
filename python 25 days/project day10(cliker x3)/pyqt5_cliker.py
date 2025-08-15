from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
import sys

class Clicker(QWidget):
    def __init__(self):
        super().__init__()
        self.count=0
        self.max_count=100
        self.min_count=0
        self.setWindowTitle("cliker PyQt5")
        self.setFixedSize(300,200)
        self.layout=QVBoxLayout()
        self.label=QLabel(str(self.count),self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 32px;")
        self.button=QPushButton("toch me",self)
        self.button.setStyleSheet("font-size: 24px; padding: 10px;")
        self.button.clicked.connect(self.increment)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
    def increment(self):
        if self.count<self.max_count:
            self.count+=1
            self.label.setText(str(self.count))
app=QApplication(sys.argv)
window=Clicker()
window.show()
sys.exit(app.exec_())
