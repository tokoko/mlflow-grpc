from __future__ import print_function
import logging
import grpc
import tempfile
from mlflow.pyfunc import load_model
from mlflow_grpc.server import prepare_env

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    from model_pb2_grpc import MLServiceStub
    from model_pb2 import ModelInput, ModelInputItem

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = MLServiceStub(channel)

        input = ModelInput(rows=
            [
            ModelInputItem(
            age = 1,
            sex = 2,
            bmi = 3,
            bp = 4,
            s1 = 411,
            s2 = 6,
            s3 = 7,
            s4 = 8,
            s5 = 9,
            s6 = 10
        )])

        # from mlflow_grpc.utils import proto_message_to_df

        # print(proto_message_to_df(input))


        response = stub.invocations(input)
    print("Greeter client received: " + str(response))


if __name__ == '__main__':
    with tempfile.TemporaryDirectory() as dirpath:
        logging.basicConfig()
        model = load_model('model')

        prepare_env(model, dirpath)

        run()