from __future__ import print_function
import logging
import grpc
from model_pb2_grpc import MLServiceStub
from model_pb2 import ModelInput

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = MLServiceStub(channel)

        input = ModelInput(
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
        )

        response = stub.invocations(input)
    print("Greeter client received: " + str(response.col1))


if __name__ == '__main__':
    logging.basicConfig()
    run()