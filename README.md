

# 🌞 Solar Rooftop Analyzer

**AI-powered tool to estimate your rooftop’s solar installation potential and financial metrics.**  

![Solar Rooftop Analyzer](https://github.com/akneeket/solar-rooftop-analyzer/assets/banner-image.png) <!-- (Add a relevant banner image if you have one!) -->

---

## 🚀 Features
✅ Upload rooftop satellite images  
✅ AI-based estimation of rooftop area  
✅ Recommended solar panel size (kW)  
✅ Estimated installation cost  
✅ Expected ROI in years  
✅ Key considerations for installation  
✅ Professional, colorful, and user-friendly UI  

---

## 🖥️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** FastAPI  
- **Language:** Python  
- **Libraries:** PIL, requests, numpy, pandas, etc.  
- **Deployment:** Render (API), Streamlit Cloud (Frontend)  

---

## ⚙️ How to Run Locally

1️⃣ Clone the repository:  
```bash
git clone https://github.com/akneeket/solar-rooftop-analyzer.git
cd solar-rooftop-analyzer
````

2️⃣ (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3️⃣ Install dependencies:

```bash
pip install -r requirements.txt
```

4️⃣ Start the **backend API (FastAPI)**:

```bash
uvicorn main:app --reload
```

5️⃣ Start the **frontend UI (Streamlit)**:

```bash
streamlit run app.py
```

6️⃣ Open your browser and enjoy!

---

## 🌐 Deployment

✅ **Backend (FastAPI)** deployed on [Render](https://render.com)
✅ **Frontend (Streamlit)** deployed on [Streamlit Cloud](https://streamlit.io/cloud)

---

## 📁 Project Structure

```
.
├── app.py               # Streamlit frontend
├── main.py              # FastAPI backend
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── .idea/               # IDE settings (can be ignored)
```

---

## 💡 Example Output

Here’s a typical JSON-style AI output:

```json
{
  "recommended_solar_size_kW": 3,
  "estimated_installation_cost": "₹210000",
  "expected_ROI_years": 6.5,
  "key_considerations": "Limited roof space restricts system size. Shading analysis crucial. Consider net metering policy in your area. Higher installation cost per kW expected due to smaller system size."
}
```

---

## 🙏 Contributing

Got ideas? Found a bug?
Feel free to **create an issue** or **submit a pull request**!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## ✨ Acknowledgements

* Inspired by the need for sustainable energy solutions.
* Built with 💙 by [Aniket](https://github.com/akneeket).

---

### 🔗 Useful Links

* **Repository:** [solar-rooftop-analyzer](https://github.com/akneeket/solar-rooftop-analyzer)
* **Streamlit Deployment:** (add URL)
* **Backend Deployment (Render):** (add URL)

---

```


