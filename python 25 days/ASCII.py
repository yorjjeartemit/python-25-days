import pyfiglet
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QTextEdit
import sys
class ASCII(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASCII")
        self.resize(1000,400)

        self.input=QLineEdit(self)
        self.input.move(20,20)
        self.input.resize(960,36)
        self.output = QTextEdit(self)
        self.output.move(20,60)
        self.output.resize(960,320)
        self.output.setReadOnly(True)
        self.output.setStyleSheet("font-family: monospace; font-size: 10pt")
        self.input.returnPressed.connect(self.show_ascii)
        self.output.setLineWrapMode(QTextEdit.NoWrap)
    def show_ascii(self):
        text=self.input.text()
        texts=pyfiglet.figlet_format(text,font="small")
        self.output.setPlainText(texts)
        texts=pyfiglet.print_figlet(f"{text}",colors="GREEN")

if __name__=="__main__":
    app=QApplication(sys.argv) 
    window=ASCII()
    window.show()
    sys.exit(app.exec ())
