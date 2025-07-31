from fastapi import APIRouter
from pydantic import BaseModel
from server.services.project_service import ProjectService

router = APIRouter(
  prefix="/projects/{namespace}/{project}/datasets",
  tags=["datasets"],
)

class Dataset(BaseModel):
    id: int
    name: str
    description: str
    namespace: str
    project: str

class ListDatasetsResponse(BaseModel):
    total: int
    datasets: list[Dataset]

@router.get("/", response_model=ListDatasetsResponse)
async def list_datasets(namespace: str, project: str):
    project_config = ProjectService.load_config(f"{namespace}/{project}")
    datasets = project_config.get("models", {})

    project = Project(
        id=project_id,
        name="test",
        description="test",
        namespace=namespace,
    )
    return DeleteProjectResponse(
      project=project,
    )