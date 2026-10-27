# Assignment: Classical Computer Vision & Lane Line Extractor

## Project Overview
The goal of this project is to build a lane line extractor using OpenCV. Static road images are processed to isolate highway lane lines using classical computer vision techniques, laying the groundwork for perception systems.

## Objectives
1. Load and process static road images using OpenCV.
2. Implement HSV color space transformations for robust color filtering.
3. Apply Gaussian blur to reduce image noise.
4. Apply Canny edge detection to identify lane boundaries.
5. Apply Region of Interest (ROI) masking to isolate the road area.

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
├── output/
│   ├── image2/
│   │   ├── blurred.jpg
│   │   ├── canny_edges.jpg
│   │   ├── colour_mask.jpg
│   │   ├── combined_edge_mask.jpg
│   │   ├── lane_lines.jpg
│   │   ├── roi_edges.jpg
│   │   └── roi_preview.jpg
│   └── new_image/
│       ├── blurred.jpg
│       ├── canny_edges.jpg
│       ├── colour_mask.jpg
│       ├── combined_edge_mask.jpg
│       ├── lane_lines.jpg
│       ├── roi_edges.jpg
│       └── roi_preview.jpg
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

## Processing Pipeline & Results

### Part 1: Straight Road Scenarios (Probabilistic Hough Line Transform)

The core code utilizes the **Probabilistic Hough Line Transform (`cv2.HoughLinesP`)** to isolate individual lane line segments. These lines are filtered by structural slope characteristics, grouped by road position, and fitted with robust bounding lines to establish linear path equations. The same Hough optimization block is deployed to outline the dashed center markings cleanly.

#### Baseline Road Configuration (`output1/` Directory)

##### 1. Load and Process Static Road Image
![Original road image](./output1/original.jpg)

##### 2. HSV Color Space Transformation (White & Yellow Filtering)
- **Isolated White Filtering (HSV Mask):**
![HSV mask](./output1/hsv_mask.jpg)

- **Isolated Yellow Filtering (Colour Mask):**
![Colour mask](./output1/colour_mask.jpg)

##### 3. Gaussian Blur Mask Output
![Blurred mask](./output1/blurred.jpg)

##### 4. Canny Edge Detection Grid
![Canny edges](./output1/canny_edges.jpg)

##### 5. Region of Interest (ROI) Masking
![ROI edges](./output1/roi_edges.jpg)

##### Successfully Extracted Lane Lines via Hough Transform (Final Output)
![Final lane detection](./output1/lane_lines.jpg)

---

#### Alternative Corridor Configuration (`output/new_image/` Directory)

##### 1. Load and Process Static Road Image (ROI Preview)
![Straight ROI Preview](./output/new_image/roi_preview.jpg)

##### 2. HSV Color Space Transformation
- **Isolated Target Markings:**
![Straight Color Mask](./output/new_image/colour_mask.jpg)

- **Combined Tracking Layers:**
![Straight Combined Edge](./output/new_image/combined_edge_mask.jpg)

##### 3. Gaussian Blur Mask Output
![Straight Blurred Mask](./output/new_image/blurred.jpg)

##### 4. Canny Edge Detection Grid
![Straight Canny Edges](./output/new_image/canny_edges.jpg)

##### 5. Region of Interest (ROI) Masking
![Straight ROI Edges](./output/new_image/roi_edges.jpg)

##### Successfully Extracted Lane Lines via Hough Transform (Final Output)
![Straight Final Lanes Output](./output/new_image/lane_lines.jpg)

---

### Part 2: Curved Road Scenario (`output/image2/` Directory)

#### 1. Load and Process Static Road Image (ROI Preview)
![Curved ROI Preview](./output/image2/roi_preview.jpg)

#### 2. HSV Color Space Transformation
- **Isolated Target Markings:**
![Curved Color Mask](./output/image2/colour_mask.jpg)

- **Combined Tracking Layers:**
![Curved Combined Edge](./output/image2/combined_edge_mask.jpg)

#### 3. Gaussian Blur Mask Output
![Curved Blurred Mask](./output/image2/blurred.jpg)

#### 4. Canny Edge Detection Grid
![Curved Canny Edges](./output/image2/canny_edges.jpg)

#### 5. Region of Interest (ROI) Masking
![Curved ROI Edges](./output/image2/roi_edges.jpg)

#### Successfully Extracted Lane Lines (Final Output)
![Curved Final Lanes Output](./output/image2/lane_lines.jpg)

---

## Limitations
- Performance depends on clear paint visibility and distinct pavement-to-shoulder contrast breaks.
- Extremely sharp right-angle curves or urban intersections can exceed the horizontal boundaries of the sliding search windows.
- The Region of Interest polygon coordinates are manually configured per image; radical camera positioning changes require updated baseline vector dimensions.

## Conclusion
This framework demonstrates a classical computer vision solution built to track lane parameters across diverse driving environments. By leveraging window tracking, directional gradients, Hough transforms, and finite difference math, the system delivers precise path estimation for both straight city streets and winding highways.


