import pandas as pd
import numpy as np
import re
from tqdm import tqdm
import IncomeData as ida


def getIncome(file_path):
    df = pd.read_excel(file_path, header=None)

    SICCode = []
    RIncomeB = []
    RIncomeE = []
    RBalB = []
    RBalE = []

    fIn = False
    fBa = False
    flag = False
    CompName = []
    Shape = df.shape
    Limit = Shape[0]

    x = 0
    while x < Limit:
        line = df.iloc[x][0]

        if pd.isna(line):
            if fIn:
                RIncomeE.append(x)
                fIn = False
            elif fBa:
                RBalE.append(x)
                fBa = False

        elif str(line).strip() == 'Report Date':
            if flag:
                RBalB.append(x)
                fBa = True
                flag = False
            else:
                RIncomeB.append(x)
                fIn = True
                flag = True

        x += 1

    RBalE.append(x - 1)

    print("RIncomeB:", RIncomeB)
    print("RIncomeE:", RIncomeE)
    print("RBalB:", RBalB)
    print("RBalE:", RBalE)

    for y in tqdm(range(0, len(RBalE)), desc='Getting data from excel'):
        TempCode = []
        TempName = []

        if y == 0:
            for z in range(0, RIncomeB[0]):
                line = df.iloc[z][0]

                if str(line).strip() == "Primary SIC":
                    String = df.iloc[z + 1][0]
                    code = re.findall(pattern=r'\d{4}', string=str(String))
                    if code:
                        TempCode.append(code[0])

                elif str(line).strip() == "General Company Information":
                    Name = df.iloc[z - 2][0]
                    TempName.append(Name)

            if len(TempName) == 1 and len(TempCode) >= 1:
                SICCode.append(TempCode[0])
                CompName.append(TempName[0])
            elif len(TempName) > 1 and len(TempCode) >= 1:
                SICCode.append(TempCode[-1])
                CompName.append(TempName[-1])

    print('Finished getting information')
    print("CompName:", CompName)
    print("SICCode:", SICCode)
    print("There are {} companies' data".format(len(CompName)))

    first = True
    InData = []

    for i in range(0, len(CompName)):
        try:
            Num = RIncomeE[i] - RIncomeB[i] + 1

            if first:
                InData = ida.YearData(file_path, RIncomeB[i], Num, CompName[i], SICCode[i])
                print("First extracted block shape:", np.array(InData).shape)
                first = False
            else:
                data = ida.YearData(file_path, RIncomeB[i], Num, CompName[i], SICCode[i])
                print("Additional extracted block shape:", np.array(data).shape)
                if len(data) > 0:
                    InData = np.concatenate((InData, data), axis=0)

        except Exception as e:
            print("Extraction error:", e)
            continue

    InColumn = [
        'Year', 'Revenue', 'GrossProfit', 'Interest_Expense',
        'Operation_Expense', 'Tax', 'NetIncome', 'Company Name', 'SIC_Code'
    ]

    di = pd.DataFrame(data=InData, columns=InColumn)
    print("Final extracted rows:", len(di))
    return di