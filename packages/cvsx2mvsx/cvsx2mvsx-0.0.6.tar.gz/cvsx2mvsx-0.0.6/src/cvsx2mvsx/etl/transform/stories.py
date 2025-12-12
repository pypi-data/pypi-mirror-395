import os
from uuid import uuid4

from cvsx2mvsx.models.mvsx.states import MVSXEntry
from cvsx2mvsx.models.stories.model import (
    SceneAsset,
    SceneData,
    Story,
    StoryContainer,
    StoryMetadata,
)


class StoriesTransformer:
    def __init__(self, mvsx_entry: MVSXEntry) -> None:
        self._mvsx_entry = mvsx_entry

    def run(self) -> StoryContainer:
        assets = self._collect_all_assets()

        scenes: list[SceneData] = []
        for i, snapshot in enumerate(self._mvsx_entry.states.snapshots):
            snapshot_id = i + 1
            scene = SceneData(
                id=str(uuid4()),
                header=snapshot.metadata.title or f"Scene {snapshot_id}",
                key=f"scene-{snapshot_id}",
                description=snapshot.metadata.description or "",
                javascript="",
            )
            scenes.append(scene)

        if not scenes:
            raise ValueError("No snapshots found in source MVSX.")

        metadata = StoryMetadata(
            title=self._mvsx_entry.states.metadata.title or "Converted MVSX",
        )
        story = Story(
            metadata=metadata,
            javascript="",
            scenes=scenes,
            assets=assets,
        )

        return StoryContainer(story=story)

    def _collect_all_assets(self) -> list[SceneAsset]:
        assets: list[SceneAsset] = []
        asset_dir = self._mvsx_entry.asset_dir

        for root, _, files in os.walk(asset_dir):
            for file in files:
                if file == "index.mvsj":
                    continue

                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, asset_dir)

                with open(full_path, "rb") as f:
                    content = f.read()
                assets.append(SceneAsset(name=rel_path, content=content))

        return assets
