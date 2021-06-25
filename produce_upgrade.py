import Universe
import pandas as pd
import numpy as np
import eq_table as et
import os
from exogenous import starvation

pd.set_option('display.max_columns', None)
np.seterr(invalid='ignore') #to ignore "RuntimeWarning: invalid value encountered" error
import tkinter
from tkinter import filedialog
root = tkinter.Tk()
root.withdraw() #use to hide tkinter window
def search_for_file_path(message = "Please select a file"):
    currdir = os.getcwd()
    tempdir = filedialog.askopenfilename(parent = root, initialdir = currdir, title = message, filetypes = (("Data files", ["*.csv*",]), ("All files", "*.*")))
    return tempdir


historyName = search_for_file_path("讀取狀態")
inputName = search_for_file_path("讀取輸入資料")


history = Universe.read(historyName)
currentRound = int(history["Round"][0]) + 1
history["Round"] = [currentRound]*10
inputdata = pd.read_csv(inputName)
#inputdata = et.modifyProductionInput(inputdata)
inputdata["ID"] = [int(i) for i in inputdata["ID"]]
inputdata = inputdata.sort_values(by="ID")
inputdata.index = [0,1,2,3,4,5,6,7,8,9]

log = []
if os.path.exists(f"Round{currentRound}") == False:
    os.mkdir(f"Round{currentRound}")
for i in range(10):
    log.append(open(f"Round{currentRound}\\{i+1}_section1_log.txt","w"))

remain_avl_popu = list(history["available_popu"]) # reamin available population
tech = history["tech"] #technology of every team

food = [0]*10 # new-production food
Si = [0]*10   # new-production Si
Ni = [0]*10   # new-production Ni
Ra = [0]*10   # new-production Ra
Co = [0]*10   # new-production Co
Cr = [0]*10   # new-production Cr


for i in range(10): # for 10 teams
    advantage = et.advantageForTeam[i]  # what advantages this team has
    print(f"第{i+1}小隊生產優勢： {advantage}\n剩餘可動用人口：{remain_avl_popu[i]}", file = log[i])
    if remain_avl_popu[i]:  # for food production
        valid_LoF = min(inputdata["labor_on_food"][i], remain_avl_popu[i])
        food[i] = round(et.foodProduction(valid_LoF))
        remain_avl_popu[i] = max(remain_avl_popu[i] - valid_LoF, 0)
    print(f"  生產食物：{food[i]}，剩餘可動用人口：{remain_avl_popu[i]}", file = log[i])

    if remain_avl_popu[i]:  # for Si production
        A = et.advantageRatio if "Si" in advantage else 1
        valid_LoSi = min(inputdata["labor_on_Si"][i], remain_avl_popu[i])
        Si[i] = round(et.elementProduction(A, tech[i], valid_LoSi))
        remain_avl_popu[i] = max(remain_avl_popu[i]-valid_LoSi, 0)
    print(f"  生產矽：{Si[i]}，剩餘可動用人口：{remain_avl_popu[i]}", file = log[i])
    
    if remain_avl_popu[i]:  # for Ni production
        A = et.advantageRatio if "Ni" in advantage else 1
        valid_LoNi = min(inputdata["labor_on_Ni"][i], remain_avl_popu[i])
        Ni[i] = round(et.elementProduction(A, tech[i], valid_LoNi))
        remain_avl_popu[i] = max(remain_avl_popu[i]-valid_LoNi, 0)
    print(f"  生產鎳：{Ni[i]}，剩餘可動用人口：{remain_avl_popu[i]}", file = log[i])
    
    if remain_avl_popu[i]:  # for Ra production
        A = et.advantageRatio if "Ra" in advantage else 1
        valid_LoRa = min(inputdata["labor_on_Ra"][i], remain_avl_popu[i])
        Ra[i] = round(et.elementProduction(A, tech[i], valid_LoRa))
        remain_avl_popu[i] = max(remain_avl_popu[i]-valid_LoRa, 0)
    print(f"  生產鐳：{Ra[i]}，剩餘可動用人口：{remain_avl_popu[i]}", file = log[i])

    if remain_avl_popu[i]:  # for Co production
        A = et.advantageRatio if "Co" in advantage else 1
        valid_LoCo = min(inputdata["labor_on_Co"][i], remain_avl_popu[i])
        Co[i] = round(et.elementProduction(A, tech[i], valid_LoCo))
        remain_avl_popu[i] = max(remain_avl_popu[i]-valid_LoCo, 0)
    print(f"  生產鈷：{Co[i]}，剩餘可動用人口：{remain_avl_popu[i]}", file = log[i])

    if remain_avl_popu[i]:  # for Cr production
        A = et.advantageRatio if "Cr" in advantage else 1
        valid_LoCr = min(inputdata["labor_on_Cr"][i], remain_avl_popu[i])
        Cr[i] = round(et.elementProduction(A, tech[i], valid_LoCr))
        remain_avl_popu[i] = max(remain_avl_popu[i]-valid_LoCr, 0)
    print(f"  生產鉻：{Cr[i]}，剩餘可動用人口：{remain_avl_popu[i]}", file = log[i])
    print("", file = log[i])



history["food"] += food
history["Si"] += Si
history["cumSi"] += Si
history["Ni"] += Ni
history["cumNi"] += Ni
history["Ra"] += Ra
history["cumRa"] += Ra
history["Co"] += Co
history["cumCo"] += Co
history["Cr"] += Cr
history["cumCr"] += Cr
# end of production

for i in range(10):
    print(f"第{i+1}小隊目前累積資源：food, [Si, Ni, Ra, Co, Cr] = {history.iloc[i][3]}, {list(history.iloc[i][6:11])}", file = log[i])
    print("", file = log[i])

# start for upgrade
upgradeDemand = list(inputdata["upgrade_input"])
for i in range(10):
    seriesData = history.iloc[i]
    invertory = list(seriesData[6:11])
    upgradeDemand[i] = str(upgradeDemand[i]).split()
    upgradeDemand[i] = [int(j) for j in upgradeDemand[i]]
    print(f"第{i+1}小隊升級投入: {upgradeDemand[i]} \n目前等級：{tech[i]}，目前資源：[Si, Ni, Ra, Co, Cr] = {invertory}，剩餘可動用人口：{remain_avl_popu[i]}", file = log[i])
    rsD, popuD, newLv = et.upgrade(tech[i], upgradeDemand[i], remain_avl_popu[i], invertory)
    
    LH = list(seriesData) # List of history
    
    stop = 1
    for j in range(5):
        LH[6+j] -= round(rsD[j])
    remain_avl_popu[i]  -= popuD
    LH[17] = newLv
    history.iloc[i] = LH
    print(f"抵達等級：{newLv}，剩餘資源：[Si, Ni, Ra, Co, Cr] = {LH[6:11]}，剩餘可動用人口：{remain_avl_popu[i]}", file = log[i])
    print("", file = log[i])
# end of upgrade

# start for building
spaceshipDamand = list(inputdata["production_set"])
for i in range(10):
    seriesData = history.iloc[i]
    spaceshipDamand[i] = str(spaceshipDamand[i]).split(" ")
    spaceshipDamand[i] = [ int(j) for j in spaceshipDamand[i] ]
    spaceshipDamand[i] = sorted(spaceshipDamand[i])
    print(f"第{i+1}小隊\n想製造產品：{spaceshipDamand[i]}", file = log[i])
    print(f"目前資源：[Si, Ni, Ra, Co, Cr] = {list(seriesData[6:11])}，剩餘可動用人口：{remain_avl_popu[i]}", file = log[i])
   
    rsD, popuD, output = et.build_spaceship(spaceshipDamand[i],  remain_avl_popu[i], seriesData)
    LH = list(seriesData) # List of history
    
    for j in range(5):
        LH[6+j] -= rsD[j]
    for j in range(10):
        LH[18+j] += output[j]
    history.iloc[i] = LH
    print(f"製造結果：{output}", file = log[i])
    print(f"剩餘資源：[Si, Ni, Ra, Co, Cr] = {LH[6:11]}，剩餘可動用人口：{remain_avl_popu[i] - popuD}", file = log[i])
    print("", file = log[i])
    

# 清算:
# 吃食物
have_meal_popu = [0]*10
maxPopu = list(history["max_popu"])

for i in range(10):
    print("食物清算：", file = log[i])
    print(f"第{i+1}小隊\n擁有食物：{history.iloc[i][3]}，此時人口上限：{maxPopu[i]}", file = log[i])
    have_meal_popu[i] = min( maxPopu[i], history["food"][i] ) # 計算多少人能吃飽
    history.loc[i,["available_popu"]] = round(have_meal_popu[i] * et.populationGrowthRate) # 吃飽的人可用，且成長
    history.loc[i,["max_popu"]] = round( maxPopu[i] * et.populationGrowthRate )  # 整體上限上升
    history.loc[i,["food"]] -= have_meal_popu[i] # 食物扣除
    print(f"下次可動用人口：{history.iloc[i][5]}，下次人口上限：{history.iloc[i][4]}", file = log[i])
    print("", file = log[i])

# 飢荒拯救
for i in range(10):
    if history.loc[i]["available_popu"] < history.loc[i]["max_popu"] * 0.15:
        history.iloc[i] = starvation(history.iloc[i])
        print(f"第{i+1}小隊 被拯救飢荒", file = log[i])

# 清算總傷害:
df_cumProd = history.iloc(1)[11:16]
history["hurt"] = et.cumulativeDamage(df_cumProd)

# 清算分數
for i in range(10):
   history.loc[i,["score"]] =  et.compute_score(history.iloc[i])


#存檔
Universe.write(history, f"{currentRound}-1.csv")


#世界歷史
price = et.inventroyPrice(history)
price = [round(i,3) for i in price]

record = pd.Series({"Round":currentRound, "food":sum(history["food"]), "Si":sum(history["Si"]), "Ni":sum(history["Ni"]), "Ra":sum(history["Ra"]), "Co":sum(history["Co"]), "Cr":sum(history["Cr"]), "P_food":price[0], "P_Si":price[1], "P_Ni":price[2], "P_Ra":price[3], "P_Co":price[4], "P_Cr":price[5]})
if os.path.isfile("historical_data.csv") == False:
    historical_data = pd.Series.to_frame(record).T
    historical_data.to_csv("historical_data.csv", sep= ",", index = False)
else:
    historical_data = pd.read_csv("historical_data.csv")
    historical_data = historical_data.append(record, ignore_index = True)
    historical_data.to_csv("historical_data.csv", sep= ",", index = False)


for i in log:
    i.close()
