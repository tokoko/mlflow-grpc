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
import argparse


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
        

def serve(model: PyFuncModel, max_workers=2, port='50051', host='localhost'):
    with tempfile.TemporaryDirectory() as dirpath:
        print(dirpath)
        prepare_env(model, dirpath)

        from model_pb2_grpc import add_MLServiceServicer_to_server
        from mlflow_grpc.grpc_server import MLServer

        server = grpc.server(futures.ThreadPoolExecutor(max_workers))
        add_MLServiceServicer_to_server(MLServer(model), server)
        server.add_insecure_port('[::]:' + port)
        server.start()
        print('Server Started')
        server.wait_for_termination()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='grpc server arguments')
    parser.add_argument('--model-uri', type=str, required=True)
    parser.add_argument('--workers', type=int)
    parser.add_argument('--port', type=str)
    parser.add_argument('--host', type=str)
    args = parser.parse_args()

    logging.basicConfig()    
    model = load_model(args.model_uri)
    serve(model, max_workers=args.workers, port=args.port, host=args.host)