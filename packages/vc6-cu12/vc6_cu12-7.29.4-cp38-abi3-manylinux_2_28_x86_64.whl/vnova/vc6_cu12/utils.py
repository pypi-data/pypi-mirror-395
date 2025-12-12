if __package__ or "." in __name__:
    from . import Vc6Utils
    from . import codec
else:
    import Vc6Utils
    import codec

from pathlib import Path

class VideoReader:
    def __init__(self, video_path : str):
        self._reader = Vc6Utils.vc6_il_util_video_reader_create(video_path)

    def __del__(self):
        if self._reader is not None:
            Vc6Utils.vc6_il_util_vr_destroy(self._reader)


    @property
    def size(self): return Vc6Utils.vc6_il_util_vr_get_frame_size(self._reader)
    @property
    def frame_count(self): return Vc6Utils.vc6_il_util_vr_get_length(self._reader)
    @property
    def fps(self): return Vc6Utils.vc6_il_util_vr_get_rate(self._reader)
    @property
    def version(self): return Vc6Utils.vc6_il_util_vr_get_frame_version(self._reader)

    def tell(self): return Vc6Utils.vc6_il_util_vr_get_position(self._reader)
    def seek(self, idx: int): return Vc6Utils.vc6_il_util_vr_set_position(self._reader, idx)
    def seek_relative(self, delta:int): return Vc6Utils.vc6_il_util_vr_set_position_relative(self._reader, delta)
    def eof(self): return Vc6Utils.vc6_il_util_vr_is_eof(self._reader)

    def read(self) -> bytearray: 
        buffer = bytearray(self.size)

        ok = Vc6Utils.vc6_il_util_vr_read(self._reader, buffer)
        if ok:
            return buffer
        else:
            print("failed to read");
            return bytearray()

    def readinto(self, buffer: "bytes | bytearray | memoryview"):
        if buffer is None:
            print("invalid buffer")
            return
        else:
            ok = Vc6Utils.vc6_il_util_vr_read(self._reader, buffer)
            if not ok:
                print("failed to read");
                return

class VideoWriter:
    def __init__(self, video_path : str, format : codec.PictureFormat, width: int, height: int, target_bitdepth:int , fps:int, fps_den:int = 1):
        path = Path(video_path)
        self._writer = None
        if path.suffix == ".mxf":
            self._writer = Vc6Utils.vc6_il_util_video_writer_create_mxf(str(path), format.value, width, height, target_bitdepth, fps, fps_den)
        elif path.suffix == ".vc6":
            self._writer = Vc6Utils.vc6_il_util_video_writer_create(str(path), format.value, width, height, target_bitdepth, fps, fps_den)
        else: 
            print("invalid extension")

    def __del__(self):
        Vc6Utils.vc6_il_util_video_writer_destroy(self._writer)

    def write_frame(self, input_buffer: "bytes | bytearray | memoryview") -> bool:
        return Vc6Utils.vc6_il_util_video_writer_write_frame(self._writer, input_buffer)

    def finalize(self) -> bool:
        return Vc6Utils.vc6_il_util_video_writer_finalise(self._writer);
