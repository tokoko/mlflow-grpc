import pytest
from mlflowgrpc import schema_to_proto
from mlflow.types import Schema, TensorSpec, ColSpec, DataType
from mlflow.exceptions import MlflowException
import numpy as np


def test_exception_if_tensorspec_schema():
    ts = TensorSpec(type=np.dtype("int32"), shape=(1,1), name="dummy")
    schema = Schema(inputs=[ts])
    
    with pytest.raises(MlflowException) as ex:
        schema_to_proto(schema, "TensorMessage")

    assert "TensorSpec schema conversion" in str(ex)

def test_colspec_conversion():
    cols = [
        ColSpec(type=DataType.boolean, name="booleanCol"),
        ColSpec(type=DataType.integer, name="integerCol"),
        ColSpec(type=DataType.long, name="longCol"),
        ColSpec(type=DataType.float, name="floatCol"),
        ColSpec(type=DataType.double, name="doubleCol"),
        ColSpec(type=DataType.string, name="stringCol"),
        ColSpec(type=DataType.binary, name="binaryCol")
    ]
    schema = Schema(inputs=cols)

    expected = """message ModelInput {
    bool booleanCol = 1;
    int32 integerCol = 2;
    int64 longCol = 3;
    float floatCol = 4;
    double doubleCol = 5;
    string stringCol = 6;
    bytes binaryCol = 7;
}"""

    assert(schema_to_proto(schema, 'ModelInput') == expected)


def test_anon_colspec_conversion():
    cols = [
        ColSpec(type=DataType.boolean),
        ColSpec(type=DataType.integer),
        ColSpec(type=DataType.integer)
    ]
    schema = Schema(inputs=cols)

    expected = """message ModelInput {
    bool col1 = 1;
    int32 col2 = 2;
    int32 col3 = 3;
}"""

    assert(schema_to_proto(schema, 'ModelInput') == expected)


