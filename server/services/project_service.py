import os
from config import load_config, LlamaFarmConfig, save_config
from core.config import settings

class ProjectService:
  """
  Service for managing projects.
  """

  @classmethod
  def get_project_dir(cls, project_id: str):
    if settings.lf_project_dir is None:
      return os.path.join(settings.lf_data_dir, "projects", project_id)
    else:
      return settings.lf_project_dir

  @classmethod
  def load_config(cls, project_id: str) -> LlamaFarmConfig:
    return load_config(cls.get_project_dir(project_id))

  @classmethod
  def save_config(cls, project_id: str, config: dict) -> LlamaFarmConfig:
    return save_config(self.get_project_dir(project_id), config)
    