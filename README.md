# 🌍 Global Holiday Planner

An interactive **Streamlit app** that helps you find the best holiday weeks around the world based on **temperature, rainfall, sunshine, and wind**.

---

## ✨ Features
- Weekly holiday score (combines temperature, rainfall, sunshine, wind)
- Uses **historical data** (Meteostat) + **forecast data**
- Clean UI with background image and fade‑in animation
- Download results as **CSV**
- Charts: weekly trend + daily heatmap
- Filters: city, year, hemisphere, summer‑only mode

---

## 🚀 How to Run

1. **Clone the repo**
   ```bash
   git clone https://github.com/awoniyijulius/global_holiday_planner.git
   cd <repo-name>
2. **Install dependencies**

pip install -r requirements.txt

3. **Start the app**

bash
streamlit run app.py

## 📂 Project Structure
Code
app.py
requirements.txt
README.md
ui/
  ├── components.py
  └── charts.py
data_sources/
  ├── meteostat_data.py
  └── forecast_data.py
logic/
  ├── scoring.py
  └── blending.py
## 🌐 Deployment
**Push this repo to GitHub**

**Go to Streamlit Cloud**

**Select your repo → branch = main → main file = app.py**

**Deploy and get your shareable link**

## 🛠️ Built With
**Streamlit**

**Pandas, Numpy**

**Meteostat**

**fpdf2**

**Plotly / Matplotlib / Seaborn**

## 📜 License
MIT License – free to use and adapt
