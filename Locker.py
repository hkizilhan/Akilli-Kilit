import hashlib, time, subprocess
from winreg import *
import tkinter as tk

DEBUG=True
SHUTDOWN_SECONDS_LIMIT = 30
DELAYED_SHUTDOWN_SECONDS_LIMIT = 900
CHECK_SECONDS = 5000 # ms
DELAY_BUTTON_COUNTER_START = 5

# No cable
#   Medya Durumu  . . . . . . . . . . : Medya Bağlantısı kesildi
#print(lines[6])  # check for "kesildi" keyword
def check_cable_connected():
    msg = subprocess.check_output("ipconfig", shell=True)
    msg = msg.decode("cp857")
    lines = msg.splitlines()
    if "kesildi" in lines[6]:
        return False
    else:
        return True


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
        self.delay_button = tk.Button(self.root, text="", command=self.delay_button_click)
        
        self.check_seconds = CHECK_SECONDS
        self.shutdown_seconds = 0
        self.shutdown_seconds_limit = SHUTDOWN_SECONDS_LIMIT
        
        self.usb_key_was_plugged=False
        self.delay_button_timer_id=None
        self.delay_button_timer_started=False
        self.delay_button_counter = DELAY_BUTTON_COUNTER_START
        
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
        cable_connected = check_cable_connected()
        
        if key_present and cable_connected:
            print("MATCH DETECTED, UNLOCK")
            self.unlock()
            self.shutdown_seconds = 0
        else:
            if not key_present:
                # Reason = No USB Key
                print("LOCKED - No Usb Present")
                self.lock(reason="no_usb")
            else:
                # Reason = No cable Connected
                print("LOCKED - No Cable Connected")
                self.lock(reason="no_cable")
            
            self.shutdown_seconds += (self.check_seconds / 1000)
            if self.shutdown_seconds > self.shutdown_seconds_limit:
                # shutdown limit passed, shutdown computer
                self.shutdown()
        
        self.main_timer_id = self.root.after(self.check_seconds, self.main_timer)
        # self.root.after_cancel(after_id)

    def lock(self, reason=None):
        self.root.deiconify()
        if reason=="no_usb":
            if self.usb_key_was_plugged:
                if not self.delay_button_timer_started:
                    self.delay_button_timer_started = True
                    self.delay_button_timer()
        

    def unlock(self):
        self.root.withdraw()
        self.usb_key_was_plugged = True
        self.shutdown_seconds_limit = SHUTDOWN_SECONDS_LIMIT

    def check_usb(self):
        k_name, k_data = get_usb_key()
        
        if k_name == None:
            return False

        key=generate_key(k_name)
        if key == k_data:
            return True
        else:
            return False
            
    def delay_button_click(self):
        # Set shutdown 15 minutes later
        self.shutdown_seconds_limit = DELAYED_SHUTDOWN_SECONDS_LIMIT
        
        # Clear counters
        self.delay_button_counter = DELAY_BUTTON_COUNTER_START
        self.delay_button_timer_started = False
        self.delay_button.place_forget()
        self.usb_key_was_plugged=False
        # Disable timer
        self.delay_button.after_cancel(self.delay_button_timer_id)
        
        
    def delay_button_timer(self):
        
        if self.delay_button_counter == DELAY_BUTTON_COUNTER_START:
            # First Run
            self.delay_button.place(relx=.5, rely=.5, height=100, width=150)
        
        self.delay_button['text'] = "15 Dakika Beklet...({})".format(int(self.delay_button_counter))
        
        self.delay_button_counter -= 1
        if self.delay_button_counter < 0:
            # Passed 5 seconds, remove button, reset counters
            self.delay_button_counter = DELAY_BUTTON_COUNTER_START
            self.delay_button_timer_started = False
            self.delay_button.place_forget()
            self.usb_key_was_plugged=False
            return
            
        # Set delay Button timer
        self.delay_button_timer_id = self.delay_button.after(1000, self.delay_button_timer)
    
    def close_request(self):
        pass

    def shutdown(self):
        self.root.bell()
        print("BYE...")
        if DEBUG:
            self.root.quit()
        else:
            subprocess.call(["shutdown", "-s", "-t", "0"])

if __name__ == '__main__':
    root = tk.Tk()
    app = Locker_Window(root=root)
    root.mainloop()
