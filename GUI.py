import hashlib, time
from tkinter import *
from tkinter import ttk
from winreg import *

VERSION=0.02

def get_usb_serial():
    Registry = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    RawKey = OpenKey(Registry, "SYSTEM\CurrentControlSet\Services\disk\Enum")

    try:
        i = 0
        while 1:
            name, value, k_type = EnumValue(RawKey, i)
            i += 1
            
            if k_type == 1 and name != '0':
                #print (value)
                return value
            
    except WindowsError:
        pass
        
    return value
    
    
def generate_key(input_str = ""):
    ser = get_usb_serial()
    
    KEY = hashlib.sha256()
    KEY.update(ser.encode('utf-8'))
    KEY.update(input_str.encode('utf-8'))
    
    return KEY.hexdigest()
    


class App():
    
    def __init__(self, root):
        
        # GUI init *********************
        
        root.minsize(500,400)
        #root.maxsize(500,400)
        root.resizable(False, False)
        
        x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
        y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
        root.geometry("+%d+%d" % (x, y))
        

        Title = root.title( "ET USB Hazırlayıcı - Hakan KIZILHAN - " + str(VERSION))

        for i in range(5):
            root.columnconfigure(i, weight=1)
            root.rowconfigure   (i, weight=1)

        self.label1 = ttk.Label(root, text ="ET USB Hazırlayıcı    -    Yazan:  Hakan KIZILHAN", foreground="blue", font=("Helvetica", 16))
        self.label1.grid(row=0, column=0, columnspan=5, sticky=E+W)

        self.lblAdSoyad = ttk.Label(root, text="Ad Soyad")
        self.lblAdSoyad.grid(row=1, column=0)
                
        self.lblTC = ttk.Label(root, text="TC No")
        self.lblTC.grid(row=2, column=0)

        self.lblHarf = ttk.Label(root, text="Sürücü Harfi")
        self.lblHarf.grid(row=3, column=0)

        
        self.txtAdSoyad = ttk.Entry(root, textvariable="")
        self.txtAdSoyad.grid(row=1, column=1, columnspan=1, sticky=E+W)
        
        self.txtTC      = ttk.Entry(root, textvariable="")
        self.txtTC      .grid(row=2, column=1, columnspan=1, sticky=E+W)
        
        self.txtHarf      = ttk.Entry(root, textvariable="")
        self.txtHarf      .grid(row=3, column=1, columnspan=1, sticky=E+W)
        

        self.btnTemizle = ttk.Button(root, text='Temizle', command=self.btn_Temizle).grid(row=4, column=0)
        self.btnKaydet  = ttk.Button(root, text='Kaydet',  command=self.btn_Kaydet).grid(row=4, column=1)

        self.lstOutput  = Listbox(root, height=6)
        self.lstOutput.grid(row=6, column=0, columnspan=5, sticky=E+W)        
        
        # ******************************************
        
        self.Output_Add(get_usb_serial())
        self.txtAdSoyad.focus()
        
    
    def btn_Temizle(self):
        self.txtAdSoyad.delete(0, END)
        self.txtTC     .delete(0, END)
        self.txtHarf   .delete(0, END)
        
        self.lstOutput .delete(0, END)
        self.Output_Add(get_usb_serial())
    

    def btn_Kaydet(self):
        Adsoyad = self.txtTC.get() + " " + self.txtAdSoyad.get()
        self.Output_Add(Adsoyad)
        
        key = generate_key(Adsoyad)
        
        self.Output_Add( key )
        
        path = self.txtHarf.get() + ":/TCNO.txt"
        
        keyfile = open(path, "w", encoding="utf-8")
        
        keyfile.write(Adsoyad + "\n")
        keyfile.write(key)
        
        keyfile.close()


    def Output_Add(self, text):
        self.lstOutput.insert(END, text)



root = Tk()
app = App(root)
root.mainloop()
