# 🛰️ **TopoVision — 3D Topographic Analysis System**

> A Python-based system for topographic data visualization, real-time analysis, and calculus-based gradient computation.

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://img.shields.io/pypi/v/topovision.svg)](https://pypi.org/project/topovision/)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/JalaU-Capstones/topovision/actions)

📦 **Repository:** [https://github.com/JalaU-Capstones/topovision.git](https://github.com/JalaU-Capstones/topovision.git)

---

## 🧭 **Overview**

**TopoVision** is a collaborative academic project developed as part of the **Calculus II course** at *Universidad Jala*.
The system combines **Computer Vision**, **Numerical Methods**, and **Topographic Analysis** to calculate and visualize slopes, gradients, and surface volumes in real time.

The main goal is to create a tool that connects mathematical theory with visual and spatial understanding — transforming multivariable calculus into an interactive experience.

---

## ✨ **What's New in Version 0.2.1**

This version introduces a complete unit conversion and perspective calibration system, making TopoVision a more accurate and user-friendly tool for real-world analysis.

*   **Unit Conversion System**: All calculations and measurements can now be displayed in various units (meters, feet, etc.).
*   **Perspective Calibration**: A new calibration tool allows you to correct for perspective distortion by defining a real-world rectangle, ensuring all measurements are dimensionally accurate.
*   **Interactive Tutorials**: A new event-driven tutorial system guides first-time users through the application's key features.
*   **Improved UI**: The user interface has been refactored for a more stable and responsive layout.
*   **Enhanced Visualizations**: The gradient heatmap and 3D plot now correctly handle perspective and aspect ratio, providing clearer and more accurate visualizations.

---

## ⚙️ **Key Features**

*   🎥 Real-time video capture using OpenCV
*   📏 **Unit Conversion**: Display results in meters, feet, kilometers, etc.
*   📐 **Perspective Calibration**: Correct for perspective distortion for accurate measurements.
*   🧮 Numerical computation of partial derivatives, gradients, arc length, and volume.
*   ✨ **Dynamic 3D Surface Plots**: Interactive visualization of topographic data.
*   🗺️ **Gradient Heatmaps**: Clear visualization of slope and steepness.
*   🖱️ Interactive region selection on the GUI.
*   🧠 **Interactive Tutorials**: Guides first-time users through the application.
*   📦 Easy installation via PyPI.

---

## 🖼️ **Visualizations**

TopoVision offers rich and interactive 3D visualizations to help understand complex topographic data.

### Dynamic 3D Surface Plots

Experience real-time rendering of surfaces, allowing you to observe changes in elevation and features interactively.

![3D Surface Plot Screenshot](docs/images/3d_surface_plot.gif)

---

## 🚀 **Quick Start**

### Installation from PyPI

```bash
pip install topovision
```

### Run the application

```bash
python -m topovision
```

Or simply:

```bash
topovision
```

You should see a GUI window with a welcome tutorial guiding you to press the **"Open Camera"** button.

---

## 📋 **System Requirements**

### Required
- **Python 3.11** or higher
- **Tkinter** (GUI toolkit)

### Tkinter Installation

Tkinter comes pre-installed with Python on **Windows** and **macOS**.

On **Linux**, you may need to install it manually:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-tkinter
```

**Arch Linux:**
```bash
sudo pacman -S tk
```

---

## 🛠️ **Installation Options**

### Standard Installation
Includes all features and GUI support:
```bash
pip install topovision
```

### Development Installation
Includes testing, linting, and documentation tools:
```bash
pip install topovision[dev]
```

### Lightweight Installation
Minimal dependencies without OpenCV GUI components:
```bash
pip install topovision[light]
```

### Installation from Source

For developers who want to contribute or modify the code:

```bash
# Clone the repository
git clone https://github.com/JalaU-Capstones/topovision.git
cd topovision

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate      # macOS/Linux
# OR
.venv\Scripts\activate         # Windows

# Install in editable mode
pip install -e .

# Or install with dev dependencies
pip install -e .[dev]
```

---

## 🧩 **Project Structure**

```
topovision/
├── src/
│   └── topovision/
│       ├── __init__.py
│       ├── __main__.py
│       ├── app.py
│       ├── core/
│       │   ├── interfaces.py
│       │   └── models.py
│       ├── capture/
│       │   └── ...
│       ├── calculus/
│       │   ├── calculus_module.py
│       │   └── strategies.py
│       ├── visualization/
│       │   ├── visualizers.py
│       │   └── plot3d.py
│       ├── gui/
│       │   ├── gui_module.py
│       │   ├── analysis_panel.py
│       │   └── ...
│       ├── services/
│       │   └── task_queue.py
│       ├── utils/
│       │   ├── math.py
│       │   ├── units.py
│       │   └── perspective.py
│       └── tests/
│           └── ...
├── docs/
│   ├── architecture.md
│   ├── user-guide.md
│   └── ...
├── pyproject.toml
├── README.md
└── ...
```

---

## 🧰 **Tech Stack**

| Layer                | Technology           |
| -------------------- | -------------------- |
| Language             | Python 3.11          |
| GUI                  | Tkinter              |
| Computer Vision      | OpenCV               |
| Numerical Analysis   | NumPy                |
| Visualization        | Matplotlib           |
| Documentation        | Markdown             |
| Testing              | Pytest               |
| Linting / Formatting | Flake8, Black, Mypy  |
| Version Control      | GitHub (GitHub Flow) |
| Distribution         | PyPI                 |

---

## 🎯 **Usage Examples**

### Basic Usage

```python
# After installation, simply run:
python -m topovision

# Or use the command directly:
topovision
```

---

## 🧮 **Core Functionalities (Mathematical Overview)**

| Feature                   | Description                                         | Method                      |
| :------------------------ | :-------------------------------------------------- | :-------------------------- |
| Partial Derivatives       | Calculated using finite difference methods          | Central Difference Scheme   |
| Gradient Vector           | Visualized as a heatmap                             | Sobel Operator              |
| Volume Calculation        | Computed with discrete Riemann sums                 | Trapezoidal Rule            |
| Arc Length Calculation    | Calculated as the sum of Euclidean distances        | Vectorized NumPy operations |
| 3D Surface Visualization  | Dynamic and interactive 3D plots of topographic surfaces | Matplotlib + NumPy          |
| Perspective Correction    | Uses a 4-point homography to correct for perspective | OpenCV `getPerspectiveTransform` |

---

## 🧩 **Development Workflow — GitHub Flow**

### 🌿 Main Branches

| Branch      | Purpose                      |
| ----------- | ---------------------------- |
| `main`      | Stable release branch        |
| `develop`   | Integration branch           |
| `feature/*` | Individual development tasks |
| `hotfix/*`  | Urgent fixes                 |
| `docs/*`    | Documentation-only updates   |

### 💬 Commit Convention

Follow **Conventional Commits** format:

```
<type>(<scope>): <description>
```

---

## 🧪 **Testing**

Run the test suite:

```bash
# Install with dev dependencies
pip install topovision[dev]

# Run tests
pytest

# Run with coverage
pytest --cov=topovision
```

---

## 👥 **Team Members**

| Name                             | Role                                |
| -------------------------------- | ----------------------------------- |
| **Alejandro Botina Herrera**     | Technical Lead & System Architect   |
| **Andreina Olivares Cabrera**    | Interface Developer & Documentation |
| **Jonathan Joel Ruviño**         | Testing & Numerical Computation     |
| **Kiara Vanessa Muñoz Bayter**   | Environment Setup & Visualization   |
| **Víctor Manuel Barrero Acosta** | Capture Systems & Demonstrations    |

---

## 🧾 **License**

This project is licensed under the **Apache License 2.0**.
See the [LICENSE](LICENSE) file for more details.

---

## 🔗 **Links**

- **PyPI Package:** https://pypi.org/project/topovision/
- **GitHub Repository:** https://github.com/JalaU-Capstones/topovision
- **Issue Tracker:** https://github.com/JalaU-Capstones/topovision/issues
- **Documentation:** [docs/](docs/)

---

🎯 *TopoVision — bridging the gap between Calculus and reality, one frame at a time.*

---
