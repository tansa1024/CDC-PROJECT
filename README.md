CDC-PROJECT

Multimodal Real Estate Price Prediction

This project implements a multimodel regression pipeline that combines traditional tabular house data with satellite imagery to predict property valuations. Performance Summary

Tabular-Only R²: 0.86 and RSME: $130014

Multimodal R²:0.76 and RMSE:$166,183.80.

Model Architecture

The architecture fuses two distinct streams:

*CNN Branch (ResNet-18): Processes 224x224 satellite images to extract 512 visual features.

*MLP Branch: Processes tabular features (sqft, bedrooms, etc.) into a 64-dimensional vector.

*Fusion Layer: Concatenates both streams into a feature vector for final price regression.

Setup & Installation

Environment Requirements

*Virtual environment with kernel Python 3.12.5 (Done in VS CODE)

*Install necessary libraries as shown in the Jupyter notebook

*There is a different version of PyTorch for GPU support. Install the necessary library(I have used GPU)

How To RUN

*Preprocessing: Ensure house prices are log-transformed ($log(1+x)$) to stabilise training.

*Training: Run the training loop for 20 epochs with a learning rate of 1e-4.Increase the epochs if not satisfied with r2 value

*Grad-CAM: Use the generate_final_gradcam function to visualise what the model is "looking at".
