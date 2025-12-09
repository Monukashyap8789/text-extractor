# 📝 Text Extraction System (OCR + Streamlit)

A simple, fast, and accurate text-extraction web app built using **Python**, **Streamlit**, and **Tesseract OCR**.  
Upload an image → extract clean readable text instantly.

---

## 🚀 Features

- Upload any image (JPG, PNG, JPEG, TIFF)
- Extract text using Tesseract OCR
- Clean UI built with Streamlit
- Works online when deployed
- Backend separated (`ocr_backend.py`) for modularity
- Supports deployment on Streamlit Cloud / Hugging Face Spaces

---

## 📁 Project Structure

New_version_of_text_Extraction_System/
│
├── app.py # Streamlit frontend UI
├── ocr_backend.py # OCR processing logic
├── requirements.txt # Python dependencies
├── packages.txt # Linux system packages (tesseract-ocr)
└── README.md # Documentation

---

## 🔧 Installation (Local Setup)

### 1. Clone the repository

git clone https://github.com/Monukashyap8789/text-extractor.git

cd text-extractor


### 2. Install Python dependencies



### 3. Install Tesseract OCR (System Dependency)

#### **Windows**
Download and install:  
https://github.com/UB-Mannheim/tesseract/wiki

Example path:


Update this in `ocr_backend.py` if needed.

#### **Linux**

(Used by Streamlit Cloud)

---

## ▶️ Running the App Locally

Run using Streamlit:


The app opens automatically in your browser:


---

## ☁️ Deployment Guide

### **Streamlit Cloud (Recommended – Free)**

1. Push the project to GitHub  
2. Go to https://share.streamlit.io  
3. New App  
4. Select repository  
5. Main file: `app.py`  
6. Deploy

Make sure you have:

### **requirements.txt**

### **packages.txt**

Streamlit Cloud will install everything automatically.

---

## 🧠 How OCR Works (Short Explanation)

1. Uploaded image is read using Pillow/OpenCV  
2. Image is processed and passed to Tesseract  
3. Tesseract extracts visible text  
4. Streamlit displays processed text on the UI  

Simple and effective.

---

## 🛠️ API / Backend Function

`extract_text(image)` is the core function that:

- Loads the uploaded image  
- Sends it to Tesseract  
- Returns extracted text  

Located in: `ocr_backend.py`.

---

## 📌 Future Improvements

- Add PDF text extraction  
- Add image preprocessing for better accuracy  
- Add multilingual text recognition  
- Add text download in .txt or .pdf format  

---

## 🤝 Contribution

Pull requests are welcome.  
If you find a bug, open an issue in the repo.

---

## 📜 License

This project is open-source and free to use for learning or commercial projects.

