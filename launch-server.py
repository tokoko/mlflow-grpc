from mlflow.pyfunc import load_model
from mlflow_grpc.server import serve
from mlflow_grpc.backend import PyFuncGrpcBackend
from mlflow.models import Model, infer_signature
from sklearn import datasets, linear_model
import shutil
import os
import mlflow


model_path = 'model'

diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True, as_frame=True)

regr = linear_model.LinearRegression()
regr.fit(diabetes_X, diabetes_y)

if os.path.exists('model'):
    shutil.rmtree('model')

mlflow.sklearn.save_model(regr, 'model', signature=infer_signature(diabetes_X, diabetes_y))

model = Model.load(model_path)

backend = PyFuncGrpcBackend(
    config=model.flavors['python_function'],
    workers=1,
    no_conda=True,
    install_mlflow=True
)

backend.serve(model_path, port='9000', host='localhost')

