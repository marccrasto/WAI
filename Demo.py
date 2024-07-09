import pandas as pd
from tensorflow import keras
from keras.models import load_model
import GetIncomeData as GI
import numpy as np
import sys
import ConvertCode as con
from sklearn.preprocessing import StandardScaler


def GetChange(di, y):
    year = y
    SIC = di.iloc[0]['SIC_Code']
    name = di.iloc[0]['Company Name']
    Data = con.index(SIC, year, name)
    return Data


def GetRow(di, y):
    sp = di.shape
    limit = sp[0]
    for i in range(0, limit):
        year = di.iloc[i]['Year']
        if(int(year) == int(y)):
            return i


def GetArray(di, y):
    Columns = ['Revenue', 'GrossProfit', 'Interest_Expense', 'Operation_Expense', 'Tax', 'NetIncome']
    array = []
    r = GetRow(di, y)
    flag = True
    for col in Columns:
        number = float(di.iloc[r][col])
        print(number)
        if(flag):
            array = np.array([number])
            flag = False
        else:
            array = np.hstack((array, [number]))
    return array


def AddInfor(array, SIC, year, name):
    Data = con.index(SIC, year, name)
    try:
        array = np.hstack((array, Data))
    except:
        array = np.hstack((array, [Data]))
    return array


Save_path = r'C:\Users\awe50\OneDrive\Desktop\WAI\Demo\Demo\Result'
Model_path = r'C:\Users\awe50\OneDrive\Desktop\WAI\Demo\Demo\DNN_600_0.9259_times.h5'

model = load_model(Model_path)
scaler = StandardScaler()
Con = 'Y'
while(Con == 'Y'):
    print("Please input the file name (XXX.xlsx)")
    file = input("File Name: ")
    #file = 'Test.xlsx'
    df = GI.getIncome(file)
    print("Which year do you want to predit? (Rang 2009 to 2028)")
    pYear = int(input('Predit Year: '))
    #pYear = 2023
    print("Which year you want to choose to be the base year?")
    byear = int(input('Base Year: '))
    times = pYear - byear
    answer = np.nan
    array = np.nan
    df['Revenue_Change'] = np.nan
    df['Employment_Change'] = np.nan
    df['Wages_Change'] = np.nan
    SIC = df.iloc[0]['SIC_Code']
    name = df.iloc[0]['Company Name']
    flagAns = True
    for i in range(0, times):
        if(i == 0):
            try:
                array = GetArray(df, byear)
            except:
                print('The file input is wrong, please try again')
                sys.exit(0)
        array = AddInfor(array, SIC, byear, name)
        array = array.reshape(1, -1)
        #array = scaler.fit_transform(array)
        try:
            income = model.predict(array)
        except:
            print("Can't find the SIC code, please try again")
            sys.exit(0)
        array = income
        byear += 1
        year = np.array([[byear]])
        #income = scaler.inverse_transform(income * scaler.scale_[:6] + scaler.mean_[:6])
        tmep = np.concatenate((year, income), axis=1)
        if(flagAns):
            answer = tmep
            flagAns = False
        else:
            answer = np.concatenate((answer, tmep), axis=0)

    ColName = ['Year', 'Revenue', 'GrossProfit', 'Interest_Expense', 'Operation_Expense', 'Tax', 'Net Income']
    dj = pd.DataFrame(answer, columns=ColName)
    path_to_save = Save_path + file
    dj.to_excel(path_to_save, index=False)
    Con = input('Do you wanna continue? Y for yes| N for no\n')
