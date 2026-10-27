### Submission: Classical Computer Vision Lane Line Extractor

### Project Overview

This repository contains a modular computer vision perception pipeline developed to isolate highway lane markings from static imagery using traditional image processing techniques. 

Built initially to fulfill baseline assignment criteria utilizing color-space clustering and geometric line fittings, this project was extended to include an advanced **Dynamic Sliding Window Scanning Matrix** and **Discrete Finite Difference Curvature Evaluation Engine**. The system autonomously handles both high-contrast straight street grids and complex winding highway channels without execution faults. 

### Objectives & Deliverables

* **Core Pipeline Implementation:** Developed clean, decoupled, and production-ready Python modules mapping the standard image processing sequence.
* **Robust Color Space Isolation:** Deployed localized adaptive thresholds alongside multi-channel HSV matrix masks to shield tracking layers from bridge shadows and environmental noise.
* **Edge & Gradient Context Fusion:** Fused classic Canny edge contours with Sobel directional Y-gradients to safely resolve both unpainted concrete curbs and standard painted lanes.
* **Dynamic Structural Adaptability (Extra Effort):** Tracked reversing S-curves sequentially via window momentum vectors and mathematically derived lane inflection vertex locations using second-order finite derivative steps.

### Technologies Used

* **Language:** Python
* **Core Libraries:** OpenCV (cv2), NumPy, OS File System Utilities

### Repository Structure

text

lane-line-extractor/
├── lane_detector.py
├── road.png
├── hsv_mask.jpg
├── colour_mask.jpg
├── blurred.jpg
├── canny_edges.jpg
├── roi_edges.jpg
├── lane_lines.jpg
├── image/
│   ├── new image.jpeg
│   └── image2.png
├── output/
│   ├── new_image/
│   │   ├── colour_mask.jpg
│   │   ├── blurred.jpg
│   │   ├── canny_edges.jpg
│   │   ├── roi_edges.jpg
│   │   ├── roi_preview.jpg
│   │   └── lane_lines.jpg
│   └── image2/
│       ├── colour_mask.jpg
│       ├── blurred.jpg
│       ├── canny_edges.jpg
│       ├── roi_edges.jpg
│       ├── roi_preview.jpg
│       └── lane_lines.jpg
└── README.md

Use code with caution.

### Installation & Setup

1. **Clone the Repository:** 

bash

git clone https://github.com/your-username/lane-line-extractor.git
cd lane-line-extractor

Use code with caution.
2. **Install Dependencies:** 

bash

py -m pip install opencv-python numpy

Use code with caution.
3. **Execution Instructions:** 

bash

py lane_detector.py

Use code with caution.

*Note: Set the global variable SHOW_WINDOWS = True at the head of lane_detector.py to prompt interactive UI display boxes across each pipeline iteration layer.*

### Part 1: Core Assignment Pipeline (Required Deliverables)

The core architecture executes a traditional perception sequence designed around localized structural attributes: 

1. **Matrix Ingestion:** Image data arrays are read and rescaled down to a standardized uniform 960 × 540 tracking frame workspace to equalize processing velocities.
2. **HSV Color Filtering:** Grayscale conversions are bypassed initially to segment white and yellow pixels across specific HSV tint matrices, preserving paint context over asphalt.
3. **Gaussian Convolution:** A 5×5 kernel blur smooths out structural color discontinuities and asphalt surface reflections.
4. **Canny Structural Mapping:** High and low threshold gradient matrices strip out regional fill and yield pure edge vectors.
5. **Region of Interest (ROI) Isolation:** Vector coordinates form an explicit geometric polygon bounding box, discarding peripheral context (sky, trees, urban structures) above the horizon line.
6. **Hough Projection Optimization:** Line fragments found inside the edge array are consolidated using slope constraints, rendering long, direct structural representations.

### Baseline Processing Sequence Artifacts

#### Stage 1: Source Roadway Image

 

#### Stage 2: Combined Color Spaces (HSV White & Yellow)

 

#### Stage 3: Post-Convolution Gaussian Smoothing

 

#### Stage 4: Canny Edge Grid Generation

 

#### Stage 5: Bounded Region of Interest Masking

 

#### Stage 6: Final Line Fitting Projection

 

### Part 2: Advanced Feature Showcase (Extra-Credit Extensions)

To challenge the limitations of traditional line fitting when managing complex roadway dynamics, an advanced tracking network was built over the baseline architecture. 

### Feature 1: Dynamic Line Realignment (Flattening Artifact Corrections)

When straight city street grids are processed via sequential upward tracking blocks, minor edge anomalies often distort the lane lines. The script calculates a strict R-squared (

R2cap R squared
𝑅2
) correlation coefficient. If tracking outputs map with high linearity, the script automatically smooths the data into direct vector lines, preventing jagged artifacts while preserving full tracking integrity. 

### Feature 2: Iterative Sliding Window Tracking & Inflection Mapping

On winding highway turns, when straight line assumptions completely fail, the system falls back onto an iterative upward sliding search grid window. Momentum filters maintain vector trajectory through broken lane paint. A second-order difference derivative block then solves rate-of-change adjustments along the matrix curve to identify the lane's physical inflection point, highlighting the exact curve apex with a green visual anchor. 

### Extra-Credit Visual Demonstrations

#### Straight Road Profile Output (City Corridor)

*Maintains razor-sharp parallel projections toward the vanishing horizon by flattening local tracking jitter.* 

* **Color Mask Output:** output/new_image/colour_mask.jpg
* **Canny Edges Matrix:** output/new_image/canny_edges.jpg
* **Active ROI Bounds:** output/new_image/roi_preview.jpg

 

#### Curved Road Profile Output (Highway Mountain Pass)

*The sliding window adapts step-by-step to the shifting lane topology, anchoring a green inflection circle precisely at the curve apex.* 

* **Color Mask Output:** output/image2/colour_mask.jpg
* **Canny Edges Matrix:** output/image2/canny_edges.jpg
* **Active ROI Bounds:** output/image2/roi_preview.jpg

 

### Operational Constraints & Limits

* **Contrast Dependencies:** System tracking accuracy relies heavily on defined differences between road markings and regional asphalt hues.
* **ROI Exclusivity:** Bounding polygon coordinate configurations are strictly static per environment template. Drastic camera lens positional updates demand updated geometry initialization parameters.
* **Angle Caps:** Ultra-sharp right-angle turns or urban street junctions can break out of the search boundaries established by the sliding window widths.

### Summary & Structural Value

This submission delivers a complete classical computer vision perception solution. By fusing traditional HSV-Canny processing sequences with custom sliding window networks and finite numeric derivative calculations, the system reliably outputs smooth, high-fidelity path estimations across both straight city street corridors and winding highway systems.
