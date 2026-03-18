# 🎨 Virtual Vision Canvas: Gesture-Based Digital Art

---

## 📌 Project Overview
**Virtual Vision Canvas** is an interactive Human-Computer Interaction (HCI) application that transforms your hand into a digital paintbrush. Leveraging **MediaPipe's High-Fidelity Hand Tracking** and **OpenCV**, this system tracks real-time skeletal landmarks to draw on a live webcam feed without the need for physical hardware like a mouse or stylus.

### 🌟 Key Features
* **Real-time Hand Tracking:** Uses MediaPipe’s 21-point landmark model for sub-millisecond latency and high precision.
* **Intelligent Mode Switching:**
    * **Drawing Mode:** Activated when the index finger is raised (uses coordinate tracking to draw lines).
    * **Hover/Selection Mode:** Activated when both index and middle fingers are raised (disengages the "pen" to move across the screen).
* **Seamless Frame Blending:** Employs advanced **Bitwise Operations** and **Inverse Masking** to merge the drawing canvas with the live video stream.
* **Mirror-Safe Experience:** Automatically flips the camera feed horizontally for an intuitive user experience.

---

## 🛠️ Technical Architecture

### 1. Data Pipeline
1.  **Capture:** BGR Frame input via OpenCV (`cv2.VideoCapture`).
2.  **Preprocessing:** Horizontal flip + BGR to RGB conversion for MediaPipe processing.
3.  **Inference:** MediaPipe Hand Landmarker identifies 21 3D coordinates.
4.  **Logic Engine:**
    * Tracks **Landmark 8** (Index Tip) for drawing.
    * Compares Y-coordinates of **Landmark 8** and **Landmark 12** (Middle Tip) to toggle drawing states.
5.  **Rendering:** Merges a secondary `numpy` black canvas with the live frame using `cv2.bitwise_or`.

### 2. Gesture Logic
| Gesture | State | Visual Feedback |
| :--- | :--- | :--- |
| Index Finger UP | **Drawing Mode** | Magenta circle + Green Line |
| Index & Middle UP | **Hover Mode** | Red circle (No line drawn) |
| Press 'q' | **Exit** | Closes Application |

---

🚀 Getting Started
Prerequisites
Python 3.11+

A working Webcam.

Installation
Clone the Repository:

Bash
git clone [https://github.com/duderrandom/virtual-canvas.git](https://github.com/duderrandom/virtual-canvas.git)
cd virtual-canvas
Install Dependencies:

Bash
pip install opencv-python mediapipe numpy
Run the Application:

Bash
python src/main.py
📈 Future Roadmap
[ ] Dynamic Color Palette: Gesture-based color selection (Red, Blue, Yellow).

[ ] Eraser Gesture: Detect a "fist" or "palm" gesture to clear the canvas.

[ ] Canvas Export: Press 'S' to save the final artwork as a .png.

[ ] Thickness Control: Use the distance between thumb and index finger to adjust line weight.

---

## 📂 Repository Structure
```text
virtual-vision-canvas/
├── src/
│   └── main.py           # Core logic for tracking and drawing
├── assets/               # Demo GIFs and screenshots
├── .gitignore            # Excludes venv, pycache, and system files
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
