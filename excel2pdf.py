# Import Module
import base64
import os

from win32com import client
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import shutil
from icon import  image


def transfile(f):
    # Open Microsoft Excel
    excel = client.Dispatch("Excel.Application")

    print('open file name is', f)
    # Read Excel File
    sheets = excel.Workbooks.Open(f)
    fname = os.path.splitext(f)[0]
    if os.path.exists(fname):
        shutil.rmtree(fname)
    os.mkdir(fname)
    logmsg("\nCreate dir: {}".format(fname))
    # print(dir(sheets))
    for idx, sheet in enumerate(sheets.Worksheets, 1):
        # print(dir(i))
        # print("name   ", i.name, i)

        # i.PageSetup.Orientation = 90#Microsoft.Office.Interop.Excel.XlPageOrientation.xlLandscape
        # print('hello', type(i.PageSetup.Orientation))
        sheet.PageSetup.Orientation = 2
        sheet.PageSetup.Zoom = False
        sheet.PageSetup.FitToPagesWide = 1
        sheet.PageSetup.FitToPagesTall = False

        dstfie = os.path.join(fname, sheet.name + ".pdf")
        print('sheet name is ', sheet.name)
        print('dst file is ', dstfie)
        sheet.ExportAsFixedFormat(0, dstfie)

        logmsg("\ntrans sheet {:02d}: {}".format(idx, sheet.name))
    return 0


def logmsg(msg):
    logtext.insert(END, msg)
    logtext.see(END)
    tk.update_idletasks()


def openfiles():
    f = filedialog.askopenfilenames(filetypes=[("XLSX", ".xlsx")])
    if f:
        filelistbox.delete(0, END)
        filelistbox.insert(0, *f)


def opendir():
    d = filedialog.askdirectory()
    if d:
        fs = os.listdir(d)
        fs = [os.path.join(d, i) for i in fs if i.endswith(".xlsx")]
        filelistbox.delete(0, END)
        filelistbox.insert(0, *fs)


def begintrans():
    fs = filelistbox.curselection()
    if fs:
        for f in [filelistbox.get(i) for i in fs]:
            f = os.path.abspath(f)
            logtext.insert(END, "\n------- begin trans {}------".format(f))
            transfile(f)
            logtext.insert(END, "\n------- end   trans {}------\n".format(f))
    else:
        messagebox.showinfo("Select file", "Please select at least one file begin to trans")

def trans_icon_to_py(f):
    with open(f,'rb') as x:
        b64str = base64.b64encode(x.read())
        data = "image = %s" % b64str
        with open("icon.py",'w+') as w:
            w.write(data)

def trans_py_to_icon(picname,img):
    pic = open(picname, "wb+")
    pic.write(base64.b64decode(img))
    pic.close()

if __name__ == '__main__':
    print("hello")
    # trans_icon_to_py(r"icon\excel2pdf.ico")
    tk = Tk()
    tk.geometry('800x800')
    tk.title("Sheet2pdf  (EMZ.1.0.6)")

    trans_py_to_icon("s2p.ico", image)
    tk.iconbitmap('s2p.ico')
    pw = PanedWindow(tk, orient="vertical")

    btnframe = Frame(pw)
    btnOpenFile = ttk.Button(btnframe, text="Open Files", command=openfiles)
    btnOpenDir = ttk.Button(btnframe, text="Open Dir", command=opendir)
    btnTrans = ttk.Button(btnframe, text="Begin Trans", command=begintrans)
    btnOpenFile.pack(side='left')
    btnOpenDir.pack(side='left')
    btnTrans.pack(side='left')

    filelistbox = Listbox(pw, selectmode=EXTENDED)
    filelistbox.bind('<Double-Button-1>', lambda x: begintrans())
    logtext = Text(pw)

    pw.pack(fill='both', expand=True)
    pw.add(btnframe)
    pw.add(filelistbox)
    pw.add(logtext)
    #
    # btnframe.pack(side='top', fill='x')
    # filelistbox.pack(fill='x')
    # logtext.pack(fill='both', expand=True)

    tk.mainloop()
