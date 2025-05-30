from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import os
from dotenv import load_dotenv
import google.generativeai as genai
import torch
from torchvision import models, transforms
import json
import re

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Load DeepLabV3 model (for rooftop segmentation)
deeplab = models.segmentation.deeplabv3_resnet101(pretrained=True).eval()

# Preprocess function for DeepLabV3
preprocess = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(256),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

@app.post("/analyze")
async def analyze_rooftop(file: UploadFile = File(...)):
    try:
        # Read the uploaded file
        image_data = await file.read()
        if not image_data:
            return JSONResponse({"error": "Empty file uploaded!"}, status_code=400)

        # Convert the file to a numpy array
        np_img = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        if img is None:
            return JSONResponse({"error": "Invalid image file or corrupt file!"}, status_code=400)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Preprocess image for DeepLabV3
        input_tensor = preprocess(img_rgb).unsqueeze(0)

        with torch.no_grad():
            output = deeplab(input_tensor)['out'][0]
        output_predictions = output.argmax(0).byte().cpu().numpy()

        # Create a binary mask for rooftop area
        rooftop_mask = (output_predictions > 0).astype(np.uint8)
        rooftop_area = int(np.sum(rooftop_mask))

        # Prepare prompt for Gemini LLM with JSON wrapped in triple backticks
        prompt = f"""
You are an expert in solar rooftop analysis specialized for India. 
Provide a strictly JSON-only response (no extra commentary). Use the format below exactly.

Consider local Indian market conditions, average installation costs (₹45,000 to ₹70,000 per kW), typical rooftop sizes, and ROI based on Indian sunlight and electricity rates.

Rooftop Area (approx pixels): {rooftop_area}

Respond only with this JSON object, wrapped in triple backticks like this:

```json
{{
  "recommended_solar_size_kW": 4,
  "estimated_installation_cost": "₹180,000",
  "expected_ROI_years": 5.0,
  "key_considerations": "Small roof area; consider micro-inverters for optimal performance. Verify shading analysis."
}}
"""
        # Gemini LLM Integration
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        analysis_text = response.text.strip()

        # Extract JSON block if wrapped in triple backticks
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", analysis_text, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
        else:
            json_str = analysis_text  # fallback if no triple backticks

        try:
            analysis_json = json.loads(json_str)
        except json.JSONDecodeError:
            return JSONResponse({
                "rooftop_area": rooftop_area,
                "analysis_raw": analysis_text,
                "warning": "Failed to parse JSON from Gemini response"
            }, status_code=200)

        return JSONResponse({
            "rooftop_area": rooftop_area,
            "analysis": analysis_json
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
