# ISS Speed Estimation using Astro Pi  

**Astro Pi Mission Space Lab - 2024**

---

## Overview  

This project was developed as part of a school project within the Astro Pi Mission Space Lab challenge (ESA).

The goal was to estimate how fast the ISS is moving using only images.

We followed the general idea from the official Astro Pi project, but implemented everything ourselves in Python using OpenCV.

The program takes two images, detects features, matches them, measures the movement, and converts that into a real-world speed.

The experiment was executed on the Astro Pi computers aboard the ISS as part of the official Astro Pi Mission Space Lab program.

Estimated speed:

**~7.47 km/s**

Actual ISS speed:

**~7.66 km/s**

So roughly a ~2-3% difference - just from image analysis.

More information:

* https://astro-pi.org/
* https://astro-pi.org/mission-space-lab/
* https://projects.raspberrypi.org/en/projects/mission-space-lab-creator-guide/0

---

## Important Note  

The images in this repository are most likely from the Astro Pi template / testing phase.

The actual images captured during runtime are unfortunately lost and couldn't be recovered.  
If I find them again, I will upload them in a separate folder.

---

## Mission Objective  

- Capture images of Earth  
- Detect features between images  
- Measure movement  
- Convert to real-world distance  
- Estimate ISS speed  

---

## How it works  

1. Capture two images  
2. Extract timestamps  
3. Detect features (SIFT)  
4. Match features (FLANN)  
5. Measure pixel displacement  
6. Convert pixels -> distance (GSD)  
7. Calculate speed  

---

## Pipeline  

Image Capture  
↓  
Feature Detection  
↓  
Feature Matching  
↓  
Displacement  
↓  
Distance  
↓  
Speed  

---

## Tech  

- Python  
- OpenCV  
- SIFT  
- FLANN  

---

## Formula  

distance = pixel_displacement × GSD  
speed = distance / time_difference  

---

## Example Output  

Approximately: 7.47 kmps  

Real ISS speed ≈ 7.66 km/s  

---

## Project Structure  

project/  
├── main.py  
├── requirements.txt  
└── README.md  

---

## Requirements  

opencv-python  
exif  
picamera  

Install:

pip install -r requirements.txt  

---

## Running  

python iss_speed_normal_version.py  

---

## Authors

Developed for the **Astro Pi Mission Space Lab 2024** project.

Created by:

* **BabbaWaagen**
* **DeMika69**

---

## Contact:
jay.miller@bladiostudio.com

---

## License

Copyright © 2026 BabbaWaagen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.

The software is provided "as is", without warranty of any kind.
