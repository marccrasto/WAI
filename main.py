from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
import numpy as np
import pandas as pd
from tensorflow import keras
from keras.models import load_model
import GetIncomeData as GI
import numpy as np
import ConvertCode as con
from sklearn.preprocessing import StandardScaler
import sys

file = None
bYear = None
pYear = None

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = r'C:\Users\awe50\OneDrive\Desktop\WAI\Demo\Demo\static\uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB

@app.route("/", methods=['GET', 'POST'])
def upload_form():
    return render_template('index.html')


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

def demo(fileName,bYear,pYear):
    Save_path = r'C:\Users\awe50\OneDrive\Desktop\WAI\Demo\Demo\static\saved\\'
    Model_path = r'C:\Users\awe50\OneDrive\Desktop\WAI\Demo\Demo\DNN_600_0.9259_times.h5'

    model = load_model(Model_path)
    scaler = StandardScaler()
    Con = 'Y'
    df = GI.getIncome(fileName)
    print(df.head())
    times = pYear - bYear
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
                    array = GetArray(df, bYear)
                except:
                    print('The file input is wrong, please try again')
                    sys.exit(0)
            array = AddInfor(array, SIC, bYear, name)
            array = array.reshape(1, -1)
            #array = scaler.fit_transform(array)
            try:
                income = model.predict(array)
            except:
                print("Can't find the SIC code, please try again")
                sys.exit(0)
            array = income
            bYear += 1
            year = np.array([[bYear]])
            #income = scaler.inverse_transform(income * scaler.scale_[:6] + scaler.mean_[:6])
            tmep = np.concatenate((year, income), axis=1)
            if(flagAns):
                answer = tmep
                flagAns = False
            else:
                answer = np.concatenate((answer, tmep), axis=0)

    ColName = ['Year', 'Revenue', 'GrossProfit', 'Interest_Expense', 'Operation_Expense', 'Tax', 'Net Income']
    dj = pd.DataFrame(answer, columns=ColName)
    path_to_save = Save_path + fileName
    dj.to_excel(path_to_save, index=False)


@app.route('/upload', methods=['POST'])
def uploadFile():
    try:
        if request.method == "POST":
            uploadedFile = request.files['file']
            bYear = request.form.get("bYear")
            bYear = int(bYear)
            pYear = request.form.get("pYear")
            pYear = int(pYear)
            

        if uploadedFile:
            file = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploadedFile.filename))
            uploadedFile.save(file)
            fileName = secure_filename(uploadedFile.filename)
            demo(fileName,bYear,pYear)

    except RequestEntityTooLarge:
        return 'File Too Large'

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port="8000")
