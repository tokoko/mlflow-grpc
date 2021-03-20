from mlflow.pyfunc import load_model
from mlflow_grpc.server import serve
from mlflow_grpc.backend import PyFuncGrpcBackend
from mlflow.models import Model
from mlflow.models.flavor_backend_registry import get_flavor_backend

model_path = 'model'

model = Model.load(model_path)

backend = PyFuncGrpcBackend(
    config=model.flavors['python_function'],
    workers=1,
    no_conda=False,
    install_mlflow=True
)

backend.serve(model_path, port='9000', host='localhost')

