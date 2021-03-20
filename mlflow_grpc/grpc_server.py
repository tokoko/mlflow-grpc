from model_pb2_grpc import MLServiceServicer, add_MLServiceServicer_to_server
from model_pb2 import ModelOutput, ModelOutputItem
from .utils import proto_message_to_df

class MLServer(MLServiceServicer):
    def __init__(self, model):
        self.model = model

    def invocations(self, request, context):
        df = proto_message_to_df(request)

        return ModelOutput(
            rows = [
                ModelOutputItem(col1=self.model.predict(df).item(0))
            ]
        )