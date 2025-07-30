import os
from config import loader, LlamaFarmConfig
from core.config import settings

class ProjectService:
  _config_loader: loader.ConfigLoader

  """
  Service for managing projects.
  """
  def __init__(self, config: loader.ConfigLoader = loader):
    self._config_loader = loader

  def _get_project_dir(self, project_id: str):
    if settings.lf_project_dir is None:
      return os.path.join(settings.lf_data_dir, "projects", project_id)
    else:
      return settings.lf_project_dir

  def load_config(self, project_id: str) -> LlamaFarmConfig:
    return self._config_loader.load_config(self._get_project_dir(project_id))

  def update_config(self, project_id: str, config: dict) -> LlamaFarmConfig:
    return self._config_loader.save_config(self._get_project_dir(project_id), config)
    