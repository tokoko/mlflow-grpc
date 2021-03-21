import logging
import os
import subprocess
import posixpath
from mlflow.models import FlavorBackend
from mlflow.models.docker_utils import _build_image, DISABLE_ENV_CREATION
from mlflow.pyfunc import ENV, scoring_server

from mlflow.utils.conda import get_or_create_conda_env, get_conda_bin_executable, get_conda_command
from mlflow.tracking.artifact_utils import _download_artifact_from_uri
from mlflow.utils.file_utils import path_to_local_file_uri
from mlflow.pyfunc.backend import PyFuncBackend, _execute_in_conda_env


_logger = logging.getLogger(__name__)


from mlflow_grpc.server import serve
from mlflow.pyfunc import load_model

class PyFuncGrpcBackend(PyFuncBackend):
    """
        Flavor backend implementation for the generic python models.
    """

    def __init__(self, config, workers=1, no_conda=False, install_mlflow=False, **kwargs):
        super().__init__(config=config, **kwargs)
        self._nworkers = workers or 1
        self._no_conda = no_conda
        self._install_mlflow = install_mlflow


    def serve(self, model_uri, port='8000', host='localhost'):
        """
        Serve pyfunc model locally.
        """
        local_path = _download_artifact_from_uri(model_uri)
        local_uri = path_to_local_file_uri(local_path)
  
        command = (
                f"python -m mlflow_grpc.server --model-uri {local_uri} --port {port} --host {host} --workers {self._nworkers}"
            )
        
        command_env = os.environ.copy()

        if not self._no_conda and ENV in self._config:
            print('Starting in conda')
            conda_env_path = os.path.join(local_path, self._config[ENV])
            return _execute_in_conda_env(
                conda_env_path, command, self._install_mlflow, command_env=command_env
            )
        else:
            _logger.info("=== Running command '%s'", command)
        
        if os.name != "nt":
            subprocess.Popen(["bash", "-c", command], env=command_env).wait()
        else:
            subprocess.Popen([command.split(" ")], env=command_env).wait()
