import os
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import the config package
repo_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(repo_root))

from config import load_config, LlamaFarmConfig, save_config, example
from core.config import settings

class ProjectService:
  """
  Service for managing projects.
  """

  @classmethod
  def get_project_dir(cls, namespace: str, project_id: str):
    if settings.lf_project_dir is None:
      return os.path.join(settings.lf_data_dir, "projects", namespace, project_id)
    else:
      return settings.lf_project_dir

  @classmethod
  def create_project(cls, namespace: str, project_id: str) -> LlamaFarmConfig:
    """
    Create a new project.
    @param project_id: The ID of the project to create. (e.g. MyNamespace/MyProject)
    """
    project_dir = cls.get_project_dir(namespace, project_id)
    os.makedirs(project_dir, exist_ok=True)
    cfg = example.create_sample_config()
    cls.save_config(namespace, project_id, cfg)
    return cfg

  @classmethod
  def load_config(cls, namespace: str, project_id: str) -> LlamaFarmConfig:
    return load_config(cls.get_project_dir(namespace, project_id))

  @classmethod
  def save_config(cls, namespace: str, project_id: str, config: LlamaFarmConfig) -> LlamaFarmConfig:
    print(f"Saving config to {cls.get_project_dir(namespace, project_id)}")
    print(f"Config: {config}")
    return save_config(config, cls.get_project_dir(namespace, project_id))