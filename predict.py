import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import json
import os

# ---------------- LOAD MODEL ----------------

model_path = os.path.join("model", "plant_disease_model.h5")
model = tf.keras.models.load_model(model_path)

# ---------------- CLASS NAMES ----------------
# Must match training folder names exactly

class_names = [
    "blight",
    "healthy",
    "leafspot",
    "powdery_mildew",
    "rust"
]

# ---------------- LOAD CARE TIPS ----------------

with open("plant_care.json", "r") as f:
    care_data = json.load(f)

# ---------------- PREDICTION FUNCTION ----------------

def predict_disease(img_path):

    try:
        # Load image
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)

        # Normalize
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        prediction = model.predict(img_array)

        predicted_index = np.argmax(prediction)
        predicted_class = class_names[predicted_index]
        confidence = float(np.max(prediction))

        # Get care tips
        care_tips = care_data.get(predicted_class, care_data["unknown"])

        return predicted_class, confidence, care_tips

    except Exception as e:
        print("Prediction Error:", e)
        return "unknown", 0.0, {}