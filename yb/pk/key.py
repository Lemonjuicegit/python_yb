# import tkinter as tk
import socket
def getkey():
    name = socket.gethostname()
    ip = socket.gethostbyname(name)
    k = 1
    n = 0
    while n < len(ip):
        try:
            k = k * ord(name[n]) + ord(ip[n])
            n += 1
        except IndexError:
            break
    return k

# integer = getkey()
#
# tkinter = tk.Tk()
#
# entry = tk.Entry(tkinter)
# entry.insert(0,str(integer))
# entry.grid()
# tk.mainloop()






