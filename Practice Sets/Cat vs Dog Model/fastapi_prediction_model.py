from fastapi import FastAPI,UploadFile,File
from tensorflow.keras.models import load_model  # type: ignore
from tensorflow.keras.preprocessing import image  # type: ignore
import numpy as np
from io import BytesIO
from PIL import Image

app = FastAPI()
# Load saved model
model = load_model("cat_vs_dog_model.h5")
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        content = await file.read()
        img = Image.open(BytesIO(content)).resize((150, 150))
        img_tensor = image.img_to_array(img)
        img_tensor = np.expand_dims(img_tensor, axis=0)
        img_tensor /= 255.0
        # Predict
        prediction = model.predict(img_tensor)
        result = "That's Dog" if prediction[0][0] > 0.5 else "That's Cat"
        return {
            "filename": file.filename,
            "prediction": result
            }
    except Exception as e:
        return {
            "filename": file.filename if file else "No file provided",
            "message" : "An error occurred during prediction.",
            "error": str(e)
        }