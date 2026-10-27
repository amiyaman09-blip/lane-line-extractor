# Multi-Strategy Lane Line Extractor Using OpenCV

## Project Overview
This project detects lane markings across diverse driving scenarios using Python, OpenCV, and NumPy. The engine combines multiple computer vision workflows to process road imagery—ranging from straight street corridors to complex curved highway channels. 

The pipeline handles static image data matrices through advanced localized thresholding, HSV filtering, edge gradient mapping, and dynamic window scanning networks. It incorporates a Probabilistic Hough Line Transform matching block to fit sharp vector models on straight road paths while utilizing an iterative sliding window sweep to map complex curves and compute geometric curve inflections.

## Objectives
- Load and process road imagery robustly using modular OpenCV structures.
- Apply HSV colour filtering to identify white and yellow lane markings.
- Use Gaussian blur to reduce image noise.
- Detect edges using the Canny edge detector.
- Apply ROI masking to focus on the road region.
- Detect straight line segments with the Probabilistic Hough Line Transform and track complex curves using an iterative sliding window sweep.
- Locate the geometric bend points of curved paths using discrete finite difference mathematics.
- Organise the code into reusable Python functions.

## Technologies Used
- Python
- OpenCV (`cv2`)
- NumPy

## Project Structure
```text
lane-line-extractor/
├── images/
│   └── road.png
├── image/
│   └── image2.png
├── new_image/
│   ├── blurred.jpg
│   ├── canny_edges.jpg
│   ├── colour_mask.jpg
│   ├── combined_edge_mask.jpg
│   ├── lane_lines.jpg
│   ├── roi_edges.jpg
│   └── roi_preview.jpg
├── output1/
│   ├── blurred.jpg
│   ├── canny_edges.jpg
│   ├── colour_mask.jpg
│   ├── hsv_mask.jpg
│   ├── lane_lines.jpg
│   ├── original.jpg
│   └── roi_edges.jpg
├── lane_detector.py
└── README.md
```

## Installation
Install the required libraries:
```bash
py -m pip install opencv-python numpy
```

## How to Run
Open the project folder in VS Code, open the terminal, and run:
```bash
py lane_detector.py
```

---

## Part 1: Baseline Straight Road Profile (`output1/` Directory)

### 1. Source Input Photo
![Original road image](output1/original.jpg)

### 2. Isolated HSV Mask (White Markings Only)
![HSV colour mask](output1/hsv_mask.jpg)

### 3. Isolated Colour Mask (Yellow Markings Only)
![HSV colour mask](output1/colour_mask.jpg)

### 4. Gaussian Blur Mask Output
![Blurred mask](output1/blurred.jpg)

### 5. Canny Edge Detection Grid
![Canny edges](output1/canny_edges.jpg)

### 6. Bounded Region of Interest (ROI) Masking
![ROI edges](output1/roi_edges.jpg)

### 7. Final Master Straight Lane Line Output
![Final lane detection](output1/lane_lines.jpg)

---

## Part 2: Advanced Curved Road Profile (`new_image/` Directory)

### 1. Combined Edge Mask Grid
![Curved Combined Edge](new_image/combined_edge_mask.jpg)

### 2. Active ROI Preview Bounding Poly
![Curved ROI Preview](new_image/roi_preview.jpg)

### 3. Final Master Curved Lane Sliding Window Output
*The sliding window adapts step-by-step to the shifting lane topology, anchoring a green inflection circle precisely at the curve apex.*
![Curved Final Lanes Output](new_image/lane_lines.jpg)

---

## Limitations
- Performance depends on clear paint visibility and distinct pavement-to-shoulder contrast breaks.
- Extremely sharp right-angle curves or urban intersections can exceed the horizontal boundaries of the sliding search windows.
- The Region of Interest polygon coordinates are manually configured per image; radical camera positioning changes require updated baseline vector dimensions.

## Conclusion
This framework demonstrates a highly adaptive computer vision solution built to track lane parameters across diverse driving environments. By leveraging local window momentum filters, directional gradients, Hough transforms, and finite difference math, the system delivers precise path estimation for both straight city streets and complex winding highways.
