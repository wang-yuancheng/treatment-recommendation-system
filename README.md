# About
This repository contains code and materials for an automated end-to-end ML pipeline that predicts cardiovascular disease (CVD) risk.<br><br>
Click [here](#data-science-workflow) to view the **data science workflow**.<br>
Click [here](#deployment-via-flask) to view the **model deployment via Flask**.<br>
Click [here](#end-to-end-ml-pipeline) to view the **end-to-end ML pipeline**.

## Highlights

- **Automated ML Pipeline (pending)**
  - Data validation & preprocessing  
  - Hyperparameter tuning with Optuna (50 trials)  
  - Final model training using best parameters  
  - Evaluation & benchmark report (metrics, plots)  
  - Artifact tracking & logging via MLflow  
    
- **Manual Deployment**
  - Docker image build & push  
  - Kubernetes manifests for staging & production  
  - Local testing & performance benchmarks
 
- **Data Science Workflow**
  - Data ingestion & exploration  
  - Cleaning & preprocessing  
  - Feature engineering & selection  
  - Modeling & hyperparameter search  
  - Evaluation & reporting  

# Data Science Workflow
- [Introduction](#introduction)
- [Dataset](#dataset)  
- [Data Preparation](#data-preparation)  
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Feature Selection](#feature-selection)  
- [Modelling](#modelling)  
- [Risk Reduction Simulation](#risk-reduction-simulation)  

## Introduction
CVD remains one of the leading causes of death worldwide. This project aims to apply the principles of data science to predict the probability of CVD based on various health indicators.

### Problem Definition
Can we predict whether a person is likely to suffer from cardiovascular disease based on measurable health indicators?
This is a binary classification problem where the target variable is `cardio` (1: presence of CVD, 0: absence).

## Dataset
Link: [Cardiovascular Disease Dataset](https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset)<br>
Author: Svetlana Ulianova<br>
Platform: Kaggle<br>
File: [cardio_train (Original)](data/cardio_train%20(Original).csv)<br>
The dataset consists of 70,000 records of patients data, 11 features + target.<br>

Note: Transformed dataset after feature engineering is [cardio_train](data/cardio_train.csv) 

## Data Preparation
### Data Cleaning
- Removed ID count
- Transformed `age` feature from days to years
- Transformed `height` feature from cm to m
- Removed rows with medically impossible values:<br>
`systolic_bp <= 0, diastolic_bp <= 0, pulse_pressure <= 0, mean_arterial_pressure <= 0`
- Removed data points outside boxplot whiskers using the IQR method
- Reset DataFrame index after row removal

### Feature Engineering
- Added three derived medical features using standard clinical formulas:
    - Body Mass Index (BMI): `BMI= Weight / (Height)^2`
    - Mean Arterial Pressure (MAP): `MAP = (Systolic BP + 2 × Diastolic BP) / 3`
    - Pulse Pressure (PP): `PP = Systolic BP – Diastolic DBP`

<details><summary>For exploratory purposes, we categorize <code>age</code>, <code>BMI</code>, <code>MAP</code>, <code>PP</code> and <code>BP</code> into bins.</summary>
    
  - `age`
    - 18-29
    - 30-39
    - 40-49
    - 50-59
    - 60-69
    - 70+  
  - `Body Mass Index`:
    - **Underweight:** < 18.5 
    - **Normal:** 18.5 – 24.9  
    - **Overweight:** 25 – 29.9 
    - **Obese:** ≥ 30  
  - `Mean Arterial Pressure`:
    - **Low:** < 70 mmHg  
    - **Normal:** 70 – 100 mmHg  
    - **High:** > 100 mmHg 
  - `Pulse Pressure`:
    - **Low:** < 40 mmHg  
    - **Normal:** 40 – 60 mmHg  
    - **High:** > 60 mmHg  
  - `Blood Pressure`:
    - **Normal**  
      - Systolic: < 120 mmHg  
      - Diastolic: < 80 mmHg  
    - **Elevated**  
      - Systolic: 120 – 129 mmHg  
      - Diastolic: < 80 mmHg  
    - **Hypertension Stage 1**  
      - Systolic: 130 – 139 mmHg  
      - Diastolic: 80 – 89 mmHg  
    - **Hypertension Stage 2**  
      - Systolic: ≥ 140 mmHg  
      - Diastolic: ≥ 90 mmHg  
    - **Hypertensive Crisis**  
      - Systolic: > 180 mmHg  
      - Diastolic: > 120 mmHg
          
  </details>
  
### Encoding
Encoded ordinal variables `cholesterol_level` `glucose_level` using one-hot encoding<br>
Scaled continuous variables `age` `BMI` `SBP` `DBP` using MinMaxScaler
  
## Exploratory Data Analysis
### Univariate Analysis
### Bivariate Analysis
### Data Visualization
### Insights

## Feature Selection
Selected `cholesterol_level` `glucose_level` `age` `BMI` `SBP` `DBP` for model input.<br>
Dropped height and weight because BMI already captured that information.<br>
Dropped derived variables like MAP and Pulse Pressure to reduce redundancy.

## Modelling
### Algorithms Used
### Evaluation Metrics
### Results
### Model Training

## Risk Reduction Simulation



# Deployment via Flask
- [Deployment](#deployment)  
- [Usage](#usage)  
- [Technologies](#technologies)

## Deployment
### Preprocessing Pipeline
Created a pipeline to automate the scaling + encoding + modeling

## Usage

## Technologies



# End-to-End ML pipeline
- [NIL](#-)  
- [NIL](#-)  
- [NIL](#-)
