# ForecastAI

ForecastAI is a machine learning-powered web application that generates financial forecasts from company Excel workbooks.

It takes structured financial data (such as income statements and company information) and predicts future values like revenue, expenses, and net income over a selected time horizon.

---

## 🚀 Live Demo

https://wai-iu30.onrender.com

> Note: The public demo uses **mock forecast outputs** for reliability.  
> The full machine learning pipeline and model integration are included in this repository.

---

## 📌 What It Does

- Upload an Excel workbook containing financial data  
- Select a base year from the dataset  
- Choose a future prediction year  
- Generate forecasts for each year in between  
- View results directly in the browser  
- Download the forecast as an Excel file  

---

## 🧠 How It Works

1. The uploaded Excel file is parsed to extract financial data  
2. Relevant features are constructed from the base year  
3. Industry data (IBIS dataset) is incorporated  
4. A trained deep neural network generates predictions  
5. Forecasts are produced iteratively year by year  

---

## ⚙️ How to Use

1. Go to the Try It page  
2. Upload an Excel file  
3. Enter:
   - Base Year (must exist in your file)
   - Prediction Year (must be greater than base year)
4. Click Generate Forecast  
5. View results and download the output  

---

## ❗ Important Notes About Input

- The base year must match the data in your Excel file  
- The model predicts forward only  
- The model can predict up to a maximum of 6 years ahead  

### Example

**Valid case**
- Base year: 2021  
- Prediction year: 2027  
→ Forecast generated for 2022–2027  

**Invalid case**
- Base year: 2021  
- Prediction year: 2028  
→ Exceeds 6 year prediction limit  

If the base year is missing or incorrect, the model will fail.

---

## 🛠️ Tech Stack

**Frontend**
- HTML  
- CSS  
- JavaScript  

**Backend**
- Python  
- Flask  

**Machine Learning**
- TensorFlow / Keras  
- NumPy  
- Pandas  

**Deployment**
- Render  

**Other Tools**
- Gunicorn (production server)  
- Git LFS (model storage)  

---

## 💻 Running Locally

To run the full application (including the model) on your machine:

### 1. Clone the repository

```
git clone https://github.com/marccrasto/WAI.git
cd WAI
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Download the model

```
git lfs pull
```

### 4. Run the application

```
python app.py
```

### 5. Open in browser

```
http://127.0.0.1:8000
```

---

## 📁 Project Structure
.
├── app.py
├── templates/
├── static/
│ ├── css/
│ ├── js/
│ ├── uploads/
│ └── samples/
├── DNN_600_0.9259_times.h5
└── README.md

---

## 🎯 Why This Project

This project focuses on integrating machine learning into a full-stack application.

It goes beyond model training and emphasizes:
- building a usable interface  
- handling real-world data inputs  
- designing end-to-end ML pipelines  
- deploying ML systems in a production-like environment  

---

## ⚠️ Limitations

- Public demo uses mock data instead of live model inference  
- Model performance depends on input data quality  
- Requires a specific Excel format
- Maximum forecast horizon is 6 years

---

## 🔮 Future Improvements

- Separate cloud-based model inference service  
- Support for multiple Excel formats  
- Improved validation and error handling  
- Data visualizations for forecasts  

---
