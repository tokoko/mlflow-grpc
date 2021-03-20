from mlflow.pyfunc import load_model
from mlflow_grpc.server import serve
from mlflow_grpc.backend import PyFuncGrpcBackend

backend = PyFuncGrpcBackend(
    config=None,
    workers=1,
    no_conda=False,
    install_mlflow=False
)

backend.serve('model', port='1', host='localhost')

# model = load_model('model')
# serve(model)
