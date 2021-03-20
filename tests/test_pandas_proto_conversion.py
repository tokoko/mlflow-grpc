from mlflow_grpc.utils import proto_message_to_df, df_to_proto_message

from model_pb2 import ModelInput, ModelInputItem, ModelOutput, ModelOutputItem


def test_proto_message_to_df():
    message = ModelInput(rows=
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

    message = proto_message_to_df(message)

    
