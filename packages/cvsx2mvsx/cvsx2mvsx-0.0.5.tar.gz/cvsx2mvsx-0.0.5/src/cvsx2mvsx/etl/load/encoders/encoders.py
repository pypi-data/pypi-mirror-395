import numpy as np
from ciftools.binary import encoder
from ciftools.binary.data_types import DataType, DataTypeEnum
from ciftools.binary.encoder import BinaryCIFEncoder, ComposeEncoders


def bytearray_encoder() -> BinaryCIFEncoder:
    return encoder.BYTE_ARRAY


def delta_encoder() -> BinaryCIFEncoder:
    return ComposeEncoders(
        encoder.DELTA,
        encoder.BYTE_ARRAY,
    )


def delta_rl_encoder() -> BinaryCIFEncoder:
    return ComposeEncoders(
        encoder.DELTA,
        encoder.RUN_LENGTH,
        encoder.BYTE_ARRAY,
    )


def delta_intpack_encoder() -> BinaryCIFEncoder:
    return ComposeEncoders(
        encoder.DELTA,
        encoder.INTEGER_PACKING,
    )


def coord_encoder(coords: np.ndarray) -> BinaryCIFEncoder:
    """Encoder for coordinate data in meshes. Applies encodings: interval-quantization, delta, byte-array"""
    # num_steps, array_type = 2**32-1, DataTypeEnum.Uint32
    num_steps, array_type = (
        2**16 - 1,
        DataTypeEnum.Uint16,
    )  # ~0.01 voxel error - should be OK
    # num_steps, array_type = 2**8-1, DataTypeEnum.Uint8  # Too low quality

    return ComposeEncoders(
        encoder.IntervalQuantization(
            coords.min(),
            coords.max(),
            num_steps,
            array_type,
        ),
        encoder.DELTA,
        # encoder.INTEGER_PACKING,  # TODO: test this one out
        encoder.BYTE_ARRAY,
    )


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
