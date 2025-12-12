from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict

# Re-using Vec3 logic or defining explicitly
Vec3 = tuple[float, float, float]


class CameraData(BaseModel):
    mode: Literal["perspective", "orthographic"]
    target: Vec3
    position: Vec3
    up: Vec3
    fov: float


class SceneAsset(BaseModel):
    name: str
    content: Optional[bytes] = None
    file_path: Optional[str] = None


class SceneData(BaseModel):
    id: str
    header: str
    key: str
    description: str
    javascript: str
    camera: Optional[CameraData] = None
    linger_duration_ms: Optional[float] = None
    transition_duration_ms: Optional[float] = None


class StoryMetadata(BaseModel):
    title: str
    author_note: Optional[str] = None
    tags: list[str] = []


class Story(BaseModel):
    metadata: StoryMetadata
    javascript: str
    scenes: list[SceneData]
    assets: list[SceneAsset]


class StoryContainer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    version: int = 1
    story: Story
