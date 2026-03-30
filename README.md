# FaceDetection_BYOP_CV 🎯  

**Author:** Daiwik Paul Chowdhury  

---

## 📌 Project Overview  

This project implements a face detection system using OpenCV and Haar Cascade classifiers. It detects human faces from images, videos, and real-time webcam input using classical Computer Vision techniques.

The project is designed to be executable entirely from the command line and demonstrates core concepts of object detection and image processing.

---

## ⚙️ Features  

- Detect faces in images  
- Detect faces in video files  
- Real-time webcam face detection  
- Outputs detection statistics (count, coordinates)  
- Saves processed image/video with bounding boxes  

---

## 🛠️ Technologies Used  

- Python 3.8+  
- OpenCV  
- NumPy  

---

## 📁 Project Structure  

```
FaceDetection_BYOP_CV/
│── main.py
│── requirements.txt
│── README.md
│── .gitignore
```

---

## 🚀 Setup and Execution  

Follow these steps to run the project:

### 1. Clone the Repository  

```bash
git clone https://github.com/daiwikpc/FaceDetection_BYOP_CV.git
cd FaceDetection_BYOP_CV
```

---

### 2. (Optional) Create Virtual Environment  

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**macOS/Linux**
```bash
source venv/bin/activate
```

---

### 3. Install Dependencies  

```bash
pip install -r requirements.txt
```

---

### 4. Prepare Input Files  

Create a folder named `data` in the project directory:

```bash
mkdir data
```

Then add:
- `sample_image.jpg` → for image detection  
- `sample_video.mp4` → for video detection  

---

### 5. Run the Project  

```bash
python main.py
```

---

## ▶️ Execution Modes  

The program runs in three modes:

### Image Detection  
- Reads image from `data/sample_image.jpg`  
- Detects faces  
- Saves output as `data/output_image.jpg`  

---

### Video Detection  
- Reads video from `data/sample_video.mp4`  
- Processes each frame  
- Saves output as `data/output_video.mp4`  

---

### Webcam Detection  
- Uses system webcam  
- Runs for 15 seconds or until `q` is pressed  

---

## 🧠 Working Principle  

This project uses the **Haar Cascade Classifier (Viola-Jones Algorithm)**.

### Steps:
1. Convert input to grayscale  
2. Perform multi-scale detection  
3. Extract Haar features  
4. Apply cascade classifier  
5. Draw bounding boxes around faces  

---

## 📊 Output  

### Image Mode  
- Number of faces detected  
- Coordinates of faces  

### Video Mode  
- Total frames processed  
- Total faces detected  
- Average faces per frame  

### Webcam Mode  
- Total frames captured  
- Detection count  
- Execution duration  

---

## ⚡ Performance  

- Runs on CPU (no GPU required)  
- Real-time detection (~25–30 FPS)  
- Best performance on frontal faces  

---

## ⚠️ Limitations  

- Reduced accuracy for tilted faces  
- Sensitive to lighting conditions  
- Possible false positives  

---

## 📚 Concepts Covered  

- Object Detection  
- Image Processing  
- Feature Extraction  
- Real-Time Vision Systems  
- Video Processing  

---

## ❓ Notes for Evaluation  

- Fully executable via command line  
- No GUI setup required  
- All dependencies included in `requirements.txt`  
- Input/output paths handled internally  

---

## 📌 Conclusion  

This project demonstrates a practical implementation of face detection using classical Computer Vision techniques and serves as a foundation for more advanced systems such as face recognition or deep learning-based detection.
