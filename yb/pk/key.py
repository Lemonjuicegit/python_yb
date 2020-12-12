import m1.IoFile as iof
import tkinter as tk

iofile = iof.IoFile()
integer = iofile.key()

tkinter = tk.Tk()

entry = tk.Entry(tkinter)
entry.insert(0,str(integer))
entry.grid()
tk.mainloop()






