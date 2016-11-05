python cx_setup_GUI.py build

rmdir /s /q build_GUI\tcl\encoding
rmdir /s /q build_GUI\tcl\http1.0
rmdir /s /q build_GUI\tcl\msgs
rmdir /s /q build_GUI\tcl\opt0.4
rmdir /s /q build_GUI\tcl\tzdata

rmdir /s /q build_GUI\tk\demos
rmdir /s /q build_GUI\tk\images
rmdir /s /q build_GUI\tk\msgs


python cx_setup_locker.py build

rmdir /s /q build_Locker\tcl\encoding
rmdir /s /q build_Locker\tcl\http1.0
rmdir /s /q build_Locker\tcl\msgs
rmdir /s /q build_Locker\tcl\opt0.4
rmdir /s /q build_Locker\tcl\tzdata

rmdir /s /q build_Locker\tk\demos
rmdir /s /q build_Locker\tk\images
rmdir /s /q build_Locker\tk\msgs
