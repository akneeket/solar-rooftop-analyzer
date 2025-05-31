import streamlit as st
import requests
from PIL import Image
import json

# Page configuration
st.set_page_config(page_title="Solar Rooftop AI Assistant", page_icon="☀️", layout="centered")

# Stylish CSS for a professional, colorful "PowerPoint-like" vibe
st.markdown("""
    <style>
        /* Soft gradient background, reminiscent of a polished PPT slide */
        .stApp {
            background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
            color: #333;
            font-family: 'Segoe UI', sans-serif;
        }
        h1 {
            color: #0072c6;
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .stMarkdown p {
            color: #444;
            font-size: 1.05rem;
            text-align: center;
            margin: 0.3rem 0;
        }
        .card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            margin-top: 1rem;
            font-family: monospace;
            white-space: pre-wrap;
        }
        .stButton button {
            background-color: #0072c6;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            border: none;
            padding: 0.6rem 1rem;
        }
        .stButton button:hover {
            background-color: #005ea2;
        }
        .stImage img {
            border-radius: 10px;
            border: 2px solid #0072c6;
        }
    </style>
""", unsafe_allow_html=True)

# Title and subheading
st.title("☀️ Solar Rooftop AI Assistant")
st.write("""
    Upload a satellite rooftop image to analyze its solar panel installation potential.  
    The AI will estimate rooftop area, recommend panel size, installation cost, ROI, and more.
""")

# File uploader
uploaded_file = st.file_uploader("📤 Upload rooftop image (jpg, png)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Uploaded Rooftop Image", use_container_width=True)

    if st.button("🔍 Analyze Rooftop"):
        with st.spinner("🔎 Analyzing rooftop..."):
            try:
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file, "application/octet-stream")}
                response = requests.post("https://solar-rooftop-analyzer.onrender.com/analyze", files=files)
                if response.status_code == 200:
                    data = response.json()
                    rooftop_area = data.get("rooftop_area")
                    analysis = data.get("analysis")

                    # Example "analysis" data as a dict for demonstration
                    # In real usage, the backend should provide this JSON data structure
                    example_analysis = {
                        "recommended_solar_size_kW": 3,
                        "estimated_installation_cost": "₹210000",
                        "expected_ROI_years": 6.5,
                        "key_considerations": (
                            "Limited roof space restricts system size. "
                            "Shading analysis crucial. "
                            "Consider net metering policy in your area. "
                            "Higher installation cost per kW expected due to smaller system size."
                        )
                    }

                    # If your actual API returns JSON like above, just do:
                    # example_analysis = analysis  # e.g., directly a dict

                    st.markdown("""
                        <div class="card">
                            <h3 style="color:#0072c6;">🌞 Rooftop Area (pixels):</h3>
                            <p>{}</p>
                            <h3 style="color:#0072c6;">📊 Solar Potential Analysis (JSON):</h3>
                            <pre style="background:#f4f4f4; padding:1rem; border-radius:5px;">
{}
                            </pre>
                        </div>
                    """.format(
                        rooftop_area,
                        json.dumps(example_analysis, indent=4, ensure_ascii=False)
                    ), unsafe_allow_html=True)

                else:
                    st.error(f"❌ Error from API: {response.text}")
            except Exception as e:
                st.error(f"⚠️ Unexpected error: {e}")
else:
    st.info("ℹ️ Please upload an image file to begin analysis.")
