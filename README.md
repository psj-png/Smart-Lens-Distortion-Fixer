# Smart-Lens-Distortion-Fixer
> **iPhone 13 Pro Ultra-Wide Lens Distortion Correction Project using OpenCV**

This project aims to mathematically analyze the strong Barrel Distortion occurring in the iPhone 13 Pro's 0.5x ultra-wide lens through camera calibration and restore it to a Perspective Model.

---

## 1. Introduction
* **Objective**: Correct geometric distortion in wide-angle lenses to restore curved lines into straight lines.
* **Tools**: Python, OpenCV, NumPy, SciPy
* **Target**: iPhone 13 Pro 0.5x Ultra-Wide Lens

---

## 2. Data Acquisition Strategy
Data reliability was enhanced by strictly adhering to **'Good Calibration'** guidelines.
* **Maintaining Flatness**: To prevent errors in 3D points ($X_i$), the chessboard pattern was attached to a rigid, flat surface during filming.
* **Motion Blur Suppression**: To reduce observation noise during corner detection, frames were captured while keeping both the camera and the pattern board as stationary as possible.
* **Maximizing Coverage**: To ensure the accuracy of peripheral lens parameters, the pattern was filmed to sufficiently cover not only the center but also the four corners (edges) of the frame.
* **Utilizing Perspective Cues**: To derive precise intrinsic parameters, the board and camera were tilted at various angles rather than kept perfectly parallel, incorporating vanishing point information.

---

## 3. Rectification Analysis
The key success points of the correction results, based on the calculated distortion coefficients, are as follows:

### Key Correction Points
1. **Barrel Distortion Removal**
   * **Original**: Due to the fisheye effect characteristic of wide-angle lenses, straight lines at the edges of the image appear curved outward.
   * **Fixed**: Through a mathematical Undistort Map, the previously curved lines are restored to be flat, aligning with straight-line guidelines.

2. **Projection Model Transformation (Equidistance to Perspective)**
   * The original video based on the Equidistance model is re-projected into a Perspective model (Pinhole Camera) to ensure that straight-line components in 3D space remain straight on the image plane.

3. **Field of View (FOV) Optimization**
   * To handle the black borders that occur after correction, an Optimal New Camera Matrix was calculated to extract only the valid image area where distortion has been removed.

---

## 4. Results
Below is the comparison between the original (Original) and the corrected (Fixed) screens.

![Calibration Demo](comparison.gif) 

---
