from collections.abc import Sequence
import enum
from typing import overload

from . import (
    ImageConversion as ImageConversion,
    ImageDimensions as ImageDimensions,
    ImageFormatDetails as ImageFormatDetails,
    ImageQuantize as ImageQuantize
)
import sourcepp._sourcepp_impl.sourcepp.math


class HOT:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, hot_data: bytes) -> HOT: ...

    @overload
    def __init__(self, hot_path: str) -> None: ...

    class Rect:
        class Flags(enum.Flag):
            NONE = 0

            RANDOM_ROTATION = 1

            RANDOM_REFLECTION = 2

            IS_ALTERNATE = 4

        @property
        def flags(self) -> HOT.Rect.Flags: ...

        @flags.setter
        def flags(self, arg: HOT.Rect.Flags, /) -> None: ...

        @property
        def x1(self) -> int: ...

        @x1.setter
        def x1(self, arg: int, /) -> None: ...

        @property
        def y1(self) -> int: ...

        @y1.setter
        def y1(self, arg: int, /) -> None: ...

        @property
        def x2(self) -> int: ...

        @x2.setter
        def x2(self, arg: int, /) -> None: ...

        @property
        def y2(self) -> int: ...

        @y2.setter
        def y2(self, arg: int, /) -> None: ...

    def __bool__(self) -> bool: ...

    @property
    def version(self) -> int: ...

    @version.setter
    def version(self, arg: int, /) -> None: ...

    @property
    def flags(self) -> int: ...

    @flags.setter
    def flags(self, arg: int, /) -> None: ...

    @property
    def rects(self) -> list[HOT.Rect]: ...

    @rects.setter
    def rects(self, arg: Sequence[HOT.Rect], /) -> None: ...

    def bake(self) -> bytes: ...

    def bake_to_file(self, hot_path: str) -> bool: ...

class ImageFormat(enum.Enum):
    RGBA8888 = 0

    ABGR8888 = 1

    RGB888 = 2

    BGR888 = 3

    RGB565 = 4

    I8 = 5

    IA88 = 6

    P8 = 7

    A8 = 8

    RGB888_BLUESCREEN = 9

    BGR888_BLUESCREEN = 10

    ARGB8888 = 11

    BGRA8888 = 12

    DXT1 = 13

    DXT3 = 14

    DXT5 = 15

    BGRX8888 = 16

    BGR565 = 17

    BGRX5551 = 18

    BGRA4444 = 19

    DXT1_ONE_BIT_ALPHA = 20

    BGRA5551 = 21

    UV88 = 22

    UVWQ8888 = 23

    RGBA16161616F = 24

    RGBA16161616 = 25

    UVLX8888 = 26

    R32F = 27

    RGB323232F = 28

    RGBA32323232F = 29

    RG1616F = 30

    RG3232F = 31

    RGBX8888 = 32

    EMPTY = 33

    ATI2N = 34

    ATI1N = 35

    RGBA1010102 = 36

    BGRA1010102 = 37

    R16F = 38

    R8 = 69

    BC7 = 70

    BC6H = 71

class PPL:
    @overload
    def __init__(self, model_checksum: int, format: ImageFormat = ImageFormat.RGB888, version: int = 0) -> None: ...

    @overload
    def __init__(self, ppl_data: bytes) -> PPL: ...

    @overload
    def __init__(self, path: str) -> None: ...

    class Image:
        @property
        def width(self) -> int: ...

        @property
        def height(self) -> int: ...

        @property
        def data(self) -> bytes: ...

    def __bool__(self) -> bool: ...

    @property
    def version(self) -> int: ...

    @version.setter
    def version(self, arg: int, /) -> None: ...

    @property
    def model_checksum(self) -> int: ...

    @model_checksum.setter
    def model_checksum(self, arg: int, /) -> None: ...

    @property
    def format(self) -> ImageFormat: ...

    def set_format(self, new_format: ImageFormat, quality: float = -1.0) -> None: ...

    def has_image_for_lod(self, lod: int) -> bool: ...

    @property
    def image_lods(self) -> list[int]: ...

    def get_image_raw(self, lod: int) -> PPL.Image | None: ...

    def get_image_as(self, new_format: ImageFormat, lod: int) -> PPL.Image | None: ...

    def get_image_as_rgb888(self, lod: int) -> PPL.Image | None: ...

    def set_image(self, imageData: bytes, format: ImageFormat, width: int, height: int, lod: int = 0, quality: float = -1.0) -> None: ...

    def set_image_resized(self, imageData: bytes, format: ImageFormat, width: int, height: int, resized_width: int, resized_height: int, lod: int = 0, filter: ImageConversion.ResizeFilter = ImageConversion.ResizeFilter.DEFAULT, quality: float = -1.0) -> None: ...

    def set_image_from_file(self, image_path: str, lod: int = 0, quality: float = -1.0) -> bool: ...

    def set_image_resized_from_file(self, image_path: str, resized_width: int, resized_height: int, lod: int = 0, filter: ImageConversion.ResizeFilter = ImageConversion.ResizeFilter.DEFAULT, quality: float = -1.0) -> bool: ...

    def save_image(self, lod: int = 0, file_format: ImageConversion.FileFormat = ImageConversion.FileFormat.DEFAULT) -> bytes: ...

    def save_image_to_file(self, image_path: str, lod: int = 0, file_format: ImageConversion.FileFormat = ImageConversion.FileFormat.DEFAULT) -> bool: ...

    def bake(self) -> bytes: ...

    def bake_to_file(self, ppl_path: str) -> bool: ...

class PSFrames:
    @overload
    def __init__(self, ps_frames_data: bytes) -> PSFrames: ...

    @overload
    def __init__(self, ps_frames_path: str) -> None: ...

    @property
    def frame_count(self) -> int: ...

    @property
    def fps(self) -> int: ...

    @property
    def width(self) -> int: ...

    @property
    def height(self) -> int: ...

    def get_image_data_as(self, new_format: ImageFormat, frame: int) -> bytes: ...

    def get_image_data_as_bgr888(self, frame: int) -> bytes: ...

class SHT:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, sht_data: bytes) -> SHT: ...

    @overload
    def __init__(self, sht_path: str) -> None: ...

    class Sequence:
        class Frame:
            class Bounds:
                @property
                def x1(self) -> float: ...

                @x1.setter
                def x1(self, arg: float, /) -> None: ...

                @property
                def y1(self) -> float: ...

                @y1.setter
                def y1(self, arg: float, /) -> None: ...

                @property
                def x2(self) -> float: ...

                @x2.setter
                def x2(self, arg: float, /) -> None: ...

                @property
                def y2(self) -> float: ...

                @y2.setter
                def y2(self, arg: float, /) -> None: ...

            @property
            def duration(self) -> float: ...

            @duration.setter
            def duration(self, arg: float, /) -> None: ...

            @property
            def bounds(self) -> list[SHT.Sequence.Frame.Bounds]: ...

            @bounds.setter
            def bounds(self, arg: Sequence[SHT.Sequence.Frame.Bounds], /) -> None: ...

            def set_all_bounds(self, newBounds: SHT.Sequence.Frame.Bounds) -> None: ...

        @property
        def id(self) -> int: ...

        @id.setter
        def id(self, arg: int, /) -> None: ...

        @property
        def loop(self) -> bool: ...

        @loop.setter
        def loop(self, arg: bool, /) -> None: ...

        @property
        def frames(self) -> list[SHT.Sequence.Frame]: ...

        @frames.setter
        def frames(self, arg: Sequence[SHT.Sequence.Frame], /) -> None: ...

        @property
        def duration_total(self) -> float: ...

        @duration_total.setter
        def duration_total(self, arg: float, /) -> None: ...

    def __bool__(self) -> bool: ...

    @property
    def version(self) -> int: ...

    @version.setter
    def version(self, arg: int, /) -> None: ...

    @property
    def sequences(self) -> list[SHT.Sequence]: ...

    @sequences.setter
    def sequences(self, arg: Sequence[SHT.Sequence], /) -> None: ...

    def get_sequence_from_id(self, id: int) -> SHT.Sequence: ...

    def get_frame_bounds_count(self) -> int: ...

    def bake(self) -> bytes: ...

    def bake_to_file(self, sht_path: str) -> bool: ...

TTH_SIGNATURE: int = 4740180

class VTF:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, vtf_data: bytes, parse_header_only: bool = False) -> VTF: ...

    @overload
    def __init__(self, vtf_path: str, parse_header_only: bool = False) -> None: ...

    class Flags(enum.Flag):
        V0_POINT_SAMPLE = 1

        V0_TRILINEAR = 2

        V0_CLAMP_S = 4

        V0_CLAMP_T = 8

        V0_ANISOTROPIC = 16

        V0_VTEX_HINT_DXT5 = 32

        V0_VTEX_NO_COMPRESS = 64

        V0_NORMAL = 128

        V0_NO_MIP = 256

        V0_NO_LOD = 512

        V0_LOAD_SMALL_MIPS = 1024

        V0_PROCEDURAL = 2048

        V0_ONE_BIT_ALPHA = 4096

        V0_MULTI_BIT_ALPHA = 8192

        V0_ENVMAP = 16384

        MASK_V0 = 32767

        MASK_V0_VTEX = 96

        V1_RENDERTARGET = 32768

        V1_DEPTH_RENDERTARGET = 65536

        V1_NO_DEBUG_OVERRIDE = 131072

        V1_SINGLE_COPY = 262144

        V1_VTEX_ONE_OVER_MIP_LEVEL_IN_ALPHA = 524288

        V1_VTEX_PREMULTIPLY_COLOR_BY_ONE_OVER_MIP_LEVEL = 1048576

        V1_VTEX_CONVERT_NORMAL_TO_DUDV = 2097152

        MASK_V1 = 4161536

        MASK_V1_VTEX = 3670016

        V2_VTEX_ALPHA_TEST_MIP_GENERATION = 4194304

        V2_NO_DEPTH_BUFFER = 8388608

        V2_VTEX_NICE_FILTERED = 16777216

        V2_CLAMP_U = 33554432

        MASK_V2 = 62914560

        MASK_V2_VTEX = 20971520

        XBOX_VTEX_PRESWIZZLED = 67108864

        XBOX_CACHEABLE = 134217728

        XBOX_UNFILTERABLE_OK = 268435456

        MASK_XBOX = 469762048

        MASK_XBOX_VTEX = 67108864

        V3_LOAD_ALL_MIPS = 1024

        V3_VERTEX_TEXTURE = 67108864

        V3_SSBUMP = 134217728

        V3_BORDER = 536870912

        MASK_V3 = 738198528

        V4_SRGB = 64

        MASK_V4 = 64

        V4_TF2_STAGING_MEMORY = 524288

        V4_TF2_IMMEDIATE_CLEANUP = 1048576

        V4_TF2_IGNORE_PICMIP = 2097152

        V4_TF2_STREAMABLE_COARSE = 1073741824

        V4_TF2_STREAMABLE_FINE = 2147483648

        MASK_V4_TF2 = 3224895488

        V5_PWL_CORRECTED = 64

        V5_SRGB = 524288

        V5_DEFAULT_POOL = 1048576

        V5_LOAD_MOST_MIPS = 268435456

        MASK_V5 = 270008384

        V5_CSGO_COMBINED = 2097152

        V5_CSGO_ASYNC_DOWNLOAD = 4194304

        V5_CSGO_SKIP_INITIAL_DOWNLOAD = 16777216

        V5_CSGO_YCOCG = 1073741824

        V5_CSGO_ASYNC_SKIP_INITIAL_LOW_RES = 2147483648

        MASK_V5_CSGO = 3244294144

        MASK_INTERNAL = 16640

    class Platform(enum.Enum):
        UNKNOWN = 0

        PC = 7

        XBOX = 5

        X360 = 864

        PS3_ORANGEBOX = 819

        PS3_PORTAL2 = 820

    class CreationOptions:
        def __init__(self) -> None: ...

        @property
        def version(self) -> int: ...

        @version.setter
        def version(self, arg: int, /) -> None: ...

        @property
        def output_format(self) -> ImageFormat: ...

        @output_format.setter
        def output_format(self, arg: ImageFormat, /) -> None: ...

        @property
        def width_resize_method(self) -> ImageConversion.ResizeMethod: ...

        @width_resize_method.setter
        def width_resize_method(self, arg: ImageConversion.ResizeMethod, /) -> None: ...

        @property
        def height_resize_method(self) -> ImageConversion.ResizeMethod: ...

        @height_resize_method.setter
        def height_resize_method(self, arg: ImageConversion.ResizeMethod, /) -> None: ...

        @property
        def filter(self) -> ImageConversion.ResizeFilter: ...

        @filter.setter
        def filter(self, arg: ImageConversion.ResizeFilter, /) -> None: ...

        @property
        def flags(self) -> int: ...

        @flags.setter
        def flags(self, arg: int, /) -> None: ...

        @property
        def initial_frame_count(self) -> int: ...

        @initial_frame_count.setter
        def initial_frame_count(self, arg: int, /) -> None: ...

        @property
        def start_frame(self) -> int: ...

        @start_frame.setter
        def start_frame(self, arg: int, /) -> None: ...

        @property
        def is_cubemap(self) -> bool: ...

        @is_cubemap.setter
        def is_cubemap(self, arg: bool, /) -> None: ...

        @property
        def initial_depth(self) -> int: ...

        @initial_depth.setter
        def initial_depth(self, arg: int, /) -> None: ...

        @property
        def compute_transparency_flags(self) -> bool: ...

        @compute_transparency_flags.setter
        def compute_transparency_flags(self, arg: bool, /) -> None: ...

        @property
        def compute_mips(self) -> bool: ...

        @compute_mips.setter
        def compute_mips(self, arg: bool, /) -> None: ...

        @property
        def compute_thumbnail(self) -> bool: ...

        @compute_thumbnail.setter
        def compute_thumbnail(self, arg: bool, /) -> None: ...

        @property
        def compute_reflectivity(self) -> bool: ...

        @compute_reflectivity.setter
        def compute_reflectivity(self, arg: bool, /) -> None: ...

        @property
        def compression_level(self) -> int: ...

        @compression_level.setter
        def compression_level(self, arg: int, /) -> None: ...

        @property
        def compression_method(self) -> CompressionMethod: ...

        @compression_method.setter
        def compression_method(self, arg: CompressionMethod, /) -> None: ...

        @property
        def bumpmap_scale(self) -> float: ...

        @bumpmap_scale.setter
        def bumpmap_scale(self, arg: float, /) -> None: ...

        @property
        def gamma_correction(self) -> float: ...

        @gamma_correction.setter
        def gamma_correction(self, arg: float, /) -> None: ...

        @property
        def invert_green_channel(self) -> bool: ...

        @invert_green_channel.setter
        def invert_green_channel(self, arg: bool, /) -> None: ...

        @property
        def console_mip_scale(self) -> int: ...

        @console_mip_scale.setter
        def console_mip_scale(self, arg: int, /) -> None: ...

    FORMAT_UNCHANGED: sourcepp._sourcepp_impl.vtfpp.ImageFormat = ...
    """(arg: object, /) -> sourcepp._sourcepp_impl.vtfpp.ImageFormat"""

    FORMAT_DEFAULT: sourcepp._sourcepp_impl.vtfpp.ImageFormat = ...
    """(arg: object, /) -> sourcepp._sourcepp_impl.vtfpp.ImageFormat"""

    def __bool__(self) -> bool: ...

    @staticmethod
    def create_and_bake(image_data: bytes, format: ImageFormat, width: int, height: int, vtf_path: str, creation_options: VTF.CreationOptions = ...) -> None: ...

    @staticmethod
    def create_blank_and_bake(format: ImageFormat, width: int, height: int, vtf_path: str, creation_options: VTF.CreationOptions = ...) -> bool: ...

    @staticmethod
    def create(image_data: bytes, format: ImageFormat, width: int, height: int, creation_options: VTF.CreationOptions = ...) -> VTF: ...

    @staticmethod
    def create_blank(format: ImageFormat, width: int, height: int, creation_options: VTF.CreationOptions = ...) -> VTF: ...

    @staticmethod
    def create_from_file_and_bake(image_path: str, vtf_path: str, creation_options: VTF.CreationOptions = ...) -> bool: ...

    @staticmethod
    def create_from_file(image_path: str, creation_options: VTF.CreationOptions = ...) -> VTF: ...

    @property
    def platform(self) -> VTF.Platform: ...

    @platform.setter
    def platform(self, arg: VTF.Platform, /) -> None: ...

    @property
    def version(self) -> int: ...

    @version.setter
    def version(self, arg: int, /) -> None: ...

    @property
    def image_width_resize_method(self) -> ImageConversion.ResizeMethod: ...

    @image_width_resize_method.setter
    def image_width_resize_method(self, arg: ImageConversion.ResizeMethod, /) -> None: ...

    @property
    def image_height_resize_method(self) -> ImageConversion.ResizeMethod: ...

    @image_height_resize_method.setter
    def image_height_resize_method(self, arg: ImageConversion.ResizeMethod, /) -> None: ...

    @property
    def width(self) -> int: ...

    def width_for_mip(self, mip: int = 0) -> int: ...

    @property
    def padded_width(self) -> int: ...

    def padded_width_for_mip(self, mip: int = 0) -> int: ...

    @property
    def height(self) -> int: ...

    def height_for_mip(self, mip: int = 0) -> int: ...

    @property
    def padded_height(self) -> int: ...

    def padded_height_for_mip(self, mip: int = 0) -> int: ...

    def set_size(self, width: int, height: int, filter: ImageConversion.ResizeFilter) -> None: ...

    @property
    def flags(self) -> int: ...

    @flags.setter
    def flags(self, arg: int, /) -> None: ...

    def add_flags(self, flags: int) -> None: ...

    def remove_flags(self, flags: int) -> None: ...

    def is_srgb(self) -> bool: ...

    def set_srgb(self, srgb: bool) -> None: ...

    def compute_transparency_flags(self) -> None: ...

    @staticmethod
    def get_default_compressed_format(input_format: ImageFormat, version: int, is_cubemap: bool) -> ImageFormat: ...

    @property
    def format(self) -> ImageFormat: ...

    def set_format(self, new_format: ImageFormat, filter: ImageConversion.ResizeFilter = ImageConversion.ResizeFilter.DEFAULT, quality: float = -1.0) -> None: ...

    @property
    def mip_count(self) -> int: ...

    @mip_count.setter
    def mip_count(self, arg: int, /) -> bool: ...

    def set_recommended_mip_count(self) -> bool: ...

    def compute_mips(self, filter: ImageConversion.ResizeFilter = ImageConversion.ResizeFilter.DEFAULT) -> None: ...

    @property
    def frame_count(self) -> int: ...

    @frame_count.setter
    def frame_count(self, arg: int, /) -> bool: ...

    @property
    def face_count(self) -> int: ...

    def set_face_count(self, is_cubemap: bool) -> bool: ...

    @property
    def depth(self) -> int: ...

    def depth_for_mip(self, mip: int = 0) -> int: ...

    def set_frame_face_and_depth(self, new_frame_count: int, is_cubemap: bool, new_depth: int = 1) -> bool: ...

    @property
    def start_frame(self) -> int: ...

    @start_frame.setter
    def start_frame(self, arg: int, /) -> None: ...

    @property
    def reflectivity(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec3f32: ...

    @reflectivity.setter
    def reflectivity(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec3f32, /) -> None: ...

    def compute_reflectivity(self) -> None: ...

    @property
    def bumpmap_scale(self) -> float: ...

    @bumpmap_scale.setter
    def bumpmap_scale(self, arg: float, /) -> None: ...

    @property
    def thumbnail_format(self) -> ImageFormat: ...

    @property
    def thumbnail_width(self) -> int: ...

    @property
    def thumbnail_height(self) -> int: ...

    @property
    def fallback_width(self) -> int: ...

    @property
    def fallback_height(self) -> int: ...

    @property
    def fallback_mip_count(self) -> int: ...

    def get_resource(self, type: Resource.Type) -> Resource: ...

    def get_palette_resource_frame(self, type: int) -> bytes: ...

    def get_particle_sheet_frame_data_raw(self, sht_sequence_id: int, sht_frame: int, sht_bounds: int = 0, mip: int = 0, frame: int = 0, face: int = 0, slice: int = 0) -> tuple[int, int, bytes]: ...

    def get_particle_sheet_frame_data_as(self, format: ImageFormat, sht_sequence_id: int, sht_frame: int, sht_bounds: int = 0, mip: int = 0, frame: int = 0, face: int = 0, slice: int = 0) -> tuple[int, int, bytes]: ...

    def get_particle_sheet_frame_data_as_rgba8888(self, sht_sequence_id: int, sht_frame: int, sht_bounds: int = 0, mip: int = 0, frame: int = 0, face: int = 0, slice: int = 0) -> tuple[int, int, bytes]: ...

    def set_particle_sheet_resource(self, value: SHT) -> None: ...

    def remove_particle_sheet_resource(self) -> None: ...

    def set_crc_resource(self, value: int) -> None: ...

    def remove_crc_resource(self) -> None: ...

    def set_lod_resource(self, u: int, v: int, u360: int = 0, v360: int = 0) -> None: ...

    def remove_lod_resource(self) -> None: ...

    def set_extended_flags_resource(self, value: int) -> None: ...

    def remove_extended_flags_resource(self) -> None: ...

    def set_keyvalues_data_resource(self, value: str) -> None: ...

    def remove_keyvalues_data_resource(self) -> None: ...

    def set_hotspot_data_resource(self, value: HOT) -> None: ...

    def remove_hotspot_data_resource(self) -> None: ...

    @property
    def compression_level(self) -> int: ...

    @compression_level.setter
    def compression_level(self, arg: int, /) -> None: ...

    @property
    def compression_method(self) -> CompressionMethod: ...

    @compression_method.setter
    def compression_method(self, arg: CompressionMethod, /) -> None: ...

    def has_image_data(self) -> bool: ...

    def get_image_data_raw(self, mip: int = 0, frame: int = 0, face: int = 0, slice: int = 0) -> bytes: ...

    def get_image_data_as(self, new_format: ImageFormat, mip: int = 0, frame: int = 0, face: int = 0, slice: int = 0) -> bytes: ...

    def get_image_data_as_rgba8888(self, mip: int = 0, frame: int = 0, face: int = 0, slice: int = 0) -> bytes: ...

    def set_image(self, image_data: bytes, format: ImageFormat, width: int, height: int, filter: ImageConversion.ResizeFilter, mip: int = 0, frame: int = 0, face: int = 0, slice: int = 0, quality: float = -1.0) -> bool: ...

    def set_image_from_file(self, image_path: str, filter: ImageConversion.ResizeFilter = ImageConversion.ResizeFilter.DEFAULT, mip: int = 0, frame: int = 0, face: int = 0, slice: int = 0, quality: float = -1.0) -> bool: ...

    def save_image(self, mip: int = 0, frame: int = 0, face: int = 0, slice: int = 0, file_format: ImageConversion.FileFormat = ImageConversion.FileFormat.DEFAULT) -> bytes: ...

    def save_image_to_file(self, image_path: str, mip: int = 0, frame: int = 0, face: int = 0, slice: int = 0, file_format: ImageConversion.FileFormat = ImageConversion.FileFormat.DEFAULT) -> bool: ...

    def has_thumbnail_data(self) -> bool: ...

    def get_thumbnail_data_raw(self) -> bytes: ...

    def get_thumbnail_data_as(self, new_format: ImageFormat) -> bytes: ...

    def get_thumbnail_data_as_rgba8888(self) -> bytes: ...

    def set_thumbnail(self, image_data: bytes, format: ImageFormat, width: int, height: int, quality: float = -1.0) -> None: ...

    def set_thumbnail_from_file(self, image_path: str, quality: float = -1.0) -> bool: ...

    def compute_thumbnail(self, filter: ImageConversion.ResizeFilter = ImageConversion.ResizeFilter.DEFAULT, quality: float = -1.0) -> None: ...

    def remove_thumbnail(self) -> None: ...

    def save_thumbnail(self, file_format: ImageConversion.FileFormat = ImageConversion.FileFormat.DEFAULT) -> bytes: ...

    def save_thumbnail_to_file(self, image_path: str, file_format: ImageConversion.FileFormat = ImageConversion.FileFormat.DEFAULT) -> bool: ...

    def has_fallback_data(self) -> bool: ...

    def get_fallback_data_raw(self, mip: int = 0, frame: int = 0, face: int = 0) -> bytes: ...

    def get_fallback_data_as(self, new_format: ImageFormat, mip: int = 0, frame: int = 0, face: int = 0) -> bytes: ...

    def get_fallback_data_as_rgba8888(self, mip: int = 0, frame: int = 0, face: int = 0) -> bytes: ...

    def compute_fallback(self, filter: ImageConversion.ResizeFilter = ImageConversion.ResizeFilter.DEFAULT) -> None: ...

    def remove_fallback(self) -> None: ...

    def save_fallback(self, mip: int = 0, frame: int = 0, face: int = 0, file_format: ImageConversion.FileFormat = ImageConversion.FileFormat.DEFAULT) -> bytes: ...

    def save_fallback_to_file(self, image_path: str, mip: int = 0, frame: int = 0, face: int = 0, file_format: ImageConversion.FileFormat = ImageConversion.FileFormat.DEFAULT) -> bool: ...

    @property
    def console_mip_scale(self) -> int: ...

    @console_mip_scale.setter
    def console_mip_scale(self, arg: int, /) -> None: ...

    def estimate_bake_size(self) -> tuple[int, bool]: ...

    def bake(self) -> bytes: ...

    def bake_to_file(self, vtf_path: str) -> bool: ...

class TTX:
    @overload
    def __init__(self, vtf: VTF) -> None: ...

    @overload
    def __init__(self, tth_data: bytes, ttz_data: bytes) -> TTX: ...

    @overload
    def __init__(self, tth_path: str, ttz_path: str) -> None: ...

    def __bool__(self) -> bool: ...

    @property
    def version_major(self) -> int: ...

    @version_major.setter
    def version_major(self, arg: int, /) -> None: ...

    @property
    def version_minor(self) -> int: ...

    @version_minor.setter
    def version_minor(self, arg: int, /) -> None: ...

    @property
    def aspect_ratio_type(self) -> int: ...

    @aspect_ratio_type.setter
    def aspect_ratio_type(self, arg: int, /) -> None: ...

    @property
    def mip_flags(self) -> list[int]: ...

    @mip_flags.setter
    def mip_flags(self, arg: Sequence[int], /) -> None: ...

    @property
    def vtf(self) -> VTF: ...

    @vtf.setter
    def vtf(self, arg: VTF, /) -> None: ...

    @property
    def compression_level(self) -> int: ...

    @compression_level.setter
    def compression_level(self, arg: int, /) -> None: ...

    def bake(self) -> tuple[bytes, bytes]: ...

    def bake_to_file(self, tth_path: str, ttz_path: str) -> bool: ...

VTF_SIGNATURE: int = 4609110

XTF_SIGNATURE: int = 4609112

VTFX_SIGNATURE: int = 1481004118

VTF3_SIGNATURE: int = 860247126

class CompressionMethod(enum.IntEnum):
    DEFLATE = 8

    ZSTD = 93

    CONSOLE_LZMA = 864

class Resource:
    class Type(enum.Enum):
        UNKNOWN = 0

        THUMBNAIL_DATA = 1

        PALETTE_DATA = 2

        FALLBACK_DATA = 3

        PARTICLE_SHEET_DATA = 16

        HOTSPOT_DATA = 43

        IMAGE_DATA = 48

        EXTENDED_FLAGS = 3167060

        CRC = 4411971

        AUX_COMPRESSION = 4413505

        LOD_CONTROL_INFO = 4476748

        KEYVALUES_DATA = 4478539

    class Flags(enum.Flag):
        NONE = 0

        LOCAL_DATA = 2

    @property
    def type(self) -> Resource.Type: ...

    @property
    def flags(self) -> Resource.Flags: ...

    def get_data_as_palette(self, frame: int = 0) -> list["std::byte"]: ...

    def get_data_as_particle_sheet(self) -> SHT: ...

    def get_data_as_crc(self) -> int: ...

    def get_data_as_extended_flags(self) -> int: ...

    def get_data_as_lod_control_info(self) -> tuple[int, int, int, int]: ...

    def get_data_as_keyvalues_data(self) -> str: ...

    def get_data_as_hotspot_data(self) -> HOT: ...

    def get_data_as_aux_compression_level(self) -> int: ...

    def get_data_as_aux_compression_method(self) -> CompressionMethod: ...

    def get_data_as_aux_compression_length(self, mip: int, mip_count: int, frame: int, frame_count: int, face: int, face_count: int) -> int: ...
