import hashlib, time
from winreg import *


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
        f=open("G:/TCNO.txt", encoding="utf-8")
        key_name = f.readline().splitlines()[0]
        key_data = f.readline().splitlines()[0]
        f.close()
        
    except:
        return None
    
    return (key_name, key_data)
    

def generate_key(input_str = ""):
    ser = get_usb_serial()
    
    KEY = hashlib.sha256()
    KEY.update(ser.encode('utf-8'))
    KEY.update(input_str.encode('utf-8'))
    
    return KEY.hexdigest()
    


try:
    while True:
        k_name, k_data = get_usb_key()
        
        key=generate_key(k_name)
        
        print(key)
        print(k_data)
        
        if key == k_data:
            print("MATCH DETECTED, UNLOCK")
        else:
            print("LOCKED")
        
        
        
        time.sleep(1)


except KeyboardInterrupt:
    pass
