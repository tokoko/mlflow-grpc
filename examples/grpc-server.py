# from diabetes_pb2 import ModelInput, ModelOutput
# from diabetes_pb2_grpc import MLServiceServicer, add_MLServiceServicer_to_server
# from concurrent import futures
# from utils import proto_message_to_df
# import logging
# import grpc
# from mlflow.pyfunc import load_model

# pymodel = load_model('model')

# class MLServer(MLServiceServicer):

#     def invocations(self, request, context):
#         df = proto_message_to_df(request)
#         return ModelOutput(res=pymodel.predict(df).item(0))


# def serve():
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
#     add_MLServiceServicer_to_server(MLServer(), server)
#     server.add_insecure_port('[::]:50051')
#     server.start()
#     print('Server Started')
#     server.wait_for_termination()

import logging

if __name__ == '__main__':
    logging.basicConfig()
    # serve()
    import subprocess
    subprocess.Popen(["python", "-m", "mlflow_grpc.server"], cwd='/workspace/mlflow-grpc').wait()