# import tkinter as tk
import socket


class licKey:

    def __init__(self):
        name = socket.gethostname()
        ip = socket.gethostbyname(name)
        self.k = 1
        for n in range(0, len(ip)):
            try:
                self.k = self.k * ord(name[n]) + ord(ip[n])
            except IndexError:
                break

    def lic(self):
        return self.k != 18670669457275772673


if __name__ == '__main__':
    lic = licKey()
    print(lic.k)
    print(lic.lic())

# integer = getkey()
#
# tkinter = tk.Tk()
#
# entry = tk.Entry(tkinter)
# entry.insert(0,str(integer))
# entry.grid()
# tk.mainloop()
