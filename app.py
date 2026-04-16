from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
import numpy as np
import pandas as pd
from keras.models import load_model
import GetIncomeData as GI
import ConvertCode as con
import sys
import time

app = Flask(__name__, static_url_path='/static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
SAVED_FOLDER = os.path.join(BASE_DIR, "static", "saved")
MODEL_PATH = os.path.join(BASE_DIR, "DNN_600_0.9259_times.h5")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SAVED_FOLDER'] = SAVED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SAVED_FOLDER, exist_ok=True)

model = load_model(MODEL_PATH)


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/how")
def how_page():
    return render_template("how.html")


@app.route("/try")
def try_page():
    return render_template("try.html")

@app.route('/health')
def health():
    return {"status": "ok"}


def GetRow(di, y):
    sp = di.shape
    limit = sp[0]
    for i in range(0, limit):
        year = di.iloc[i]['Year']
        if int(year) == int(y):
            return i
    return None


def GetArray(di, y):
    columns = ['Revenue', 'GrossProfit', 'Interest_Expense', 'Operation_Expense', 'Tax', 'NetIncome']
    row_index = GetRow(di, y)
    if row_index is None:
        raise ValueError("Base year not found in uploaded file.")

    values = []
    for col in columns:
        values.append(float(di.iloc[row_index][col]))
    return np.array(values)

industry_cache = {}

def AddInfor(array, sic, year, name):
    key = (str(sic), int(year), str(name))
    if key not in industry_cache:
        industry_cache[key] = con.index(sic, year, name)
    data = industry_cache[key]
    return np.hstack((array, data))


def run_forecast(file_path, file_name, base_year, predict_year):
    start_time = time.time()

    df = GI.getIncome(file_path)
    print("getIncome took:", time.time() - start_time)

    if df.empty:
        raise ValueError("No readable financial data was found in the uploaded workbook.")

    times = predict_year - base_year
    if times <= 0:
        raise ValueError("Prediction year must be greater than base year.")

    if times > 10:
        raise ValueError("Prediction range is too large. Please choose a range of 10 years or less.")

    sic = df.iloc[0]['SIC_Code']
    name = df.iloc[0]['Company Name']

    answer = None
    array = None

    for i in range(times):
        loop_start = time.time()

        if i == 0:
            array = GetArray(df, base_year)

        info_start = time.time()
        array_with_info = AddInfor(array, sic, base_year, name)
        print(f"AddInfor for year {base_year} took:", time.time() - info_start)

        pred_start = time.time()
        model_input = array_with_info.reshape(1, -1)
        income = model.predict(model_input, verbose=0)
        print(f"predict for year {base_year} took:", time.time() - pred_start)

        array = income.flatten()

        base_year += 1
        year_arr = np.array([[base_year]])
        temp = np.concatenate((year_arr, income), axis=1)

        if answer is None:
            answer = temp
        else:
            answer = np.concatenate((answer, temp), axis=0)

        print(f"Total loop for year {base_year} took:", time.time() - loop_start)

    columns = ['Year', 'Revenue', 'GrossProfit', 'Interest_Expense', 'Operation_Expense', 'Tax', 'Net Income']
    result_df = pd.DataFrame(answer, columns=columns)

    output_name = f"forecast_{secure_filename(file_name)}"
    save_path = os.path.join(app.config['SAVED_FOLDER'], output_name)
    result_df.to_excel(save_path, index=False)

    preview_df = result_df.copy()
    numeric_cols = ['Revenue', 'GrossProfit', 'Interest_Expense', 'Operation_Expense', 'Tax', 'Net Income']
    for col in numeric_cols:
        preview_df[col] = preview_df[col].round(2)

    preview_rows = preview_df.head(10).to_dict(orient="records")

    print("Total run_forecast time:", time.time() - start_time)

    return output_name, columns, preview_rows


@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        uploaded_file = request.files.get("file")
        if not uploaded_file or uploaded_file.filename == "":
            return jsonify({"success": False, "error": "Please choose an Excel file."}), 400

        base_year = request.form.get("bYear", "").strip()
        predict_year = request.form.get("pYear", "").strip()

        if not base_year or not predict_year:
            return jsonify({"success": False, "error": "Please enter both base year and prediction year."}), 400

        try:
            base_year = int(base_year)
            predict_year = int(predict_year)
        except ValueError:
            return jsonify({"success": False, "error": "Years must be valid numbers."}), 400

        filename = secure_filename(uploaded_file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(upload_path)

        output_name, columns, preview_rows = run_forecast(upload_path, filename, base_year, predict_year)

        return jsonify({
            "success": True,
            "message": "Forecast generated successfully.",
            "columns": columns,
            "rows": preview_rows,
            "download_url": f"/download/{output_name}"
        })

    except RequestEntityTooLarge:
        return jsonify({"success": False, "error": "File too large."}), 413
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Something went wrong: {str(e)}"}), 500


@app.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(app.config['SAVED_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=8000)