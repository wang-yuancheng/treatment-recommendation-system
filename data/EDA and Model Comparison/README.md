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
The dataset consists of 70,000 records of patients data, 11 features + target.<br>

Link: [Cardiovascular Disease Dataset](https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset)<br>
Author: Svetlana Ulianova<br>
Platform: Kaggle<br>
File: [cardio_train (Original)](data/cardio_train%20(Original).csv)<br>

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
Below are just a few visualizations, more in-depth analysis and charts can be found in the [EDA notebook](IE0005%20Group%20Project%20Code.ipynb).
### Univariate Analysis
![Chart](assets/Count%20Plot%20for%20Cardio.png)
### Insights
- This count plot shows that the dataset is relatively balanced, as it has a similar number of individuals with and without cardiovascular disease, which is good for training predictive models.

### Bivariate Analysis
![Chart](assets/%25%20of%20individuals%20with%20cardio%20in%20each%20category%201.png)
![Chart](assets/%25%20of%20individuals%20with%20cardio%20in%20each%20category%202.png)
### Insights
- Higher CVD proportions are observed among older age groups. <br>
- Clinical variables like blood pressure, BMI, mean arterial pressure, pulse pressure, cholesterol, and glucose levels show strong patterns: individuals in higher-risk categories consistently have a higher percentage of cardiovascular disease.<br>
- Interestingly, inactive individuals and those who consume alcohol or smoke show similar CVD prevalence when compared to those who are active, and those who do not consume alcohol or smoke.

<details><summary>📊 Percentage of Individuals with Cardiovascular Disease by Category</summary>

#### 🩺 Blood Pressure Category
- **Hypertension Stage 2**: 79.28%
- **Hypertension Stage 1**: 43.78%
- **Elevated Blood Pressure**: 32.48%
- **Normal Blood Pressure**: 23.71%

#### ⚖️ BMI Category
- **Obesity**: 58.04%
- **Overweight**: 49.11%
- **Normal weight**: 39.61%
- **Underweight**: 29.83%

#### 💓 Mean Arterial Pressure Category
- **High MAP**: 78.07%
- **Normal MAP**: 38.11%
- **Low MAP**: *nan%*

#### 🔁 Pulse Pressure Category
- **High Pulse Pressure**: 81.36%
- **Normal Pulse Pressure**: 49.20%
- **Low Pulse Pressure**: 29.09%

#### 🩸 Cholesterol Category (1 = Normal, 2 = Above Normal, 3 = Well Above Normal)
- **3**: 74.98%
- **2**: 57.03%
- **1**: 42.04%

#### 🍬 Glucose Category (1 = Normal, 2 = Above Normal, 3 = Well Above Normal)
- **3**: 60.19%
- **2**: 55.27%
- **1**: 45.82%

#### 🚬 Smoking Status
- **1 (Smokes)**: 43.46%
- **0 (Does Not Smoke)**: 47.91%

#### 🍺 Alcohol Consumption
- **1 (Drinks)**: 44.53%
- **0 (Does Not Drink)**: 47.69%

#### 🏃 Physical Activity
- **1 (Exercises)**: 46.53%
- **0 (Does Not Exercise)**: 51.65%

#### 📅 Age Category
- **60–69**: 64.45%
- **50–59**: 48.20%
- **40–49**: 35.47%

#### 🚻 Gender
- **2 (Men)**: 47.32%
- **1 (Women)**: 47.65%
</details>

### Multivariate Analysis
Extracted from [Individual Model Comparison](Individual%20Model%20Comparison.ipynb)
![Heatmap](assets/Correlation%20Heatmap.png)
### Insights
### 📊 Correlation Heatmap Analysis

This heatmap illustrates the Pearson correlation between various features and the target variable `cardiovascular_disease`.

---

#### 🔺 Top Positively Correlated Features with Cardiovascular Disease
- **Systolic Blood Pressure (`systolic_bp`)**: 0.41
- **Mean Arterial Pressure (`mean_arterial_pressure`)**: 0.39
- **Diastolic Blood Pressure (`diastolic_bp`)**: 0.33
- **Pulse Pressure (`pulse_pressure`)**: 0.31
- **Age (`age_years`)**: 0.23
- **Body Mass Index (`body_mass_index`)**: 0.17

These moderate positive correlations suggest that individuals with higher blood pressure, higher BMI, and older age are more likely to have cardiovascular disease.

---

#### 🧪 Lab Indicators (Cholesterol and Glucose Levels)
- **Cholesterol Level 3 (Well Above Normal)**: 0.19
- **Cholesterol Level 2 (Above Normal)**: 0.07
- **Glucose Level 2**: 0.08  
- **Glucose Level 3**: 0.07

These indicators show smaller, yet noticeable positive correlations with cardiovascular disease, indicating some association with elevated risk.

---

#### ⚠️ Weak or Negligible Correlation Features
- **Smoking Status**: 0.03
- **Alcohol Consumption**: 0.01
- **Physical Activity**: 0.04
- **Gender**: 0.05

These variables show weak linear correlation with cardiovascular disease, though they may still contribute value in non-linear models or through interaction effects.

---

#### 🔗 Notable Inter-Feature Correlations (Multicollinearity Risk)
- **Systolic vs. Diastolic Blood Pressure**: 0.76  
  Although strongly correlated, both provide distinct clinical information: **systolic pressure** reflects the force during heartbeats, while **diastolic pressure** measures pressure between beats. Retaining both can be valuable for models interpreting cardiovascular function more holistically.
- **BMI vs. Weight**: 0.84  
  High correlation suggests redundancy, as BMI is derived from weight and height. Consider keeping only one or evaluating their individual predictive power.
- **MAP vs. BP Values**: > 0.90  
  Mean Arterial Pressure is a derived metric from systolic and diastolic values. It may be excluded to reduce redundancy unless it offers clearer interpretability or predictive strength.

## Feature Selection
From the above findings, we identified the following features as most relevant for predicting cardiovascular disease:

- **Age**
- **BMI**
- **Systolic Blood Pressure (SBP)**
- **Diastolic Blood Pressure (DBP)**
- **Cholesterol Level**
- **Glucose Level**

These features showed meaningful correlation with the target variable and are retained as inputs for model training.

To reduce redundancy and improve model efficiency:
- We **dropped `height` and `weight`**, since **BMI** already captures that relationship.
- We **excluded derived variables** like **Mean Arterial Pressure (MAP)** and **Pulse Pressure**, which are calculated from SBP and DBP, to avoid multicollinearity.

## Modelling
### Algorithms Used
### Evaluation Metrics
### Results
![Chart](assets/Model%20Comparison%20%28Test%20Accuracy%29.png)
![Chart](assets/Model%20Comparison%20%28Recall%29.png)
![Chart](assets/Model%20Comparison%20%28ROC%20AUC%29.png) 
### Model Training

## Risk Reduction Simulation
