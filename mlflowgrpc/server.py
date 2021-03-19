from mlflow.pyfunc import PyFuncModel, load_model
from .utils import model_to_proto, proto_message_to_df
import os
import subprocess
import grpc
from concurrent import futures


def prepare_env(model):
    with open(file='model.proto', mode='w') as f:
        f.write(model_to_proto(model))

    command = 'python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. ./model.proto'

    if os.name != "nt":
        child = subprocess.Popen(["bash", "-c", command], close_fds=True)
    else:
        child = subprocess.Popen(["cmd", "/c", command], close_fds=True)
    child.wait()

def serve(model: PyFuncModel, max_workers=2, port='50051'):
    prepare_env(model)

    from model_pb2_grpc import add_MLServiceServicer_to_server
    from .grpc import MLServer

    server = grpc.server(futures.ThreadPoolExecutor(max_workers))
    add_MLServiceServicer_to_server(MLServer(model), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print('Server Started')
    server.wait_for_termination()
