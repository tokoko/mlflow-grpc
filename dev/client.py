from sklearn import datasets
import requests
import numpy as np

diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True, as_frame=True)

data = {
    "columns": list(diabetes_X.columns), 
    "data": diabetes_X.head().values.tolist()
}

res = requests.post('http://127.0.0.1:5000/invocations', json=data)

print(res.text)

# curl http://127.0.0.1:5000/invocations -H 'Content-Type: application/json' -d '{
#             "columns": ["a", "b", "c"],
#             "data": [[1, 2, 3], [4, 5, 6]]
#         }'