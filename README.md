# ISS Speed Estimation using Astro Pi

**Astro Pi Mission Space Lab – 2024**

## Overview

This project was developed as part of the **Astro Pi Mission Space Lab 2024** challenge organized by the **European Space Agency (ESA)** and the **Raspberry Pi Foundation**.

The goal of the mission was to create a Python program that runs on the **Astro Pi computers aboard the International Space Station (ISS)** and performs a scientific experiment in orbit.

Our experiment estimates the **orbital speed of the ISS** by analyzing photographs taken from space. Using computer vision techniques, the program detects and tracks features in consecutive images of the Earth’s surface and calculates how far the station moved between the images.

During testing on the ISS, the program estimated a speed of:

**~7.47 km/s**

The real orbital speed of the ISS is approximately:

**~7.66 km/s**

This result demonstrates that image-based motion estimation can produce surprisingly accurate results even with limited onboard computing resources.

---

# Mission Objective

The objective of this experiment was to:

* Capture high-resolution images of Earth from the ISS
* Detect recognizable features in consecutive images
* Measure the displacement of those features
* Convert the measured displacement into a real-world distance
* Estimate the **orbital velocity of the ISS**

This experiment demonstrates how **computer vision and image analysis** can be used to estimate motion in space.

---

# How the Experiment Works

The program follows a multi-step processing pipeline:

1. Capture two images using the Astro Pi camera
2. Extract timestamps from image metadata
3. Detect visual features in both images
4. Match the same features across both images
5. Measure the average pixel displacement
6. Convert pixel displacement to ground distance
7. Calculate the speed using the time difference between images

### Processing Pipeline

```
Image Capture
      ↓
Feature Detection (SIFT)
      ↓
Feature Matching (FLANN)
      ↓
Pixel Displacement Measurement
      ↓
Ground Distance Estimation
      ↓
Speed Calculation
```

---

# Hardware Platform

The experiment runs on the **Astro Pi computer installed on the ISS**.

### Hardware used

* Raspberry Pi
* Raspberry Pi Camera
* Astro Pi sensor suite
* ISS observation window

The camera captures images of the Earth's surface as the ISS moves along its orbit.

---

# Image Processing

The project uses **OpenCV** for computer vision.

Two important algorithms are used:

### SIFT – Scale-Invariant Feature Transform

SIFT detects unique visual points in an image that remain recognizable even when:

* the camera moves
* the image rotates
* lighting conditions change

These points are called **keypoints**.

---

### FLANN – Fast Library for Approximate Nearest Neighbors

FLANN is used to match keypoints between two images.

This allows the program to find the **same physical locations on Earth** in both images.

---

# Speed Calculation

Once matching points are identified, the program measures the pixel displacement between them.

The average displacement is converted into real-world distance using a constant called **Ground Sampling Distance (GSD)**.

```
distance = pixel_displacement × GSD
speed = distance / time_difference
```

The result is an estimated **orbital speed in kilometers per second (km/s)**.

---

# Example Output

Example console output:

```
Approximately: 7.47 kmps
```

This value is very close to the real orbital speed of the ISS:

```
Real ISS speed ≈ 7.66 km/s
```

---

# Repository Structure

```
project/
│
├── main.py
├── requirements.txt
└── README.md
```

### main.py

Contains the full experiment code including:

* image capture
* feature detection
* feature matching
* speed estimation

### requirements.txt

Lists required Python libraries for running the project.

---

# Requirements

The project requires the following Python libraries:

```
opencv-python
exif
picamera
```

Install dependencies with:

```
pip install -r requirements.txt
```

---

# Running the Experiment

1. Connect a Raspberry Pi camera
2. Install required dependencies
3. Run the program

```
python main.py
```

The program will continuously:

* take two images
* analyze them
* estimate the ISS speed

---

# Educational Goals

This project demonstrates concepts from several scientific fields:

* computer vision
* orbital mechanics
* data analysis
* space engineering
* embedded programming

Students participating in Astro Pi Mission Space Lab gain hands-on experience with real scientific experiments performed in space.

---

# About Astro Pi

**Astro Pi** is an educational initiative by the **European Space Agency (ESA)** and the **Raspberry Pi Foundation**.

Students write programs that run on Raspberry Pi computers located on the **International Space Station**.

More information:

* https://astro-pi.org/
* https://astro-pi.org/mission-space-lab/

---

# Authors

Developed for the **Astro Pi Mission Space Lab 2024** project.

Created by:

* **BabbaWaagen**
* **DeMika69**

---

# License

Copyright © 2026 BabbaWaagen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.

The software is provided **“as is”**, without warranty of any kind.
