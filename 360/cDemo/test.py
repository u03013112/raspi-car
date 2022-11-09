import ctypes
dll = ctypes.cdll.LoadLibrary
lib = dll('./test.so') 
lib.foo(1, 3)


import ctypes
dll = ctypes.cdll.LoadLibrary
lib = dll('./test++.so') 
lib.display()
lib.display_int(0)
