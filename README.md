#  YouTube Views Prediction App

This project is a machine learning web application that predicts the expected number of views for a YouTube video based on key features such as likes, comment count, publish hour, category, and channel title.

The model is trained using **Multiple Linear Regression** and deployed through a **Streamlit** web interface.

---

##  Features

- Predict YouTube video views using ML
- User-friendly interface built with Streamlit
- Category dropdown (no need to remember category IDs)
- Automatic engagement rate calculation
- Clean and responsive UI
- Fully reproducible using `uv` package manager

---

## 🛠 Installation

This project uses **uv** for fast environment creation and dependency syncing.

### 1. Clone the Repository

```bash
git clone https://github.com/SoeukBondol-ai/Yt-views-Predict.git
cd Yt-views-Predict
uv sync
```

### 2. Start run project
```bash
cd app
uv run streamlit run main.py
```

