# 🧹 Trash Skimming Robot for Water Bodies

This repository contains code, models, and evaluation workflows for a trash detection system aimed at identifying floating waste in water bodies. The system uses the YOLO object detection architecture and is designed for integration with an autonomous trash-skimming robot.

---

## 📂 Project Structure

```
.
├── notebooks/                  # Jupyter notebooks (baseline, improvements, visualizations)
│   ├── baseline.ipynb
│   └── improved_model.ipynb
├── src/                        # Core Python scripts
│   ├── boat/                        # Python scripts to handle boat's hardware/movement
│   │   ├── LaptopCameraControl.py
│   │   └── JetsonCameraControl.py
│   ├── miscellaneous/                  # Scripts for dataset annotation format conversion
│   │   ├── convert_XML_annotations.py
│   │   ├── convert_XML_annotations_2.py
│   │   └── convert_multiclass_annotations.py
├── models/                     # Trained YOLO models
│   ├── baseline_YOLOv12s.pt
│   ├── improved_YOLOv12s.pt
│   └── improved_YOLOv12n.pt
├── results/                    # Model Training and evaluation results
│   ├── yolo12vs-results/
│   ├── yolo12vn-results/
│   └── annotated_videos/       # Videos annotated using the improved model
├── .gitignore
└── README.md
```

---

## 🧠 Project Objective

To detect and classify floating trash in water bodies using YOLO-based object detection. The aim is to support real-time deployment on edge devices (e.g., Jetson Nano) for robotic waste removal applications.

---

## 🏗️ Methodology

### Baseline

* **Model:** YOLOv12 (custom trained on water-trash dataset)
* **Data:** 3,798 annotated images, Pascal VOC format, 19 overlapping trash classes
* **Metrics:** Precision, Recall, Accuracy, F1 Score

### Improvements

* Refined trash label set for better consistency
* IoU-based evaluation to distinguish overlapping and missed detections
* Video annotation pipeline for real-world frame-by-frame assessment

---

## 🎯 Results Summary

| Metric    | Baseline YOLO |
| --------- | ------------- |
| Accuracy  | 77.96%        |
| Precision | 87.48%        |
| Recall    | 87.75%        |
| F1 Score  | 87.62%        |

### Challenges Identified

* Poor detection of small or reflective objects
* False positives on background elements and water reflections
* Inconsistencies due to lighting, weather, and camera angle

---

## 🖼️ Visualizations

* **Bounding Boxes:** Red = Ground Truth, Green = Predicted
* **Annotated Videos:** Found in `results/annotated_videos/*`

---

## 📹 Video Annotation Pipeline

1. Load video frame-by-frame with OpenCV
2. Perform inference using YOLO
3. Draw bounding boxes around trash detections
4. Save annotated frames into output video

---

## 📥 Dataset Download

You can download the full annotated dataset (3,798 images in Pascal VOC format across 19 trash classes) from our [OneDrive folder](https://pern-my.sharepoint.com/:f:/g/personal/26100192_lums_edu_pk/Eh6KSecwmLRNsO6KOScjWSYB34LuJp4PC5RlNKSnwM3yGw?e=TUbEWO).

---


## 🤖 Hardware Integration

* Scripts for controlling laptop and Jetson Nano cameras:

  * `LaptopCameraControl.py`
  * `JetsonCameraControl.py`
* These support live inference and testing on embedded systems.

---

## 📜 License

MIT License. See `LICENSE` file for more details.

---

## 👥 Contributors

* Muhammad Abdullah 
* Zaeem Mohtashim Khan
* Model architecture based on [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)


