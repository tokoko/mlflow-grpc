import numpy as np
import mlflow
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import shutil
import os
from mlflow.models import infer_signature

# Load the diabetes dataset
diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True, as_frame=True)

print(diabetes_X)

# # Use only one feature
# diabetes_X = diabetes_X[:, np.newaxis, 2]

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(diabetes_X, diabetes_y)

# Persist model in mlflow format
if os.path.exists('model'):
    shutil.rmtree('model')

mlflow.sklearn.save_model(regr, 'model')

# # Make predictions using the testing set
diabetes_y_pred = regr.predict(diabetes_X)

# print(diabetes_y_pred)

print(infer_signature(diabetes_X, diabetes_y))