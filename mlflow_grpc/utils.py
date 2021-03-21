from mlflow.types.schema import Schema
from mlflow.models.signature import ModelSignature
from mlflow.exceptions import MlflowException
from mlflow.pyfunc import PyFuncModel
from google.protobuf.json_format import MessageToDict, ParseDict
import pandas as pd
import subprocess
import sys


def schema_to_proto(schema: Schema, message_name: str):
    if schema.is_tensor_spec():
        raise MlflowException('TensorSpec schema conversion to proto message is not allowed')

    schema_to_proto_type = {
        'boolean': 'bool',
        'integer': 'int32',
        'long': 'int64',
        'float': 'float',
        'double': 'double',
        'string': 'string',
        'binary': 'bytes'
    }

    cols = [
            {
                'index': i[0] + 1,
                'type': i[1]['type'], 
                'name': i[1]['name'] if 'name' in i[1] else f'col{i[0] + 1}' 
            } for i in enumerate(schema.to_dict())
        ]

    res = [f'    {schema_to_proto_type[c["type"]]} {c["name"]} = {c["index"]};' for c in cols]
    
    res = "\n".join(res)
    return f'''message {message_name} {{
{res}
}}'''

# def model_to_proto(model: PyFuncModel) -> str:
#     signature: ModelSignature = model.metadata.signature

#     if not signature:
#         raise MlflowException("Can't serve grpc endpoint without model signature")

#     return model_signature_to_proto(signature)

def prepare_env(signature: ModelSignature, dirpath):
    import os
    with open(file=os.path.join(dirpath, 'model.proto'), mode='w') as f:
        f.write(model_signature_to_proto(signature))

    command = 'python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. ./model.proto'

    if os.name != "nt":
        child = subprocess.Popen(["bash", "-c", command], close_fds=True, cwd=dirpath)
    else:
        child = subprocess.Popen(["cmd", "/c", command], close_fds=True, cwd=dirpath)
    child.wait()

    sys.path.append(dirpath)


def model_signature_to_proto(signature: ModelSignature) -> str:
    return f'''syntax = "proto3";

service MLService {{
    rpc invocations (ModelInput) returns (ModelOutput) {{}}
}}

message ModelInput {{
    repeated ModelInputItem rows = 1;
}}

message ModelOutput {{
    repeated ModelOutputItem rows = 1;
}}

{schema_to_proto(signature.inputs, "ModelInputItem")}

{schema_to_proto(signature.outputs, "ModelOutputItem")}'''


def proto_message_to_df(message):
    return pd.DataFrame(
        [MessageToDict(i) for i in message.rows]
    )


def df_to_proto_input(df):
    from model_pb2 import ModelInput, ModelInputItem

    return ModelInput(
        rows=[ParseDict(row, ModelInputItem()) for row in df.to_dict('records')]
    )

def df_to_proto_output(df):
    from model_pb2 import ModelOutput, ModelOutputItem
    import pandas as pd

    return ModelOutput(
        rows=[ParseDict(row, ModelOutputItem()) for row in pd.DataFrame({'col1' : df}).to_dict('records')]
    )
