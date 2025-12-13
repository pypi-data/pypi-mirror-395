import numpy as np
from ciftools.binary import encoder
from ciftools.binary.data_types import DataType, DataTypeEnum
from ciftools.binary.encoder import BinaryCIFEncoder, ComposeEncoders


def decide_encoder(data: np.ndarray) -> tuple[BinaryCIFEncoder, np.dtype]:
    data_type = DataType.from_dtype(data.dtype)
    typed_array = DataType.to_dtype(data_type)

    encoders: list[BinaryCIFEncoder] = []

    if data_type in [DataTypeEnum.Float32, DataTypeEnum.Float64]:
        interval_quantization = encoder.IntervalQuantization(
            data.min(initial=data[0]),
            data.max(initial=data[0]),
            255,
            DataTypeEnum.Uint8,
        )
        encoders.append(interval_quantization)
    else:
        encoders.append(encoder.RUN_LENGTH)

    encoders.append(encoder.BYTE_ARRAY)
    composed_encoders = ComposeEncoders(*encoders)

    return composed_encoders, typed_array
