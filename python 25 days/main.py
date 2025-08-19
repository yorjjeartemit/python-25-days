from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QVBoxLayout,QFrame
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QFont
import pygame,sys,numpy as np,time

pygame.mixer.init(frequency=44100,size=-16,channels=1)

class ToyPiano(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("silly piano")
		self.fullW=1200
		self.fullH=220
		self.darkH=int(self.fullH*0.6)
		self.setFixedSize(self.fullW+40,self.fullH+60)
		self.btnHold={}
		self.mapKeys={}
		self.lastTap={}
		self.uiReady()
		self.setFocusPolicy(Qt.StrongFocus)

	def uiReady(self):
		self.baseLay=QVBoxLayout(self)
		self.baseLay.setContentsMargins(20,10,20,10)
		self.zone=QFrame(self)
		self.zone.setFixedSize(self.fullW,self.fullH)
		self.zone.setStyleSheet("background:#f0f0f0;border:1px solid #888;")
		self.baseLay.addWidget(self.zone,alignment=Qt.AlignHCenter)
		self.spawnBtns()

	def spawnBtns(self):
		whiteRow=[("C4","Z"),("D4","X"),("E4","C"),("F4","V"),("G4","B"),("A4","N"),("B4","M"),("C5","Q"),("D5","W"),("E5","E"),("F5","R"),("G5","T"),("A5","Y"),("B5","U")]
		blackRow=[("C#4","S",0),("D#4","D",1),("F#4","G",3),("G#4","H",4),("A#4","J",5),("C#5","2",7),("D#5","3",8),("F#5","5",10),("G#5","6",11),("A#5","7",12)]
		allW=len(whiteRow)
		wide=self.fullW//allW
		darkW=int(wide*0.6)
		for idx,(note,lab) in enumerate(whiteRow):
			posX=idx*wide
			btn=QPushButton(self.zone)
			btn.setGeometry(posX,0,wide,self.fullH)
			btn.setText(f"{lab}\n{note}")
			btn.setFont(QFont("Arial",10))
			btn.setStyleSheet("QPushButton{background:white;border:1px solid black;}QPushButton:pressed{background:#e6e6e6;}")
			btn.clicked.connect(lambda _,n=note:self.tapNote(n))
			btn.setProperty("dark",False)
			btn.show()
			self.btnHold[note]=btn
		for note,lab,lid in blackRow:
			posL=lid*wide
			posX=posL+wide-darkW//2
			btn=QPushButton(self.zone)
			btn.setGeometry(posX,0,darkW,self.darkH)
			btn.setText(f"{lab}\n{note}")
			btn.setFont(QFont("Arial",9))
			btn.setStyleSheet("QPushButton{background:black;color:white;border:1px solid #111;}QPushButton:pressed{background:#333;}")
			btn.clicked.connect(lambda _,n=note:self.tapNote(n))
			btn.setProperty("dark",True)
			btn.raise_()
			btn.show()
			self.btnHold[note]=btn
		for note,lab in whiteRow:self.mapKeys[lab.upper()]=note
		for note,lab,_ in blackRow:self.mapKeys[lab.upper()]=note

	def tapNote(self,note):
		self.makeNoise(note)
		self.flashBtn(note)

	def makeNoise(self,note,dur=500):
		now=time.time()
		if note in self.lastTap and now-self.lastTap[note]<1:return
		self.lastTap[note]=now
		f=self.freqNote(note)
		rate=44100
		t=np.linspace(0,dur/1000,int(rate*dur/1000),False)
		wave=0.5*np.sin(2*np.pi*f*t)
		stereo=np.column_stack((wave,wave))
		sound=pygame.sndarray.make_sound((stereo*32767).astype(np.int16))
		sound.play()

	def freqNote(self,note):
		ref=440.0
		scale={"C":-9,"C#":-8,"D":-7,"D#":-6,"E":-5,"F":-4,"F#":-3,"G":-2,"G#":-1,"A":0,"A#":1,"B":2}
		name=note[:-1]
		octv=int(note[-1])
		shift=scale[name]+12*(octv-4)
		return ref*(2**(shift/12.0))

	def flashBtn(self,note):
		btn=self.btnHold.get(note)
		if not btn:return
		dark=bool(btn.property("dark"))
		if dark:
			btn.setStyleSheet("QPushButton{background:#333;color:white;border:1px solid #111;}")
			QTimer.singleShot(120,lambda:btn.setStyleSheet("QPushButton{background:black;color:white;border:1px solid #111;}QPushButton:pressed{background:#333;}"))
		else:
			btn.setStyleSheet("QPushButton{background:#e6e6e6;border:1px solid black;}")
			QTimer.singleShot(120,lambda:btn.setStyleSheet("QPushButton{background:white;border:1px solid black;}QPushButton:pressed{background:#e6e6e6;}"))

	def keyPressEvent(self,e):
		txt=e.text()
		if not txt:return
		ch=txt.upper()
		if ch in self.mapKeys:
			note=self.mapKeys[ch]
			self.makeNoise(note)
			self.flashBtn(note)

if __name__=="__main__":
	app=QApplication(sys.argv)
	ins=ToyPiano()
	ins.show()
	sys.exit(app.exec_())
