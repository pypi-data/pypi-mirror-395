from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from cvsx2mvsx.etl.extract.cvsx import CVSXExtractor
from cvsx2mvsx.etl.extract.internal import InternalExtractor
from cvsx2mvsx.etl.load.internal import InternalLoader
from cvsx2mvsx.etl.load.mvsx import MVSXLoader
from cvsx2mvsx.etl.load.stories import StoriesLoader
from cvsx2mvsx.etl.pipelines.context import PipelineContext
from cvsx2mvsx.etl.transform.internal import InternalTransformer
from cvsx2mvsx.etl.transform.mvsx import MVSXTransformer
from cvsx2mvsx.etl.transform.stories import StoriesTransformer
from cvsx2mvsx.models.cvsx.entry import CVSXEntry
from cvsx2mvsx.models.internal.entry import InternalEntry
from cvsx2mvsx.models.mvsx.states import MVSXEntry
from cvsx2mvsx.models.stories.model import StoryContainer

In = TypeVar("In")
Out = TypeVar("Out")


class PipelineStep(ABC, Generic[In, Out]):
    @abstractmethod
    def execute(self, data: In, context: PipelineContext) -> Out:
        pass


class ExtractCVSX(PipelineStep[str, CVSXEntry]):
    def execute(
        self,
        zip_path: str,
        context: PipelineContext,
    ) -> CVSXEntry:
        extract_dir = context.get_path("extracted_cvsx")
        return CVSXExtractor(
            zip_path=zip_path,
            out_dir_path=extract_dir,
        ).run()


class ExtractInternal(PipelineStep[str, InternalEntry]):
    def execute(
        self,
        internal_dir_path: str,
        context: PipelineContext,
    ) -> InternalEntry:
        return InternalExtractor(
            internal_dir_path=internal_dir_path,
        ).run()


class TransformToInternal(PipelineStep[CVSXEntry, InternalEntry]):
    def execute(
        self,
        entry: CVSXEntry,
        context: PipelineContext,
    ) -> InternalEntry:
        internal_dir = context.get_path("internal_model")
        return InternalTransformer(
            cvsx_entry=entry,
            out_dir_path=internal_dir,
            lattice_to_mesh=context.config.lattice_to_mesh,
        ).run()


class TransformToMVSX(PipelineStep[InternalEntry, MVSXEntry]):
    def execute(
        self,
        entry: InternalEntry,
        context: PipelineContext,
    ) -> MVSXEntry:
        out_dir = context.get_path("mvsx_assets")
        return MVSXTransformer(
            internal_entry=entry,
            out_dir_path=out_dir,
        ).run()


class TransformToStories(PipelineStep[InternalEntry, StoryContainer]):
    def execute(
        self,
        entry: InternalEntry,
        context: PipelineContext,
    ) -> StoryContainer:
        return StoriesTransformer(
            internal_entry=entry,
        ).run()


class LoadMVSX(PipelineStep[MVSXEntry, None]):
    def execute(
        self,
        entry: MVSXEntry,
        context: PipelineContext,
    ) -> None:
        MVSXLoader(
            mvsx_entry=entry,
            out_file_path=context.config.output_path,
            compression_level=context.config.compression_level,
        ).run()


class LoadStories(PipelineStep[StoryContainer, None]):
    def execute(
        self,
        container: StoryContainer,
        context: PipelineContext,
    ) -> None:
        StoriesLoader(
            story_container=container,
            out_file_path=context.config.output_path,
            compression_level=context.config.compression_level,
        ).run()


class LoadInternal(PipelineStep[InternalEntry, None]):
    def execute(
        self,
        entry: InternalEntry,
        context: PipelineContext,
    ) -> None:
        InternalLoader(
            internal_entry=entry,
            out_dir_path=context.config.output_path,
        ).run()
