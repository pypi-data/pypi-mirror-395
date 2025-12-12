import enum

import sourcepp._sourcepp_impl.vtfpp


DEFAULT_COMPRESSED_QUALITY: float = -1.0

def convert_image_data_to_format(image_data: bytes, old_format: sourcepp._sourcepp_impl.vtfpp.ImageFormat, new_format: sourcepp._sourcepp_impl.vtfpp.ImageFormat, width: int, height: int, quality: float = -1.0) -> bytes: ...

def convert_several_image_data_to_format(image_data: bytes, old_format: sourcepp._sourcepp_impl.vtfpp.ImageFormat, new_format: sourcepp._sourcepp_impl.vtfpp.ImageFormat, mip_count: int, frame_count: int, face_count: int, width: int, height: int, depth: int, quality: float = -1.0) -> bytes: ...

def convert_hdri_to_cubemap(image_data: bytes, format: sourcepp._sourcepp_impl.vtfpp.ImageFormat, width: int, height: int, resolution: int = 0, bilinear: bool = True) -> tuple[bytes, bytes, bytes, bytes, bytes, bytes]: ...

class FileFormat(enum.Enum):
    DEFAULT = 0

    PNG = 1

    JPG = 2

    BMP = 3

    TGA = 4

    WEBP = 5

    QOI = 6

    HDR = 7

    EXR = 8

def get_default_file_format_for_image_format(format: sourcepp._sourcepp_impl.vtfpp.ImageFormat) -> FileFormat: ...

def convert_image_data_to_file(image_data: bytes, format: sourcepp._sourcepp_impl.vtfpp.ImageFormat, width: int, height: int, file_format: FileFormat = FileFormat.DEFAULT) -> bytes: ...

def convert_file_to_image_data(file_data: bytes) -> tuple[bytes, sourcepp._sourcepp_impl.vtfpp.ImageFormat, int, int, int]: ...

class ResizeEdge(enum.Enum):
    CLAMP = 0

    REFLECT = 1

    WRAP = 2

    ZERO = 3

class ResizeFilter(enum.Enum):
    DEFAULT = 0

    BOX = 1

    BILINEAR = 2

    CUBIC_BSPLINE = 3

    CATMULL_ROM = 4

    MITCHELL = 5

    POINT_SAMPLE = 6

    KAISER = 100

    NICE = 101

class ResizeMethod(enum.Enum):
    NONE = 0

    POWER_OF_TWO_BIGGER = 1

    POWER_OF_TWO_SMALLER = 2

    POWER_OF_TWO_NEAREST = 3

def get_resized_dim(n: int, resize_method: ResizeMethod) -> int: ...

def get_resized_dims(width: int, resize_width: ResizeMethod, height: int, resize_height: ResizeMethod) -> tuple[int, int]: ...

def resize_image_data(image_data: bytes, format: sourcepp._sourcepp_impl.vtfpp.ImageFormat, width: int, new_width: int, height: int, new_height: int, srgb: bool, filter: ResizeFilter, edge: ResizeEdge = ResizeEdge.CLAMP) -> bytes: ...

def resize_image_data_strict(image_data: bytes, format: sourcepp._sourcepp_impl.vtfpp.ImageFormat, width: int, new_width: int, width_resize: ResizeMethod, height: int, new_height: int, height_resize: ResizeMethod, srgb: bool, filter: ResizeFilter, edge: ResizeEdge = ResizeEdge.CLAMP) -> tuple[bytes, int, int]: ...

def crop_image_data(image_data: bytes, format: sourcepp._sourcepp_impl.vtfpp.ImageFormat, width: int, new_width: int, x_offset: int, height: int, new_height: int, y_offset: int) -> bytes: ...

def pad_image_data(image_data: bytes, format: sourcepp._sourcepp_impl.vtfpp.ImageFormat, width: int, width_pad: int, height: int, height_pad: int) -> bytes: ...

def gamma_correct_image_data(image_data: bytes, format: sourcepp._sourcepp_impl.vtfpp.ImageFormat, width: int, height: int, gamma: float) -> bytes: ...

def invert_green_channel_for_image_data(image_data: bytes, format: sourcepp._sourcepp_impl.vtfpp.ImageFormat, width: int, height: int) -> bytes: ...
