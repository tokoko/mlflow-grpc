from sklearn import datasets
import requests
import numpy as np

diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True)

diabetes_X = diabetes_X[:, np.newaxis, 2]

# print(diabetes_X.schema)
# print(diabetes_X)

data = {
    "data": diabetes_X.tolist()[0]
}

# print(diabetes_X.tolist())

res = requests.post('http://127.0.0.1:5000/invocations', json=data)

print(res.text)

# curl http://127.0.0.1:5000/invocations -H 'Content-Type: application/json' -d '{
#             "columns": ["a", "b", "c"],
#             "data": [[1, 2, 3], [4, 5, 6]]
#         }'