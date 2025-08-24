import cv2
import numpy as np
import tensorflow as tf

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Load pre-trained mask detection model (TensorFlow/Keras)
model = tf.keras.models.load_model("mask_detector_model.h5")

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        face = frame[y:y + h, x:x + w]
        face_resized = cv2.resize(face, (100, 100)) / 255.0
        face_resized = np.expand_dims(face_resized, axis=0)

        # Predict mask/no mask
        prediction = model.predict(face_resized)[0][0]
        label = "Mask" if prediction > 0.5 else "No Mask"
        color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

        # Draw rectangle and label
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Face Mask Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()