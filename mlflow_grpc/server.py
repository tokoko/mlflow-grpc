import os
import sys
import subprocess
import grpc
import tempfile
import logging
import os
import argparse
from concurrent import futures
from mlflow.pyfunc import PyFuncModel, load_model
from mlflow.exceptions import MlflowException
from mlflow.models.signature import ModelSignature
from mlflow_grpc.utils import prepare_env


def serve(model: PyFuncModel, max_workers=2, port='50051', host='localhost'):
    signature: ModelSignature = model.metadata.signature

    if not signature:
        raise MlflowException("Can't serve grpc endpoint without model signature")
    
    with tempfile.TemporaryDirectory() as dirpath:
        prepare_env(signature, dirpath)

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