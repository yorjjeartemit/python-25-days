from tkinter import *
class Area(Tk):
    def __init__(self):
        super(Area,self).__init__()
        self.count=0
        self.title("clicker on tkinter")
        self.geometry("128x64")
        self.minsize(128,64)
        self.maxsize(256,128)   
    def button(self,count):
        self.count+=count
def update_btn():
    win.button(1)
    btn['text']=f"click:{win.count}"


win=Area()
btn=Button(win,text=f"click:{win.count}",font=("Arial",20,"bold"),bg="red",command=update_btn)
btn.place(relx=0.5,rely=0.5,anchor="center")
win.mainloop()