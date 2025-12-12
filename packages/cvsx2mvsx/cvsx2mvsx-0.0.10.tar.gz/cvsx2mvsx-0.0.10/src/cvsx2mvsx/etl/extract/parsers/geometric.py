from cvsx2mvsx.etl.extract.parsers.interface import Parser
from cvsx2mvsx.models.cvsx.geometric import ShapePrimitiveData


class GeometricParser(Parser[ShapePrimitiveData]):
    def parse(self, data: bytes) -> ShapePrimitiveData:
        try:
            json_string = data.decode("utf-8")
            return ShapePrimitiveData.model_validate_json(json_string)
        except Exception as e:
            raise ValueError(f"Geometric parsing error: {e}")
