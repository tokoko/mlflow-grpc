from model_pb2_grpc import MLServiceServicer, add_MLServiceServicer_to_server
from model_pb2 import ModelOutput, ModelOutputItem
from .utils import proto_message_to_df, df_to_proto_output

class MLServer(MLServiceServicer):
    def __init__(self, model):
        self.model = model

    def invocations(self, request, context):
        input_df = proto_message_to_df(request)
        out_df = self.model.predict(input_df)
        return df_to_proto_output(out_df)