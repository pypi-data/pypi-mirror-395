import os
import zlib

import msgpack

from cvsx2mvsx.models.stories.model import StoryContainer


class StoriesLoader:
    def __init__(self, story_container: StoryContainer, out_file_path: str) -> None:
        self._story_container = story_container
        self._out_file_path = out_file_path

    def run(self) -> None:
        dirpath = os.path.dirname(self._out_file_path)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)

        story_data_dict = self._story_container.model_dump(exclude_none=True)
        data_bytes = msgpack.packb(story_data_dict, use_bin_type=True)
        compressed = zlib.compress(data_bytes)

        with open(self._out_file_path, "wb") as f:
            f.write(compressed)
