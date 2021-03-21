from __future__ import print_function
import logging
import grpc
import tempfile
from mlflow.pyfunc import load_model
from mlflow_grpc.server import prepare_env
from mlflow_grpc.utils import df_to_proto_input, proto_message_to_df
from sklearn import datasets

def run():
    diabetes_X, _ = datasets.load_diabetes(return_X_y=True, as_frame=True)

    from model_pb2_grpc import MLServiceStub
    from model_pb2 import ModelInput, ModelInputItem

    with grpc.insecure_channel('localhost:9000') as channel:
        stub = MLServiceStub(channel)

        response = stub.invocations(df_to_proto_input(diabetes_X))

        print(proto_message_to_df(response))


if __name__ == '__main__':
    with tempfile.TemporaryDirectory() as dirpath:
        model = load_model('model')
        signature = model.metadata.signature

        prepare_env(signature, dirpath)

        run()


 # input = ModelInput(rows=
        #     [
        #     ModelInputItem(
        #     age = 1,
        #     sex = 2,
        #     bmi = 3,
        #     bp = 4,
        #     s1 = 411,
        #     s2 = 6,
        #     s3 = 7,
        #     s4 = 8,
        #     s5 = 9,
        #     s6 = 10
        # )])