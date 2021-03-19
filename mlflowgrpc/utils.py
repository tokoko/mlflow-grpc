from mlflow.types.schema import Schema
from mlflow.models.signature import ModelSignature
from mlflow.exceptions import MlflowException
from mlflow.pyfunc import PyFuncModel
from google.protobuf.json_format import MessageToDict
import pandas as pd
from pprint import pprint


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

def model_to_proto(model: PyFuncModel):
    signature: ModelSignature = model.metadata.signature

    if not signature:
        raise MlflowException("Can't serve grpc endpoint without model signature")

    return f'''syntax = "proto3";

service MLService {{
    rpc invocations (ModelInput) returns (ModelOutput) {{}}
}}

{schema_to_proto(signature.inputs, "ModelInput")}

{schema_to_proto(signature.outputs, "ModelOutput")}'''


def proto_message_to_df(message):
    d = MessageToDict(message)
    return pd.DataFrame([d])