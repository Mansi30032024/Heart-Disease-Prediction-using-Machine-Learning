# -*- coding: utf-8 -*-
"""heartDisease.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1f4MOL9yGkSCZqj7qRT8Majgj4L5WGCmd

Importing Libraries
"""

import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

"""Importing Dataset"""

heart_data = pd.read_csv("/content/heart_2020_cleaned.csv")

heart_data.head(6)

heart_data.shape

#checking for missing
heart_data.isnull().sum()

heart_data.info()

heart_data.describe()

#checking distribution of Target Variable
heart_data['HeartDisease'].value_counts()

X= heart_data.drop(columns='HeartDisease', axis=1)
Y= heart_data['HeartDisease']
print(X)

print(Y)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
categorical_cols = ['HeartDisease', 'Smoking', 'AlcoholDrinking', 'Stroke',
                    'DiffWalking', 'PhysicalActivity', 'Asthma', 'KidneyDisease',
                    'SkinCancer']
for col in categorical_cols:
    heart_data[col] = le.fit_transform(heart_data[col])

# selecting all the rows [:]...........selecting all columns except first col
X= heart_data.iloc[: , 1:].values
Y= heart_data.iloc[: ,0].values
print(X)

print(Y)

"""SPLITTING DATA INTO TRAINING AND TEST SET"""

# do not run this
#X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

X = heart_data.drop(columns='HeartDisease', axis=1)
Y = heart_data['HeartDisease']
# one-hot encoding on categorical features
categorical_cols = ['Smoking', 'AlcoholDrinking', 'Stroke', 'DiffWalking', 'PhysicalActivity', 'Asthma', 'KidneyDisease', 'SkinCancer','Sex','Race','Diabetic','GenHealth','AgeCategory']
X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)  # Now this should work

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

print(X.shape, X_train.shape, X_test.shape)

print(X_train)

print(X_test)

print(Y_train)

print(Y_test)

"""Feature Scaling(we need feature scaling to prevent some features to be dominated by others features)"""

from sklearn.preprocessing import StandardScaler
sc =  StandardScaler()
X_train

"""converting categorical columns into numerical columns using one-hot encoding. The drop_first=True part avoids creating redundant columns.

Logistic Regression: A baseline linear model for binary classification.
"""

model = LogisticRegression()

# Create and train the model
#model = LogisticRegression()
model.fit(X_train, Y_train)

# Make predictions and evaluate the model
X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)*100
print(f"Training data accuracy: {training_data_accuracy:.2f}%")

#X = heart_data.drop(columns=['HeartDisease'])
#y = heart_data['HeartDisease']

# Encode target if it's categorical (e.g., 'Yes' and 'No')
#y = y.map({'Yes': 1, 'No': 0})  # Convert 'Yes' to 1 and 'No' to 0

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Convert data into DMatrix, the format used by XGBoost
train_data = xgb.DMatrix(X_train, label=y_train)
test_data = xgb.DMatrix(X_test, label=y_test)

# Set parameters for the XGBoost model
params = {
    'objective': 'binary:logistic',  # Binary classification
    'max_depth': 4,                 # Maximum depth of each tree
    'eta': 0.3,                     # Learning rate
    'eval_metric': 'logloss',       # Evaluation metric
}

# Train the XGBoost model
bst = xgb.train(params, train_data, num_boost_round=100)

# Make predictions
y_pred_proba = bst.predict(test_data)  # Probabilities
y_pred = (y_pred_proba > 0.5).astype(int)  # Convert probabilities to binary predictions

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

"""RANDOM FOREST ALGO"""

# Initialize Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred)*100)
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

plt.figure(figsize=(8, 6))
sns.scatterplot(data=heart_data, x='BMI', y='PhysicalHealth', hue='HeartDisease', alpha=0.7)

# Plot labels and title
plt.title('Scatter Plot: BMI vs PhysicalHealth (Colored by HeartDisease)', fontsize=14)
plt.xlabel('BMI', fontsize=12)
plt.ylabel('PhysicalHealth', fontsize=12)
plt.legend(title='Heart Disease')
plt.grid(True)

plt.show()

heart_data.hist(['Smoking', 'AlcoholDrinking', 'Stroke', 'DiffWalking', 'PhysicalActivity', 'Asthma', 'KidneyDisease', 'SkinCancer','Sex','Race','Diabetic','GenHealth','AgeCategory'],figsize=(18,8))

heart_data.hist(['HeartDisease'],figsize=(18,8))

"""DECISON TREE CLASSIFIER"""

from sklearn.tree import DecisionTreeClassifier

model2= DecisionTreeClassifier()
model2.fit(X_train, Y_train)
print(f"Decision Tree Score: {model2.score(X_test,Y_test)*100}")
X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)*100
print(f"Accuracy of model : {training_data_accuracy}")

"""K NEAREST NIEGHBORS"""

from sklearn.neighbors import KNeighborsClassifier
#creat and train model
knn_model=KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train,Y_train)

Y_pred_knn=knn_model.predict(X_test)
accuracy_knn=accuracy_score(Y_test,Y_pred_knn)*100
print(f"KNN accuracy: {accuracy_knn:.2f}%")