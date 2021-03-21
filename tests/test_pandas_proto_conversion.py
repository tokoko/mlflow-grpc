from mlflow_grpc.utils import proto_message_to_df, prepare_env, df_to_proto_input, df_to_proto_output
from mlflow.models import infer_signature
from sklearn import datasets
from pandas.util.testing import assert_frame_equal
import tempfile


def df_to_proto_input_and_back(df):
    proto = df_to_proto_input(df)
    return proto_message_to_df(proto)

def df_to_proto_output_and_back(df):
    proto = df_to_proto_output(df)
    return proto_message_to_df(proto)


def test_diabetes_conversion():
    diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True, as_frame=True)
    signature = infer_signature(diabetes_X, diabetes_y)

    with tempfile.TemporaryDirectory() as dirpath:
        prepare_env(signature, dirpath)

        assert_frame_equal(
            df_to_proto_input_and_back(diabetes_X).reset_index(drop=True), 
            diabetes_X.reset_index(drop=True)
        )
