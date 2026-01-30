# Point2CAD – Point Cloud to CAD Solid Reconstruction

## 📌 Overview
Point2CAD is a reverse-engineering pipeline that converts a **3D point cloud** into:
- **Triangle Mesh** (PLY / OBJ / STL) for visualization
- **Parametric CAD Solid** (STEP) using inferred geometric primitives

The project follows **industry-standard Scan-to-CAD methodology**, separating **mesh reconstruction** from **design-intent reconstruction**.

---

## 🎯 Objectives
- Preprocess raw point cloud data
- Segment geometric primitives (planes, cylinders)
- Fit mathematical primitives
- Infer missing features (middle connector)
- Construct parametric CAD solids
- Export manufacturable STEP files

---

## 🧠 Core Concept
There are two different representations used:

| Representation | Purpose | Output |
|----------------|--------|--------|
| Triangle Mesh | Visualization | `.ply`, `.obj`, `.stl` |
| Parametric CAD | Manufacturing | `.step` |

> Meshes approximate surfaces.  
> CAD solids represent geometry mathematically.

---

## PipeLine OverView

Raw Point Cloud (.ply)
        ↓
Preprocessing (denoise, downsample, normalize)
        ↓
Segmentation (planes & cylinders)
        ↓
Primitive Fitting (axis, radius, height)
        ↓
Design Intent Inference (connector cylinder)
        ↓
Parametric CAD Construction (pythonOCC)
        ↓
STEP Export (final_solid.step)

---

## 📂 Project Structure
point2cad-project/
├── data/
│   ├── raw_pointcloud/
│   │   └── input.ply
│   ├── segmented/
│   │   └── plane_*.ply
│   └── outputs/
│       ├── final_mesh.ply
│       ├── final_mesh.stl
│       └── final_solid.step
│
├── src/
│   ├── preprocessing/
│   │   ├── denoise.py
│   │   ├── downsample.py
│   │   ├── normalize.py
│   │   └── save.py
│   │
│   ├── segmentation/
│   │   ├── ransac_segmentation.py
│   │   └── cylinder_segmentation.py
│   │
│   ├── primitive_fitting/
│   │   ├── plane_fitting.py
│   │   ├── cylinder_fitting.py
│   │   └── sphere_fitting.py
│   │
│   ├── mesh_reconstruction/
│   │   └── pointcloud_to_mesh.py
│   │
│   ├── topology/
│   │   └── cad_builder.py
│   │
│   ├── cad_export/
│   │   └── step_export.py
│   │
│   └── visualization/
│       └── viewer.py
│
├── main.py
├── requirements.txt
└── README.md

---

## 🔧 Pipeline Explanation

### 1. Preprocessing
- Noise removal
- Voxel downsampling
- Normal estimation

📁 `src/preprocessing/`

---

### 2. Segmentation
- Plane detection (RANSAC)
- Cylinder candidate extraction using normal consistency

📁 `src/segmentation/`

---

### 3. Primitive Fitting
For each detected cylinder:
- Axis direction
- Center point
- Radius
- Height

📁 `src/primitive_fitting/`

---

### 4. Design Intent Inference
The middle connector is **not reliably present in the scan**.

Instead of mesh filling:
- Connector geometry is **inferred mathematically**
- Based on detected cylinder parameters

📁 `src/topology/cad_builder.py`

---

### 5. CAD Solid Construction
- Base solid creation
- Cylindrical hole cutting
- Connector fusion
- Boolean operations

Uses **pythonOCC (OpenCASCADE)**.

---

### 6. Mesh Reconstruction (Optional)
- Poisson surface reconstruction
- Used only for visualization

📁 `src/mesh_reconstruction/`

---

### 7. Export
- Mesh → PLY / OBJ / STL
- CAD Solid → STEP

📁 `src/cad_export/`

---

## 📤 Outputs

| File | Description |
|-----|------------|
| `final_mesh.ply` | Triangle mesh |
| `final_mesh.stl` | Printable mesh |
| `final_solid.step` | Parametric CAD solid |

---

## 🧪 Technologies Used
- Python
- Open3D
- NumPy / SciPy
- pythonOCC (OpenCASCADE)
- VS Code + Anaconda

---

## ⚠️ Limitations
- Scanned point clouds may contain holes
- Mesh reconstruction cannot recover missing design intent
- CAD inference requires geometric assumptions

---

## 🏭 Industry Relevance
This workflow mirrors:
- CATIA Scan-to-3D
- Siemens NX Reverse Engineering
- SolidWorks Feature Recognition

---

## ▶️ How to Run

```bash
conda activate point2cad
python main.py

