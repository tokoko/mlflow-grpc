import numpy as np
import mlflow
from sklearn import datasets, linear_model
from mlflow.models import infer_signature
import pyarrow as pa




# Load the diabetes dataset
diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True, as_frame=True)


model_signature = infer_signature(diabetes_X, diabetes_y)

pa_schema = pa.Schema.from_pandas(diabetes_X)

print(model_signature)
print(pa_schema)
