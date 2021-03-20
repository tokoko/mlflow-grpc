from mlflow.pyfunc import PyFuncModel, load_model
from mlflow_grpc.utils import model_to_proto, proto_message_to_df
from concurrent import futures
import os
import sys
import subprocess
import grpc
import tempfile
import logging
import os

def prepare_env(model, dirpath):    
    with open(file=os.path.join(dirpath, 'model.proto'), mode='w') as f:
        f.write(model_to_proto(model))

    command = 'python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. ./model.proto'

    if os.name != "nt":
        child = subprocess.Popen(["bash", "-c", command], close_fds=True, cwd=dirpath)
    else:
        child = subprocess.Popen(["cmd", "/c", command], close_fds=True, cwd=dirpath)
    child.wait()

    sys.path.append(dirpath)
        

def serve(model: PyFuncModel, max_workers=2, port='50051'):
    with tempfile.TemporaryDirectory() as dirpath:
        print(dirpath)
        prepare_env(model, dirpath)

        from model_pb2_grpc import add_MLServiceServicer_to_server
        from mlflow_grpc.grpc import MLServer

        server = grpc.server(futures.ThreadPoolExecutor(max_workers))
        add_MLServiceServicer_to_server(MLServer(model), server)
        server.add_insecure_port('[::]:' + port)
        server.start()
        print('Server Started')
        server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()    
    local_uri = 'file:///workspace/mlflow-grpc/model'
    model = load_model(local_uri)
    serve(model)