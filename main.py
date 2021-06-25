import os
import tkinter
from tkinter import filedialog
from Universe import read_csv_to_gamedata, read_csv_to_historydata
from tkinter import messagebox
import exogenous as ex


def produce_upgrade():
    os.system("python produce_upgrade.py")

def trade():
    os.system("python trade.py")

def producitonRead():
    os.system("python ProductionRead.py")

def tradeRead():
    os.system("python TradeRead.py")

def uploadGameData():
    root = tkinter.Tk()
    root.withdraw()
    currdir = os.getcwd()
    tempdir = filedialog.askopenfilename(parent = root, initialdir = currdir, title = "上傳gameData檔案", filetypes = (("Data files", ["*.csv*",]), ("All files", "*.*")))
    read_csv_to_gamedata(tempdir)

def uploadHistoryData():
    root = tkinter.Tk()
    root.withdraw()
    currdir = os.getcwd()
    tempdir = filedialog.askopenfilename(parent = root, initialdir = currdir, title = "上傳hostoryData檔案", filetypes = (("Data files", ["*.csv*",]), ("All files", "*.*")))
    read_csv_to_historydata(tempdir)

def multipleResource(event):
    id = int(entry_ID1.get())
    mul = int(entry_multiplier.get())
    ex.multipleResource(id, mul)

def techUpgrade(event):
    id = int(entry_ID2.get())
    ex.techUpgrade(id)

def addMoney(event):
    id = entry_IDList.get()
    id = id.split()
    id = [int(i) for i in id]
    money = entry_moneyList.get()
    money = money.split()
    money = [int(i) for i in money]
    ex.addMoney(id, money)

def actionDeductMoney(event):
    id = int(entry_ID3.get())
    money = int(entry_money.get())
    ex.actionDeductMoney(id, money)

def addResource(event):
    id = int(entry_ID4.get())
    res = entry_resList.get()
    res = res.split()
    res = [int(i) for i in res]
    ex.addResource(id, food = res[0], Si = res[1], Ni = res[2], Ra = res[3], Co = res[4], Cr = res[5])

def addPopulation(event):
    id = int(entry_ID5.get())
    popu = int(entry_popu.get())
    ex.addPopulation(id, popu)


def quitGame():
    ans = messagebox.askyesno(title = "Warning", message = "  Quit the Game ?")
    if ans:
        window.quit()
    else:
        return None


window = tkinter.Tk()
window.attributes('-alpha', 0.95)
window.protocol('WM_DELETE_WINDOW', quitGame)
window.title("台大經濟營營包遊戲")
window.geometry("600x800")

if __name__=="__main__":

    modeOne = tkinter.Button(window,text="生產、升級、製造",font = ("微軟正黑體",16), width=20, height=1, command = produce_upgrade, bg = "#2e75b6" ,fg = "white")
    modeOne.place(relx=0.45, rely=0.07, anchor=tkinter.CENTER)
    
    m1download = tkinter.Button(window,text = "↓", font = ("微軟正黑體", 10), width = 3, height = 1, command = producitonRead, bg = "#2e75b6",fg = "white")
    m1download.place(relx=0.80, rely=0.07, anchor=tkinter.CENTER)
  
    modeTwo = tkinter.Button(window,text= "貿易",font = ("微軟正黑體",16), width=20, height=1, command = trade, bg = "#137197", fg = "white") 
    modeTwo.place(relx=0.45, rely=0.16, anchor=tkinter.CENTER)

    m2download = tkinter.Button(window,text="↓",font = ("微軟正黑體",10), width=3, height=1, command = tradeRead, bg = "#137197", fg = "white") 
    m2download.place(relx=0.80, rely=0.16, anchor=tkinter.CENTER)

    gdupload = tkinter.Button(window,text = "上傳gameData檔案", font = ("微軟正黑體", 11), width = 16, height = 1, command = uploadGameData, bg = "#239437",fg = "white")
    gdupload.place(relx=0.33, rely=0.24, anchor=tkinter.CENTER)

    hdupload = tkinter.Button(window,text = "上傳hostoryData檔案", font = ("微軟正黑體", 11), width = 16, height = 1, command = uploadHistoryData, bg = "#28b128",fg = "white")
    hdupload.place(relx=0.67, rely=0.24, anchor=tkinter.CENTER)

    # for multipleResource
    label1 = tkinter.Label(window, text = '................................................................................................................................................\n資源倍增',font = ("微軟正黑體",12))
    label1.place(relx=0.5, rely=0.30, anchor=tkinter.CENTER)

    Text_ID1 = tkinter.Label(window,text = "編號", font = ("微軟正黑體", 12))
    Text_ID1.place(relx=0.12, rely=0.35, anchor=tkinter.CENTER)
    Text_multiplier = tkinter.Label(window,text = "倍數", font = ("微軟正黑體", 12))
    Text_multiplier.place(relx=0.37, rely=0.35, anchor=tkinter.CENTER)
    str_ID1 = tkinter.StringVar()
    
    str_multiplier = tkinter.StringVar()

    entry_ID1 = tkinter.Entry(window, width=7, textvariable = str_ID1)
    entry_ID1.place(relx=0.22, rely=0.35, anchor=tkinter.CENTER)
    entry_multiplier = tkinter.Entry(window, width=7, textvariable = str_multiplier)
    entry_multiplier.place(relx=0.47, rely=0.35, anchor=tkinter.CENTER)
    
    button_multipleResource = tkinter.Button(window,text = "RUN", font = ("微軟正黑體", 8), width = 10, height = 1)
    button_multipleResource.place(relx=0.78, rely=0.34, anchor=tkinter.CENTER)
    button_multipleResource.bind("<Button-1>",multipleResource)

    # for techUpgrade
    label2 = tkinter.Label(window, text = '................................................................................................................................................\n技術升級',font = ("微軟正黑體",12))
    label2.place(relx=0.5, rely=0.40, anchor=tkinter.CENTER)

    Text_ID2 = tkinter.Label(window,text = "編號", font = ("微軟正黑體", 12))
    Text_ID2.place(relx=0.195, rely=0.45, anchor=tkinter.CENTER)
    str_ID2 = tkinter.StringVar()

    entry_ID2 = tkinter.Entry(window, width=20, textvariable = str_ID2)
    entry_ID2.place(relx=0.45, rely=0.45, anchor=tkinter.CENTER)

    button_techUpgrade = tkinter.Button(window,text = "RUN", font = ("微軟正黑體", 8), width = 10, height = 1)
    button_techUpgrade.place(relx=0.78, rely=0.44, anchor=tkinter.CENTER)
    button_techUpgrade.bind("<Button-1>" ,techUpgrade)

    # for addMoney
    label3 = tkinter.Label(window, text = '................................................................................................................................................\n金錢增加',font = ("微軟正黑體",12))
    label3.place(relx=0.5, rely=0.497, anchor=tkinter.CENTER)

    Text_IDList = tkinter.Label(window,text = "編號列表", font = ("微軟正黑體", 12))
    Text_IDList.place(relx=0.17, rely=0.527, anchor=tkinter.CENTER)
    Text_moneyList = tkinter.Label(window,text = "欲增加金額列表（循上列編號列表排序，以空白鍵隔開）", font = ("微軟正黑體", 10))
    Text_moneyList.place(relx=0.405, rely=0.595, anchor=tkinter.CENTER)
    str_IDList = tkinter.StringVar()
    str_moneyList = tkinter.StringVar()

    entry_IDList = tkinter.Entry(window, width=45, textvariable = str_IDList)
    entry_moneyList = tkinter.Entry(window, width=45, textvariable = str_moneyList)
    entry_IDList.place(relx=0.40, rely=0.555, anchor=tkinter.CENTER)
    entry_moneyList.place(relx=0.40, rely=0.625, anchor=tkinter.CENTER)
    
    button_addMoney = tkinter.Button(window,text = "RUN", font = ("微軟正黑體", 8), width = 8, height = 2)
    button_addMoney.place(relx=0.87, rely=0.58, anchor=tkinter.CENTER)
    button_addMoney.bind("<Button-1>", addMoney)
    

    # for actionDeductMoney
    label4 = tkinter.Label(window, text = '................................................................................................................................................\n競標扣除',font = ("微軟正黑體",12))
    label4.place(relx=0.5, rely=0.68, anchor=tkinter.CENTER)

    Text_ID3 = tkinter.Label(window,text = "編號", font = ("微軟正黑體", 12))
    Text_ID3.place(relx=0.12, rely=0.73, anchor=tkinter.CENTER)
    Text_money = tkinter.Label(window,text = "金額", font = ("微軟正黑體", 12))
    Text_money.place(relx=0.37, rely=0.73, anchor=tkinter.CENTER)
    str_ID3 = tkinter.StringVar()
    str_money = tkinter.StringVar()

    entry_ID3 = tkinter.Entry(window, width=7, textvariable = str_ID3)
    entry_money = tkinter.Entry(window, width=7, textvariable = str_money)
    entry_ID3.place(relx=0.22, rely=0.73, anchor=tkinter.CENTER)
    entry_money.place(relx=0.47, rely=0.73, anchor=tkinter.CENTER)
    
    button_multipleResource = tkinter.Button(window,text = "RUN", font = ("微軟正黑體", 8), width = 10, height = 1)
    button_multipleResource.place(relx=0.78, rely=0.72, anchor=tkinter.CENTER)
    button_multipleResource.bind("<Button-1>",actionDeductMoney)

    # for addResource
    label5 = tkinter.Label(window, text = '................................................................................................................................................\n資源增加',font = ("微軟正黑體",12))
    label5.place(relx=0.5, rely=0.78, anchor=tkinter.CENTER)

    Text_ID4 = tkinter.Label(window,text = "ID", font = ("微軟正黑體", 12))
    Text_ID4.place(relx=0.08, rely=0.81, anchor=tkinter.CENTER)
    Text_resList = tkinter.Label(window,text = "(F S N R Co Cr)", font = ("微軟正黑體", 11))
    Text_resList.place(relx=0.15, rely=0.85, anchor=tkinter.CENTER)
    str_ID4 = tkinter.StringVar()
    str_resList = tkinter.StringVar()

    entry_ID4 = tkinter.Entry(window, width=5, textvariable = str_ID4)
    entry_resList = tkinter.Entry(window, width=36, textvariable = str_resList)
    entry_ID4.place(relx=0.16, rely=0.81, anchor=tkinter.CENTER)
    entry_resList.place(relx=0.55, rely=0.85, anchor=tkinter.CENTER)
    
    button_addMoney = tkinter.Button(window,text = "RUN", font = ("微軟正黑體", 8), width = 5, height = 1)
    button_addMoney.place(relx=0.90, rely=0.832, anchor=tkinter.CENTER)
    button_addMoney.bind("<Button-1>", addResource)

    # for addPopulation
    label6 = tkinter.Label(window, text = '................................................................................................................................................\n人口增加',font = ("微軟正黑體",12))
    label6.place(relx=0.5, rely=0.91, anchor=tkinter.CENTER)

    Text_ID5 = tkinter.Label(window,text = "編號", font = ("微軟正黑體", 12))
    Text_ID5.place(relx=0.12, rely=0.96, anchor=tkinter.CENTER)
    Text_popu = tkinter.Label(window,text = "人數", font = ("微軟正黑體", 12))
    Text_popu.place(relx=0.37, rely=0.96, anchor=tkinter.CENTER)
    str_ID5 = tkinter.StringVar()
    str_popu = tkinter.StringVar()

    entry_ID5 = tkinter.Entry(window, width=7, textvariable = str_ID5)
    entry_popu = tkinter.Entry(window, width=7, textvariable = str_popu)
    entry_ID5.place(relx=0.22, rely=0.96, anchor=tkinter.CENTER)
    entry_popu.place(relx=0.47, rely=0.96, anchor=tkinter.CENTER)
    
    button_multipleResource = tkinter.Button(window,text = "RUN", font = ("微軟正黑體", 8), width = 10, height = 1)
    button_multipleResource.place(relx=0.80, rely=0.958, anchor=tkinter.CENTER)
    button_multipleResource.bind("<Button-1>", addPopulation)


    window.mainloop()



    #exit = tkinter.Button(window,text="關閉程式",font = ("微軟正黑體",10), width=7, height=1 ,command = quitGame, bg = "red2", fg = "white")
   # exit.place(relx=0.93, rely=0.94, anchor=tkinter.CENTER)
    
    
    

