from mlflow.pyfunc import load_model
from mlflow_grpc.server import serve




def test_grpc_serve():
    model = load_model('/workspace/mlflow-grpc/model')
    res = serve(model)

    assert res == 'Success'