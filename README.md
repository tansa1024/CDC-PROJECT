# Satellite Imagery-Based Property Valuation

A **Multimodal Regression Pipeline** that predicts property market values by fusing traditional tabular data (square footage, bedrooms, etc.) with high-resolution satellite imagery. This project quantifies "curb appeal" and environmental context through **Computer Vision**.

## Key Features
* **Automated Data Acquisition:** Programmatic fetching of satellite images using Latitude/Longitude via Mapbox/Google Maps Static APIs.
* **Multimodal Fusion:** A dual-branch neural network architecture combining **CNN-extracted visual embeddings** with dense tabular layers.
* **Geospatial Insights:** Analysis of "neighborhood density" and green cover impact on property value.
* **Model Explainability:** Implementation of **Grad-CAM** to visualize which visual features (e.g., Trees, road density) drive price predictions.

## Tech Stack
* **GIS Engine:** Esri ArcGIS (ArcGIS API for Python)
* **Deep Learning:** PyTorch, Torchvision
* **Data Analysis:** Pandas (Spatially Enabled DataFrames), NumPy, Scikit-learn
* **Visualization:** Matplotlib, ArcGIS Pro Map Viewer

## Setup & Installation
Follow these steps to set up your environment in **VS Code** with **GPU support** using `pip`.

1. Create a Virtual Environment
Open your terminal in VS Code and run:
```bash
# Create the environment
python -m venv venv
```

2. Activate the environment
```bash
On Windows:
.\venv\Scripts\activate
On macOS/Linux:
source venv/bin/activate
```
3. Install PyTorch with GPU Support: 
To ensure PyTorch uses your NVIDIA GPU, install it using the specific CUDA index (adjust cu121 to your CUDA version if necessary):
```bash
pip install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu121](https://download.pytorch.org/whl/cu121)
```
3. Install Dependencies
```bash
pip install pandas numpy matplotlib openpyxl scikit-learn joblib
```
4. ArcGIS API Configuration
The data_fetcher.py script requires your ArcGIS credentials to fetch satellite imagery:
```bash
from arcgis.gis import GIS
https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{ZOOM_LEVEL}/{y}/{x}
```

## Model Architecture

The system utilizes a **Late Fusion Strategy** to integrate heterogeneous data sources.

1.  **Vision Branch (CNN):** A pre-trained **ResNet-50** extracts spatial features from 224x224 satellite chips.
2.  **Tabular Branch (MLP):** A Multi-Layer Perceptron processes normalized house metadata (sqft, grade).
3.  **Fusion Head:** Concatenates visual and tabular embeddings into a single vector to regress the final **Price**.

## Results & Performance Evaluation

The performance of the **Multimodal Model** was benchmarked against a baseline **Tabular-only** regressor.

### 1. Quantitative Comparison
| Model Architecture | Mean Absolute Error (MAE) | R² Score |
| :--- | :--- | :--- |
| **Baseline (Tabular Data Only)** | $130014 | 0.86 |
| **Multimodal (Tabular + Satellite)** | **$166,183** | **0.76** |

*Note: The Multimodal approach showed significant error increase in high-density urban areas and properties with specific visual features like green cover or waterfronts.*

### 2. Model Explainability (Grad-CAM)
To ensure the model was learning relevant spatial features rather than noise, we implemented **Grad-CAM**. This highlights the areas in the satellite images that most influenced the price prediction.



**Key Observations:**
* **Positive Value Drivers:** Large canopy cover (trees), proximity to blue spaces (water), and low road density in suburban areas.
* **Negative Value Drivers:** Industrial proximity, high concrete density, and poor "curb appeal" signatures.
