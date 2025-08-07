import tkinter as ti
from tkinter import filedialog,messagebox
import os
import json
import subprocess
#varible
file="programs.json"
#classes
class Launchers:
    def __init__(self,root):
        self.root=root
        self.root.title("Launcher Python")
        self.programs=[]
        self.block=ti.Frame(root)
        self.block.pack(padx=16,pady=16)
        self.listbox=ti.Listbox(self.block,width=56,height=16)
        self.listbox.pack(side=ti.LEFT)
        scrolbar=ti.Scrollbar(self.block,command=self.listbox.yview)
        scrolbar.pack(side=ti.LEFT,fill=ti.Y)
        self.listbox.config(yscrollcommand=scrolbar.set)
        button_block=ti.Frame(root)
        button_block.pack(pady=16)
        ti.Button(button_block,text="adds program",command=self.add_program).grid(row=0,column=0,padx=5)
        ti.Button(button_block,text="run program",command=self.run_program).grid(row=0,column=1,padx=5)
        ti.Button(button_block,text="delete program",command=self.delete_program).grid(row=0,column=2,padx=5)
        self.load_program()
    def update_listbox(self):
        self.listbox.delete(0,ti.END)
        for path in self.programs:
            name=os.path.basename(path)
            self.listbox.insert(ti.END,name)
    def add_program(self):
        filepath=filedialog.askopenfilename(title="select program")
        if filepath:
            self.programs.append(filepath)
            self.update_listbox()
            self.save_programs()
    def run_program(self):
        select=self.listbox.curselection()
        if select:
            index=select[0]
            try:
                subprocess.Popen(self.programs[index],shell=True)
            except Exception as exc:
                messagebox.showerror("error",f"failed run:\n{exc}")

        else:
            messagebox.showinfo("info","select program")
    def delete_program(self):
        select=self.listbox.curselection()
        if select:
            index=select[0]
            del self.programs[index]
            self.update_listbox()
            self.save_program()
        else:
            messagebox.showinfo('info',"select delete")
    def load_program(self):
        if os.path.exists(file):
            try:
                with open(file,'r') as f:
                    self.programs=json.load(f)
            except json.JSONDecodeError:
                messagebox.showwarning('warning',"program.json is corrupted. Resetting.")
                self.programs=[]
            self.update_listbox()
    def save_program(self):
        with open(file,"w") as f:
            json.dump(self.programs,f,indent=2)
if __name__=="__main__":
    root=ti.Tk()
    app=Launchers(root)
    root.mainloop()