if __package__ or "." in __name__:
    from . import vc6il
else:
    import vc6il

if "cuda" in __package__ or "cuda" in __name__:
    import cupy as cupy_module
else:
    cupy_module = None

from enum import Enum
from typing import Iterable
import ctypes
import platform

class CodecType(Enum):
    ENCODER = vc6il.VC6_IL_CODEC_TYPE_ENCODER
    DECODER = vc6il.VC6_IL_CODEC_TYPE_DECODER


class CodecBackendType(Enum):
    CPU = vc6il.VC6_IL_CODEC_BACKEND_CPU
    GPU = vc6il.VC6_IL_CODEC_BACKEND_GPU

class ImageMemoryType(Enum):
    CPU = vc6il.VC6_IL_MEMORY_POOL_TYPE_CPU
    CUDA_DEVICE = vc6il.VC6_IL_MEMORY_POOL_TYPE_CUDA_DEVICE

class EncoderGenericPreset(Enum):
    # High speed and reasonable quality
    PROXY = vc6il.VC6_IL_ENCODER_GENERIC_PRESET_PROXY
    HT = vc6il.VC6_IL_ENCODER_GENERIC_PRESET_HT  # High speed and good quality
    STD = vc6il.VC6_IL_ENCODER_GENERIC_PRESET_STD  # Good speed and better quality
    HQ = vc6il.VC6_IL_ENCODER_GENERIC_PRESET_HQ  # Good speed and high quality
    # Very high quality, visually lossless
    XQ = vc6il.VC6_IL_ENCODER_GENERIC_PRESET_XQ
    LOSSLESS = vc6il.VC6_IL_ENCODER_GENERIC_PRESET_LOSSLESS  # Lossless compression


class EncoderProfilePreset(Enum):
    LIGHT = vc6il.VC6_IL_ENCODER_PROFILE_PRESET_LIGHT
    GOOD = vc6il.VC6_IL_ENCODER_PROFILE_PRESET_GOOD
    BETTER = vc6il.VC6_IL_ENCODER_PROFILE_PRESET_BETTER
    ULTRA = vc6il.VC6_IL_ENCODER_PROFILE_PRESET_ULTRA


class EncoderQualityPreset(Enum):
    # Constant bitrate targeting a given BitsPerPixel
    CBR = vc6il.VC6_IL_ENCODER_QUALITY_PRESET_CBR
    # Performs multiple passes to achieve accurate constant bitrate
    CBR_MULTIPASS = vc6il.VC6_IL_ENCODER_QUALITY_PRESET_CBR_MULTIPASS
    # Variable Bitrate Lossless
    VBR_LOSSLESS = vc6il.VC6_IL_ENCODER_QUALITY_PRESET_VBR_LOSSLESS


# 10 bit formats are little-endian


class PictureFormat(Enum):
    RGB_8 = vc6il.VC6_IL_PICTURE_FORMAT_RGB8
    RGBA_8 = vc6il.VC6_IL_PICTURE_FORMAT_RGBA8
    RGB_10 = vc6il.VC6_IL_PICTURE_FORMAT_RGB10
    RGBA_10 = vc6il.VC6_IL_PICTURE_FORMAT_RGBA10
    YUV_8_444 = vc6il.VC6_IL_PICTURE_FORMAT_YUV8_444_P
    YUV_8_422 = vc6il.VC6_IL_PICTURE_FORMAT_YUV8_422_P
    YUV_8_420 = vc6il.VC6_IL_PICTURE_FORMAT_YUV8_420_P
    YUV_10_444 = vc6il.VC6_IL_PICTURE_FORMAT_YUV10_444_P
    YUV_10_422 = vc6il.VC6_IL_PICTURE_FORMAT_YUV10_422_P
    YUV_10_420 = vc6il.VC6_IL_PICTURE_FORMAT_YUV10_420_P


class LogDestination(Enum):
    SUPPRESS = vc6il.log_suppress
    STDOUT = vc6il.log_stdout
    STDERROR = vc6il.log_stderr


class FrameRegion:
    def __init__(self, echelon=0, origin_x=0, origin_y=0, width=0, height=0):
        self._region = vc6il.vc6_il_frame_region_t()
        self._region.echelon = echelon
        self._region.origin_x = origin_x
        self._region.origin_y = origin_y
        self._region.width = width
        self._region.height = height
        self._region.num_planes = 0

class FrameProbeResult:
    def __init__(self):
        self._probe_result = vc6il.vc6_il_frame_probe_result_t()
        self.width = 0
        self.height = 0
        self.num_planes = 0
        self.bitdepth = 0
        self.chroma_subsampling = 0
        self.frame_size = 0


def _raise_if_vc6_error(status, msg=None):
    if status != vc6il.VC6_IL_STATUS_CODE_SUCCESS:
        raise Exception("Failure in VC-6 API call" if msg is None else msg)


def _populate_encoder_input_io(input_buffer, input_io):
    cuda_interface = getattr(input_buffer, "__cuda_array_interface__", None)
    if not cuda_interface:
        status = vc6il.vc6_io_set_from_py_buffer(input_buffer, input_io)
        _raise_if_vc6_error(status)
        return

    version = cuda_interface.get("version", 0)
    if version < 2:
        raise Exception("CUDA array interface version 2 or higher is required")

    typestr = cuda_interface.get("typestr")
    itemsize = {
        '|u1': 1,  # unsigned 1-byte
        '|u2': 2,  # unsigned 2-byte
        '<u2': 2,  # unsigned 2-byte
    }.get(typestr)

    if itemsize is None:
        raise Exception(f"Unsupported dtype: {typestr} (expected '|u1' or '|u2')")

    shape = cuda_interface.get("shape")

    if cuda_interface.get("strides") is not None:
        raise Exception("Only C-contiguous CUDA arrays are supported")

    pointer = int(cuda_interface.get("data")[0])
    total_bytes = itemsize
    for dim in shape:
        total_bytes *= int(dim)

    input_io.clear()
    input_io.data = pointer
    input_io.offset = 0
    input_io.size = total_bytes


class ImageBuffer:
    def __init__(self, memory_type : ImageMemoryType,  io_object, io_owner=None):
        self._memory_type = memory_type
        self._vc6_codec = io_owner
        self._vc6_io_object = io_object

    def __del__(self):
        self.release()

    @property
    def memory_type(self) -> ImageMemoryType:
        return self._memory_type

    @property
    def memoryview(self) -> memoryview:
        if self._memory_type != ImageMemoryType.CPU:
            return None
        return self._vc6_io_object.get_memoryview()
        # TODO : should we set the object->base ?

    @property
    def __cuda_array_interface__(self):
        if self._memory_type != ImageMemoryType.CUDA_DEVICE:
            return None
        interface = {'shape': (self._vc6_io_object.size,), 'typestr': '|u1', 'descr': [('', '|u1')], 'stream': None, 'version': 3, 'strides': None, 'data': (int(self._vc6_io_object.data), False)}
        return interface

    def release(self):
        if self._vc6_codec is not None:
            status = vc6il.vc6_il_return_output_io(
                self._vc6_codec.codec, self._vc6_io_object
            )
            self._vc6_codec = None
            _raise_if_vc6_error(status, "failed to return a codec owned io object")


class AsyncImageBuffer:
    def __init__(self, memory_type : ImageMemoryType, io_owner, input_ref):
        self._memory_type = memory_type
        # this is to keep temporary input object alive
        self.input_ref = input_ref
        self._vc6_codec = io_owner
        self._vc6_io_object = None

    def __del__(self):
        self.release()

    def _wait_output(self):
        if self._vc6_io_object is None:
            status, self._vc6_io_object = vc6il.vc6_il_wait_output(self._vc6_codec.codec)
            _raise_if_vc6_error(status, "Async decode failed")

    @property
    def memory_type(self) -> ImageMemoryType:
        return self._memory_type

    @property
    def memoryview(self) -> memoryview:
        if self._memory_type != ImageMemoryType.CPU:
            return None
        self._wait_output()
        return self._vc6_io_object.get_memoryview()

    def get_memoryview(self) -> memoryview:
        return self.memoryview

    @property
    def __cuda_array_interface__(self):
        if self._memory_type != ImageMemoryType.CUDA_DEVICE:
            return None
        self._wait_output()
        interface = {'shape': (self._vc6_io_object.size,), 'typestr': '|u1', 'descr': [('', '|u1')], 'stream': None, 'version': 3, 'strides': None, 'data': (int(self._vc6_io_object.data), False)}
        return interface


    def release(self):
        self._wait_output()
        if self._vc6_codec is not None and self._vc6_io_object is not None:
            status = vc6il.vc6_il_return_output_io(
                self._vc6_codec.codec, self._vc6_io_object
            )
            self._vc6_codec = None
            _raise_if_vc6_error(status, "failed to return a codec owned io object")


def ProbeFrame(input_buffer: "bytes | bytearray | memoryview") -> FrameProbeResult :
    input_io = vc6il.vc6_il_io_t()
    vc6il.vc6_io_set_from_py_buffer(input_buffer, input_io)
    _probe_result = vc6il.vc6_il_frame_probe_result_t()
    status = vc6il.vc6_il_probe_frame(input_io, _probe_result)
    probe_result = FrameProbeResult()
    probe_result.width = _probe_result.width
    probe_result.height = _probe_result.height
    probe_result.num_planes = _probe_result.num_planes
    probe_result.bitdepth = _probe_result.bitdepth
    probe_result.chroma_subsampling = _probe_result.chroma_subsampling
    probe_result.frame_size = _probe_result.frame_size
    probe_result.num_echelons = _probe_result.num_echelons
    _raise_if_vc6_error(status, "failed to return a codec owned io object")
    return probe_result

def GetRequiredSizeForTargetEchelon(input_buffer: "bytes | bytearray | memoryview", target_echelon: int) -> int:
    input_io = vc6il.vc6_il_io_t()
    vc6il.vc6_io_set_from_py_buffer(input_buffer, input_io)
    status, size = vc6il.vc6_il_get_required_size_for_echelon(input_io, target_echelon)
    if status != vc6il.VC6_IL_STATUS_CODE_SUCCESS:
        size = 0
        print("Failed to query the size because insufficient data, return 0")
    return size

class Codec:
    def __init__(
        self,
        init_frame_width: int,
        init_frame_height: int,
        codec_type: CodecType,
        codec_backend_type: CodecBackendType,
        picture_format: PictureFormat,
        raw_image_memory_type: ImageMemoryType,
        async_mode: bool,
        peer_codec: "Codec",
        enable_logs: bool,
    ):
        if not isinstance(codec_type, CodecType):
            raise Exception(
                "codec_type parameter should be a member of CodecType enum"
            )
        if not isinstance(codec_backend_type, CodecBackendType):
            raise Exception(
                "codec_backend_type parameter should be a member of CodecBackendType enum"
            )
        if not isinstance(picture_format, PictureFormat):
            raise Exception(
                "picture_format parameter should be a member of PictureFormat enum"
            )
        if not isinstance(raw_image_memory_type, ImageMemoryType):
            raise Exception(
                "raw_image_memory_type parameter should be a member of ImageMemoryType enum"
            )

        self.codec_config = vc6il.vc6_il_codec_configuration_t()
        status = vc6il.vc6_il_default_codec_configuration_create(
            self.codec_config, codec_type.value
        )
        _raise_if_vc6_error(status, "Failed to create vc6 codec")
        self.codec_config.backend_type = codec_backend_type.value
        if codec_backend_type.value == vc6il.VC6_IL_CODEC_BACKEND_CPU:
            json_str = vc6il.vc6_il_json_str_t()
            arch = platform.machine()
            if arch.lower() in ["arm64", "aarch64"]:
                json_str.content = '{"simd_type" : "NEON" }'
            else:
                json_str.content = '{"simd_type" : "SSE3" }'
            json_str.length = len(json_str.content)
            self.codec_config.backend_json_str = json_str

        self.codec_config.num_backends = 1
        self.codec_config.async_mode = async_mode
        self.codec_config.compressed_io_pool_size = 3 if async_mode else 2
        self.codec_config.raw_io_pool_size = 3 if async_mode else 2
        self.codec_config.raw_io_memory_pool_type = raw_image_memory_type.value
        self.raw_memory_type = raw_image_memory_type

        # Configure raw io
        raw_io = vc6il.vc6_il_picture_description_t()
        raw_io.picture_format = picture_format.value
        self.picture_format = picture_format
        raw_io.width = init_frame_width
        raw_io.height = init_frame_height
        raw_io.row_alignment = 0
        self.codec_config.raw_io_picture_description = raw_io
        self.current_picture_description = raw_io
        self.codec_config.internal_video_bitdepth = 0
        self.codec_config.codec_type = codec_type.value
        self.codec_config.log_callback = (
            LogDestination.STDOUT.value
            if enable_logs
            else LogDestination.SUPPRESS.value
        )
        self.codec_config.error_callback = LogDestination.STDERROR.value
        if peer_codec is not None:
            status = vc6il.vc6_il_codec_configuration_set_peer_codec(
                self.codec_config, peer_codec.codec
            )
            _raise_if_vc6_error(status, "Failed to set peer codec")

        status, self.codec = vc6il.vc6_il_codec_create(self.codec_config)
        _raise_if_vc6_error(status, "Failed to create vc6 codec")

    def __del__(self):
        if self.codec is not None and vc6il:
            vc6il.vc6_il_codec_destroy(self.codec)

    def reconfigure(
        self, new_width: int, new_height: int, new_format: PictureFormat
    ):
        reconfig_params = vc6il.vc6_il_codec_reconfiguration_params_t()
        raw_io = vc6il.vc6_il_picture_description_t()
        raw_io.picture_format = new_format.value
        raw_io.width = new_width
        raw_io.height = new_height
        raw_io.row_alignment = 0
        reconfig_params.raw_io_picture_description = raw_io
        reconfig_params.internal_video_bitdepth = 0

        status = vc6il.vc6_il_codec_reconfigure(self.codec, reconfig_params)
        _raise_if_vc6_error(status, "Failed to reconfigure vc6 codec")
        self.current_picture_description = raw_io

    def set_configuration_json(self, json_str):
        c_json_str = vc6il.vc6_il_json_str_t()
        c_json_str.content = str(json_str)
        c_json_str.length = len(json_str)
        status = vc6il.vc6_il_set_codec_parameters_from_json(self.codec, c_json_str)
        _raise_if_vc6_error(status, "Failed to set configuration json for vc6 codec")


class EncoderSync(Codec):

    def __init__(
        self,
        init_frame_width: int,
        init_frame_height: int,
        codec_backend_type: CodecBackendType,
        picture_format: PictureFormat,
        raw_image_memory_type: ImageMemoryType = ImageMemoryType.CPU,
        peer_codec: "Codec" = None,
        enable_logs: bool = False,
    ):
        Codec.__init__(
            self,
            init_frame_width,
            init_frame_height,
            CodecType.ENCODER,
            codec_backend_type,
            picture_format,
            raw_image_memory_type,
            False,
            peer_codec,
            enable_logs,
        )

    def set_generic_preset(self, preset: EncoderGenericPreset) -> None:
        if not isinstance(preset, EncoderGenericPreset):
            raise Exception(
                "Parameter for set_generic_preset() should be a member of EncoderGenericPreset enum"
            )
        status = vc6il.vc6_il_set_encoder_generic_preset(self.codec, preset.value)
        _raise_if_vc6_error(status, "Failed to set encoder preset")

    def set_profile_from_preset(self, preset: EncoderProfilePreset) -> None:
        if not isinstance(preset, EncoderProfilePreset):
            raise Exception(
                "Parameter for set_profile_preset() should be a member of EncoderProfilePreset enum"
            )
        status = vc6il.vc6_il_set_encoder_profile_from_preset(self.codec, preset.value)
        _raise_if_vc6_error(status, "Failed to set encoder preset")

    def set_quality_from_preset(
        self, preset: EncoderQualityPreset, bpp: float = None
    ) -> None:
        if not isinstance(preset, EncoderQualityPreset):
            raise Exception(
                "Parameter preset for set_profile_preset() should be a member of EncoderQualityPreset enum"
            )
        if preset == EncoderQualityPreset.VBR_LOSSLESS and bpp is not None:
            bpp = 0
        float_bpp = float(bpp)
        status = vc6il.vc6_il_set_encoder_quality_from_preset(
            self.codec, preset.value, bpp
        )
        _raise_if_vc6_error(status, "Failed to set encoder preset")

    def read(self, input_path: str) -> ImageBuffer:
        # initializing the input and output pointers
        status, input_io = vc6il.vc6_il_get_input_io(self.codec)
        _raise_if_vc6_error(status)
        status, output_io = vc6il.vc6_il_get_output_io(self.codec)
        _raise_if_vc6_error(status)

        # read input file to input object
        with open(input_path, "rb") as f:
            read_size = f.readinto(input_io.get_memoryview())
            input_io.size = read_size

        # encoding the image to output_io pointer
        status = vc6il.vc6_il_encode(self.codec, input_io, output_io)
        _raise_if_vc6_error(status)
        return ImageBuffer(ImageMemoryType.CPU, output_io, self)

    def write(
        self, input_buffer: object, output_path: str
    ) -> None:
        # Initializing the input and output pointers
        input_io = vc6il.vc6_il_io_t()
        _populate_encoder_input_io(input_buffer, input_io)
        status, output_io = vc6il.vc6_il_get_output_io(self.codec)
        _raise_if_vc6_error(status)

        # encoding the image to output_io pointer
        status = vc6il.vc6_il_encode(self.codec, input_io, output_io)
        _raise_if_vc6_error(status)

        with open(output_path, "wb") as f:
            f.write(output_io.get_memoryview())

        # returning the output memory
        status = vc6il.vc6_il_return_output_io(self.codec, output_io)
        _raise_if_vc6_error(status)

    def encode(self, input_buffer: object) -> ImageBuffer:
        # initializing the input and output pointers
        input_io = vc6il.vc6_il_io_t()
        _populate_encoder_input_io(input_buffer, input_io)
        status, output_io = vc6il.vc6_il_get_output_io(self.codec)
        _raise_if_vc6_error(status)

        # encoding the image to output_io pointer
        status = vc6il.vc6_il_encode(self.codec, input_io, output_io)
        _raise_if_vc6_error(status)

        return ImageBuffer(ImageMemoryType.CPU, output_io, self)


class DecoderBase(Codec):

    def __init__(
        self,
        init_frame_width: int,
        init_frame_height: int,
        codec_backend_type: CodecBackendType,
        picture_format: PictureFormat,
        output_memory_type: ImageMemoryType,
        async_mode,
        peer_codec: "Codec" = None,
        enable_logs: bool = False,
    ):
        Codec.__init__(
            self,
            init_frame_width,
            init_frame_height,
            CodecType.DECODER,
            codec_backend_type,
            picture_format,
            output_memory_type,
            async_mode,
            peer_codec,
            enable_logs,
        )

    def read(
        self, input_path: str, frame_region=FrameRegion(echelon=0)
    ) -> vc6il.vc6_il_io_t:
        # initializing the input and output pointers
        status, input_io = vc6il.vc6_il_get_input_io(self.codec)
        _raise_if_vc6_error(status)
        status, output_io = vc6il.vc6_il_get_output_io(self.codec)
        _raise_if_vc6_error(status)

        # read input file to input object. Do partial read if LoQ 0 is not the target
        echelon = frame_region._region.echelon
        with open(input_path, "rb") as f:
            if echelon == 0:
                read_size = f.readinto(input_io.get_memoryview())
                input_io.size = read_size
            else:
                headers = f.read(2048)
                if headers is None:
                    raise Exception("Failed to inspect VC-6 headers")
                partial_size = GetRequiredSizeForTargetEchelon(headers, echelon)
                input_io.size = partial_size
                f.seek(0)
                read_size = f.readinto(input_io.get_memoryview())
                if read_size != input_io.size:
                    raise Exception("Failed to read VC-6 file for decode")

        self._reconfigure(input_io)
        # encoding the image to output_io pointer
        status = vc6il.vc6_il_decode(
            self.codec, input_io, frame_region._region, output_io
        )
        _raise_if_vc6_error(status)
        return output_io

    def decode(
        self,
        input_buffer: "bytes | bytearray | memoryview",
        frame_region=FrameRegion(echelon=0),
    ) -> tuple[vc6il.vc6_il_io_t, vc6il.vc6_il_io_t]:
        # initializing the input and output pointers
        input_io = None
        if input_buffer is not None:
            input_io = vc6il.vc6_il_io_t()
            vc6il.vc6_io_set_from_py_buffer(input_buffer, input_io)
            self._reconfigure(input_io)
        status, output_io = vc6il.vc6_il_get_output_io(self.codec)
        _raise_if_vc6_error(status)
        # encoding the image to output_io pointer
        status = vc6il.vc6_il_decode(
            self.codec, input_io, frame_region._region, output_io
        )
        _raise_if_vc6_error(status)
        return input_io, output_io

    def open(self, input_buffer: "bytes | bytearray | memoryview") -> None:
        input_io = vc6il.vc6_il_io_t()
        vc6il.vc6_io_set_from_py_buffer(input_buffer, input_io)
        self._reconfigure(input_io)
        status = vc6il.vc6_il_decoder_open(self.codec, input_io)
        _raise_if_vc6_error(status)

    def close(self) -> None:
        status = vc6il.vc6_il_decoder_close(self.codec)
        _raise_if_vc6_error(status)

    def _reconfigure(self, input_io):
        _probe_result = vc6il.vc6_il_frame_probe_result_t()
        status = vc6il.vc6_il_probe_frame(input_io, _probe_result)
        _raise_if_vc6_error(status)
        self.reconfigure(_probe_result.width, _probe_result.height, self.picture_format)


class DecoderSync(DecoderBase):
    def __init__(
        self,
        init_frame_width: int,
        init_frame_height: int,
        codec_backend_type: CodecBackendType,
        picture_format: PictureFormat,
        raw_image_memory_type: ImageMemoryType = ImageMemoryType.CPU,
        peer_codec: "Codec" = None,
        enable_logs: bool = False,
    ):
        DecoderBase.__init__(
            self,
            init_frame_width,
            init_frame_height,
            codec_backend_type,
            picture_format,
            raw_image_memory_type,
            False,
            peer_codec,
            enable_logs,
        )

    def read(
        self, input_path: str, frame_region=FrameRegion(echelon=0)
    ) -> ImageBuffer:
        output_io = DecoderBase.read(self, input_path, frame_region)
        return ImageBuffer(self.raw_memory_type, output_io, self)

    def decode(
        self,
        input_buffer: "bytes | bytearray | memoryview",
        frame_region=FrameRegion(echelon=0),
    ) -> ImageBuffer:
        _, output_io = DecoderBase.decode(self, input_buffer, frame_region)
        return ImageBuffer(self.raw_memory_type, output_io, self)

    def write(
        self, input_buffer: "bytes | bytearray | memoryview", output_path: str, frame_region=FrameRegion(echelon=0)
    ) -> None:
        # initializing the input and output pointers
        input_io = None
        if input_buffer is not None:
            input_io = vc6il.vc6_il_io_t()
            vc6il.vc6_io_set_from_py_buffer(input_buffer, input_io)
            self._reconfigure(input_io)
        status, output_io = vc6il.vc6_il_get_output_io(self.codec)
        _raise_if_vc6_error(status)

        # decoding the image to output_io pointer
        status = vc6il.vc6_il_decode(self.codec, input_io, frame_region._region, output_io)
        _raise_if_vc6_error(status)

        with open(output_path, "wb") as f:
            f.write(output_io.get_memoryview())

        # returning the output memory
        status = vc6il.vc6_il_return_output_io(self.codec, output_io)
        _raise_if_vc6_error(status)


class DecoderAsync(DecoderBase):
    def __init__(
        self,
        init_frame_width: int,
        init_frame_height: int,
        codec_backend_type: CodecBackendType,
        picture_format: PictureFormat,
        output_memory_type: ImageMemoryType,
        peer_codec: "Codec" = None,
        enable_logs: bool = False
    ):
        DecoderBase.__init__(
            self,
            init_frame_width,
            init_frame_height,
            codec_backend_type,
            picture_format,
            output_memory_type,
            True,
            peer_codec,
            enable_logs,
        )

    def decode(
        self,
        input_buffer: "bytes | bytearray | memoryview",
        frame_region=FrameRegion(echelon=0),
    ) -> AsyncImageBuffer:
        input_io, _ = DecoderBase.decode(self, input_buffer, frame_region)
        return AsyncImageBuffer(self.raw_memory_type, self, input_io)

    def read(
        self,
        input_path,
        frame_region=FrameRegion(echelon=0),
    ) -> ImageBuffer:
        _ = DecoderBase.read(self, input_path, frame_region)
        return AsyncImageBuffer(self.raw_memory_type, self, None)

class BatchDecoder():
    def __init__(
        self,
        init_frame_width: int,
        init_frame_height: int,
        codec_backend_type: CodecBackendType,
        picture_format: PictureFormat,
        output_memory_type: ImageMemoryType,
        enable_logs: bool,
        num_backends: int,
        num_buffers: int
    ):
        if not isinstance(output_memory_type, ImageMemoryType):
            raise Exception(
                "output_memory_type parameter should be a member of ImageMemoryType enum"
            )
        if output_memory_type == ImageMemoryType.CUDA_DEVICE and cupy_module is None:
            raise Exception(
                "With output_memory_type == CUDA_DEVICE, a cuda version of vc6 should be used and cupy module should be imported"
            )
        self._decoders_c = vc6il.new_Vc6DecoderArray(num_backends)
        self._decoders_py = [None] * num_backends
        self._output_buffers = [None] * num_buffers
        self._output_memory_type = output_memory_type
        for i in range(num_backends):
            # we indicate raw buffer as CPU we allocate the GPU ones externally
            self._decoders_py[i] = DecoderSync(init_frame_width, init_frame_height, codec_backend_type, picture_format, output_memory_type, None, enable_logs)
            vc6il.vc6_il_decoder_carray_set_item(self._decoders_c, i, self._decoders_py[i].codec)
        self.buffer_size = init_frame_width * init_frame_height * 3
        if output_memory_type == ImageMemoryType.CUDA_DEVICE:
            for i in range(num_buffers):
                self._output_buffers[i] = cupy_module.zeros(self.buffer_size, dtype=cupy_module.uint8, order="C")
        else:
            for i in range(num_buffers):
                self._output_buffers[i] = bytearray(self.buffer_size,)

    def decode(
        self,
        input_buffers: "list[bytes] | list[bytearray] | list[memoryview]",
        echelons: "int | list[int]"
    ) -> list[ImageBuffer]:
        num_images = len(input_buffers)

        while num_images > len(self._output_buffers):
            if self._output_memory_type == ImageMemoryType.CUDA_DEVICE:
                self._output_buffers.append(cupy_module.zeros(self.buffer_size, dtype=cupy_module.uint8, order="C"))
            else:
                self._output_buffers.append(bytearray(self.buffer_size))

        output_images = [None] * num_images
        input_io_array = vc6il.new_Vc6IOArray(num_images)
        output_io_array = vc6il.new_Vc6IOArray(num_images)
        num_echelons = 1
        if isinstance(echelons, Iterable):
            num_echelons = len(echelons)
        else:
            echelons = [echelons]
        echelon_array = vc6il.new_Vc6EchelonArray(num_echelons)
        tmp_io = vc6il.vc6_il_io_t()
        for i in range(num_images):
            vc6il.vc6_il_io_carray_set_item(input_io_array, i, input_buffers[i])
            if self._output_memory_type == ImageMemoryType.CUDA_DEVICE:
                tmp_interface = self._output_buffers[i].__cuda_array_interface__
                if(tmp_interface['version'] != 3):
                    raise Exception(
                    "Cupy __cuda_array_interface__ versions lower than 3 are not supported"
                    )
                tmp_io.clear()
                tmp_io.data = tmp_interface['data'][0]
                tmp_io.size = tmp_interface['shape'][0]
                vc6il.Vc6IOArray_setitem(output_io_array, i, tmp_io)
            else:
                vc6il.vc6_il_io_carray_set_item(output_io_array, i, self._output_buffers[i])
            if i < num_echelons :
                vc6il.Vc6EchelonArray_setitem(echelon_array, i, echelons[i])
        vc6il.vc6_il_batch_decode(len(self._decoders_py), self._decoders_c, num_images, input_io_array, output_io_array, num_echelons, echelon_array)

        for i in range(num_images):
            output_images[i] = ImageBuffer(self._output_memory_type, vc6il.Vc6IOArray_getitem(output_io_array, i), None)
        return output_images
