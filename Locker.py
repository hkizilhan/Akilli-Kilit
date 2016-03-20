import hashlib, time
from winreg import *
from subprocess import call
import tkinter as tk

DEBUG=False

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
        f=open("D:/TCNO.txt", encoding="utf-8")
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

        self.check_seconds = 5000 # check every 5 secons
        self.shutdown_seconds = 0
        self.shutdown_seconds_limit = 25
        
        self.state = False
        self.visible = True

        if DEBUG:
            # Testing
            self.root.bind("<F11>", lambda state:self.set_fullscreen(state=True))
            self.root.bind("<Escape>", lambda state:self.set_fullscreen(state=False))
        else:
            # Production
            self.root.protocol("WM_DELETE_WINDOW", self.close_request)
            self.set_fullscreen(state=True)

        self.main_timer_id = self.root.after(self.check_seconds, self.main_timer)

    def set_fullscreen(self, state=True):
        self.root.attributes("-fullscreen", state)
        return "break"

    def main_timer(self):
        key_present = self.check_usb()
        if key_present:
            self.unlock()
            self.shutdown_seconds = 0
        else:
            self.lock()
            self.shutdown_seconds += (self.check_seconds / 1000)
            if self.shutdown_seconds > self.shutdown_seconds_limit:
                # shutdown limit passed, shutdown computer
                self.shutdown()
        
        self.main_timer_id = self.root.after(self.check_seconds, self.main_timer)
        # self.root.after_cancel(after_id)

    def lock(self):
        self.root.deiconify()

    def unlock(self):
        self.root.withdraw()

    def check_usb(self):
        k_name, k_data = get_usb_key()
        
        if k_name == None:
            print("LOCKED")
            return False

        key=generate_key(k_name)
        if key == k_data:
            print("MATCH DETECTED, UNLOCK")
            return True
        else:
            print("LOCKED")
            return False
            
    def close_request(self):
        pass

    def shutdown(self):
        self.root.bell()
        print("BYE...")
        if DEBUG:
            self.root.quit()
        else:
            call(["shutdown", "-s", "-t", "0"])

if __name__ == '__main__':
    root = tk.Tk()
    app = Locker_Window(root=root)
    root.mainloop()
