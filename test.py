from mlflow.pyfunc import load_model
from mlflowgrpc.grpc import prepare_env

model = load_model('model')
prepare_env(model)

from mlflowgrpc.server import serve

serve(model)
