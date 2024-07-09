import pandas as pd
import numpy as np
import re

from tqdm import tqdm
import sys
import os

import ConvertCode as con
import IncomeData as ida


def getIncome(file):
    file_path = r'C:\Users\awe50\OneDrive\Desktop\WAI\Demo\Demo\static\uploads\\'
    full = file_path + file
    print(full)
    df = pd.read_excel(full, header=None)
    SICCode = []
    RIncomeB = []
    RIncomeE = []
    RBalB = []
    RBalE = []

    fIn = False
    fBa = False
    nan = False
    flag = False
    CompName = []
    Shape = df.shape
    Limit = Shape[0]

    x = 0
    while x < Limit:
        line = df.iloc[x][0]
        # print(line)
        if(pd.isna(line)):
            if(fIn):
                RIncomeE.append(x)
                fIn = False
            elif(fBa):
                RBalE.append(x)
                fBa = False
        elif(line == 'Report Date'):
            if(flag):
                RBalB.append(x)
                fBa = True
                flag = False
            else:
                RIncomeB.append(x)
                fIn = True
                flag = True
        x += 1
    RBalE.append(x - 1)
    for y in tqdm(range(0, len(RBalE)), desc='Getting data from excel'):
        TempCode = []
        TempName = []
        if(y == 0):
            for z in range(0, RIncomeB[0]):
                line = df.iloc[z][0]
                if(line == "Primary SIC"):
                    String = df.iloc[z + 1][0]
                    code = re.findall(pattern='\d{4}', string=String)
                    code = code[0]
                    TempCode.append(code)
                elif(line == "General Company Information"):
                    Name = df.iloc[z - 2][0]
                    TempName.append(Name)
            if(len(TempName) == 1):
                SICCode.append(TempCode[0])
                CompName.append(TempName[0])
            else:
                SICCode.append(TempCode[-1])
                CompName.append(TempName[-1])
            TempCode = []
            TempName = []

    print('Finished getting informaiton')
    print("There are {} companies' data".format(len(CompName)))
    first = True
    InData = []

    for i in range(0, len(CompName)):
        try:
            if (first):
                Num = RIncomeE[i] - RIncomeB[i] + 1
                InData = ida.YearData(full, RIncomeB[i], Num, CompName[i], SICCode[i])
                first = False
            else:
                Num = RIncomeE[i] - RIncomeB[i] + 1
                data = ida.YearData(full, RIncomeB[i], Num, CompName[i], SICCode[i])
                if(len(data) > 0):
                    InData = np.concatenate((InData, data), axis=0)
        except:
            continue
    InColumn = ['Year', 'Revenue', 'GrossProfit', 'Interest_Expense', 'Operation_Expense', 'Tax', 'NetIncome', 'Company Name', 'SIC_Code']
    di = pd.DataFrame(data=InData, columns=InColumn)
    return di


#print(getIncome('Test.xlsx'))
