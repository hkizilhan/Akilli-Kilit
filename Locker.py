import hashlib, time
from winreg import *
import tkinter as tk

DEBUG=True

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

def get_usb_key():
    key_name = ""
    key_data = ""
    
    try:
        f=open("E:/TCNO.txt", encoding="utf-8")
        key_name = f.readline().splitlines()[0]
        key_data = f.readline().splitlines()[0]
        f.close()
        
    except:
        return (None, None)
    
    return (key_name, key_data)
    

def generate_key(input_str = ""):
    ser = get_usb_serial()
    
    KEY = hashlib.sha256()
    KEY.update(ser.encode('utf-8'))
    KEY.update(input_str.encode('utf-8'))
    
    return KEY.hexdigest()
    


class Locker_Window():

    def __init__(self, root=None):
        self.root=root
        self.root.wm_attributes("-topmost", 1) # Always on top
        self.root.geometry("800x600")
        self.root.config(bg="red")

        self.state = False
        self.visible = True

        if DEBUG:
            # Testing
            self.root.bind("<F11>", lambda state:self.set_fullscreen(state=True))
            self.root.bind("<Escape>", lambda state:self.set_fullscreen(state=False))
        else:
            # Production
            self.root.protocol("WM_DELETE_WINDOW", self.shutdown)

            self.set_fullscreen(state=True)

        
        self.root.after(3000, self.timer)

    def set_fullscreen(self, state=True):
        self.root.attributes("-fullscreen", state)
        return "break"

    def timer(self):
        self.check_usb()
        
        self.root.after(5000, self.timer)

    def lock(self):
        self.root.deiconify()

    def unlock(self):
        self.root.withdraw()


    def check_usb(self):
        k_name, k_data = get_usb_key()
        
        if k_name == None:
            print("LOCKED")
            self.lock()
            return False

        key=generate_key(k_name)

        if key == k_data:
            print("MATCH DETECTED, UNLOCK")
            self.unlock()
            
        else:
            print("LOCKED")
            self.lock()
            


    def shutdown(self):
        self.root.bell()
    

if __name__ == '__main__':
    root = tk.Tk()
    app = Locker_Window(root=root)
    root.mainloop()
