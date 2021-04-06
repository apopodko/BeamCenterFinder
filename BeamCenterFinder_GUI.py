from tkinter import Label, Button, StringVar, DoubleVar, IntVar, Tk, filedialog
from tkinter.ttk import Entry
from tkinter import messagebox
import BeamCenterFinder as bm

class Root(Tk):
    
    def __init__(self):
        super(Root, self).__init__()
        self.title("Beam Center Finder")
        self.minsize(500, 250)

        def load_dir():
            f = filedialog.askdirectory()
            self.img_dir.set(f)
            
        def about():
            #lines = []
            messagebox.showinfo(title='About', message='BeamCenterFinder is a script based on the article: "Beam focal spot position: The forgotten linac QA parameter. An EPID-based phantomless method for routine Stereotactic linac QA" by Jacek M. Chojnowski et al. The idea is to find the actual position of the beam focal spot using different distances from target to X, Y jaws and MLC. \n\nMIT License \nCopyright (c) 2021 Alexey Popodko')   
        
        def beam_center():
            if not self.img_dir.get():
                self.results.set('Please choose a directory')
            else:
                res = bm.findcenter(PathDicom= self.img_dir.get(), Depi= self.Depi.get(), 
                                Djaw= [self.DjawX.get(), self.DjawY.get()], Dmlc= self.Dmlc.get(), ResF= self.RszF.get())
                self.results.set(res)

        self.img_dir = StringVar()
        self.Depi = DoubleVar(value=100.0)
        self.Dmlc = DoubleVar(value=49.0)
        self.DjawX = DoubleVar(value=40.6)
        self.DjawY = DoubleVar(value=31.9)
        self.RszF = IntVar(value=10)
        self.results = StringVar()
        Label(text='Load Directory with DICOM images').grid(column=1, columnspan=3, row=0, pady=5, sticky='we')
        Button(text='Load Directory...', command=load_dir).grid(column=2, row=1, pady=5)
        Label(textvariable=self.img_dir).grid(column=0, columnspan=5, row=2, pady=5, sticky='we')
        Label(text='Distance to EPID:').grid(column=0, row=3, padx=5)
        Entry(width=7, textvariable=self.Depi).grid(column=0, row=4)
        Label(text='Distance to MLC:').grid(column=1, row=3)
        Entry(width=7, textvariable=self.Dmlc).grid(column=1, row=4)
        Label(text='Resize factor:').grid(column=2, row=3)
        Entry(width=7, textvariable=self.RszF).grid(column=2, row=4)
        Label(text='Distance to X Jaws:').grid(column=3, row=3)
        Entry(width=7, textvariable=self.DjawX).grid(column=3, row=4)
        Label(text='Distance to Y Jaws:').grid(column=4, row=3, padx=5)
        Entry(width=7, textvariable=self.DjawY).grid(column=4, row=4)
        Button(text='Analyze', command=beam_center).grid(column=2, row=5, pady=10)
        Label(text='Calculated shift at target level [x,y] mm:').grid(column=1, columnspan=3, row=6, sticky='we')
        Label(textvariable=self.results).grid(column=1, columnspan=3, row=7, pady=5, sticky='we')
        Button(text='About', command=about).grid(column=4, row=0, sticky='e', padx=5, pady=5)

        
def if_exit():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.quit()

root = Root()
root.protocol("WM_DELETE_WINDOW", if_exit)
root.mainloop()
root.destroy()
del root