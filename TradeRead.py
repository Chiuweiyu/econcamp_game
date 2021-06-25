import pygsheets
import pandas as pd
import os
import tkinter
from tkinter import filedialog

def save():
    currdir = os.getcwd()
    tempdir = filedialog.asksaveasfilename(initialdir = currdir, title = "", initialfile = "交易", defaultextension='.txt', filetypes= (("csv files", ".csv"), ("All files", "*.*")))
    return tempdir

gc = pygsheets.authorize(service_account_file = "econcamp.json")

survey_url = 'https://docs.google.com/spreadsheets/d/1D-Ih2IWxx0-F8mlRAy89BpPBH6CBsnFfuUgaa7w5zPI/'
sh = gc.open_by_url(survey_url).sheet1
df = pd.DataFrame(sh.get_all_values())
df = df.iloc(1)[1:8]
start = 1

while(True):
    if df.iloc[start][1] == "":
        start += 1
    else:
        break
df = df.iloc[start:start+10]
df = df.rename(columns={1:"ID",2:"netBuyFood",3: "netBuySi",4: "netBuyNi",5:"netBuyRa", 6: "netBuyCo", 7: "netBuyCr"})
df.index = [0,1,2,3,4,5,6,7,8,9]

root = tkinter.Tk()
root.withdraw() #use to hide tkinter window
df.to_csv(save(), sep= ",", index = False, encoding="utf_8_sig")


