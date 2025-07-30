# Financial-Statement-Analysis
📊 Interactive Streamlit dashboard for visualizing quarterly financial statement data collected from PDF reports. Includes time-series visualizations and multi-company comparisons. Future updates will add raw data parsing from PDF and number-based analysis.

# 📈 Financial Statement Visualization Dashboard

This repository contains a **Streamlit web app** for visualizing quarterly financial statement data from various banks and financial institutions. The project transforms tabular and percentage-based financial features into **interactive visualizations** to help track changes over time and compare across companies.

---

## 🚀 Features

- 📊 Interactive line charts with multi-company comparison  
- 📈 Explore key financial ratios like ROA, NPL, LDR, etc. over quarters  
- 🧠 Smart sorting of quarters (Q1, Q2, ...) for clean time-series plotting  
- 🔍 Customize views with dropdowns and filters  
- 📅 Data based on quarterly financial statements  

---

## 📂 Project Structure

<!-- START STRUCTURE -->
```
.
├── README.md
├── STRUCTURE.txt
├── data
│   ├── Aset.xlsx
│   ├── Rasio.xlsx
│   ├── summarized_aset.xlsx
│   └── summarized_rasio.xlsx
├── full_requirements.txt
├── main_app.py
├── pages
│   ├── number
│   └── percentage
├── requirements.txt
├── structure.txt
└── tmp

5 directories, 11 files
```
<!-- END STRUCTURE -->

---

## 📥 Future Additions

The following features are planned for upcoming releases:

- 📄 PDF Reading Module: Automatically extract financial data from PDFs  
- 🔢 New Pages: Visualizations for number-based (not percentage) features  
- 🧾 Expanded Feature Set: Include more financial ratios and indicators  
- 📁 Sample PDFs: Include the original quarterly reports used as data source  

---

## 🛠 Installation

Make sure you have Python 3.10 installed.

1. **Clone the repository**
   ```
   git clone https://github.com/tancos02/Financial-Statement-Analysis.git
   cd your-repo-name
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**
   ```
   streamlit run main_app.py
   ```

---

## 🌐 Deployment

This app is ready to be deployed on [Streamlit Cloud](https://streamlit.io/cloud) for **free hosting**. Simply connect this GitHub repository to your Streamlit account.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🤝 Contributions

Contributions and suggestions for new features or improvements are welcome!

---

## 📬 Contact

For questions, feel free to reach out via GitHub issues or [LinkedIn](https://www.linkedin.com/in/paulussiahaan02/).
