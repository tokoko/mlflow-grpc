from mlflow.models.cli import _get_flavor_backend


# serve('model')

model_uri = 'model'
no_conda = True
install_mlflow = False
workers = 1
host='localhost'
port='5000'



_get_flavor_backend(
        model_uri, no_conda=no_conda, workers=workers, install_mlflow=install_mlflow
    ).serve(model_uri=model_uri, port=port, host=host)


#mlflow models serve -m runs:/my-run-id/model-path &