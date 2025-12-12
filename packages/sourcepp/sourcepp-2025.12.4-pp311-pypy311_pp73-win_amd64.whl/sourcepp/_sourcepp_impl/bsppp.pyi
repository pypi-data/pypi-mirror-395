from collections.abc import Callable, Sequence
import enum

import sourcepp._sourcepp_impl.sourcepp.math
import sourcepp._sourcepp_impl.vpkpp


class BSP:
    def __init__(self, path: str, load_patch_files: bool = True) -> None: ...

    class EntityKeyValues:
        def __init__(self) -> None: ...

        class Element:
            __init__: wrapper_descriptor = ...

            @property
            def key(self) -> str: ...

            @key.setter
            def key(self, arg: str, /) -> None: ...

            @property
            def value(self) -> str: ...

            @value.setter
            def value(self, arg: str, /) -> None: ...

            @property
            def invalid(self) -> bool: ...

        def has_child(self, child_key: str) -> bool: ...

        @property
        def keyvalues_count(self) -> int: ...

        def get_keyvalues_count_for_key(self, child_key: str) -> int: ...

        @property
        def keyvalues(self) -> list[BSP.EntityKeyValues.Element]: ...

        def at(self, n: int) -> BSP.EntityKeyValues.Element: ...

        def get(self, child_key: str) -> BSP.EntityKeyValues.Element: ...

        def __getitem__(self, child_key: str) -> BSP.EntityKeyValues.Element: ...

        def get_n(self, child_key: str, n: int) -> BSP.EntityKeyValues.Element: ...

        def add_keyvalue(self, child_key: str, value: str) -> BSP.EntityKeyValues.Element: ...

        def remove_keyvalue(self, child_key: str, n: int = -1) -> None: ...

        def bake(self, use_escapes: bool) -> str: ...

    class Plane_v0:
        def __init__(self) -> None: ...

        @property
        def normal(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec3f32: ...

        @normal.setter
        def normal(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec3f32, /) -> None: ...

        @property
        def dist(self) -> float: ...

        @dist.setter
        def dist(self, arg: float, /) -> None: ...

        @property
        def type(self) -> int: ...

        @type.setter
        def type(self, arg: int, /) -> None: ...

    class TextureData_v0:
        def __init__(self) -> None: ...

        @property
        def reflectivity(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec3f32: ...

        @reflectivity.setter
        def reflectivity(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec3f32, /) -> None: ...

        @property
        def name_string_table_id(self) -> int: ...

        @name_string_table_id.setter
        def name_string_table_id(self, arg: int, /) -> None: ...

        @property
        def width(self) -> int: ...

        @width.setter
        def width(self, arg: int, /) -> None: ...

        @property
        def height(self) -> int: ...

        @height.setter
        def height(self, arg: int, /) -> None: ...

        @property
        def view_width(self) -> int: ...

        @view_width.setter
        def view_width(self, arg: int, /) -> None: ...

        @property
        def view_height(self) -> int: ...

        @view_height.setter
        def view_height(self, arg: int, /) -> None: ...

    class Vertex_v0:
        def __init__(self) -> None: ...

        @property
        def position(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec3f32: ...

        @position.setter
        def position(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec3f32, /) -> None: ...

    class Node_v0:
        def __init__(self) -> None: ...

        @property
        def plane_num(self) -> int: ...

        @plane_num.setter
        def plane_num(self, arg: int, /) -> None: ...

        @property
        def children(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec2i32: ...

        @children.setter
        def children(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec2i32, /) -> None: ...

        @property
        def mins(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec3i16: ...

        @mins.setter
        def mins(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec3i16, /) -> None: ...

        @property
        def maxs(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec3i16: ...

        @maxs.setter
        def maxs(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec3i16, /) -> None: ...

        @property
        def first_face(self) -> int: ...

        @first_face.setter
        def first_face(self, arg: int, /) -> None: ...

        @property
        def num_faces(self) -> int: ...

        @num_faces.setter
        def num_faces(self, arg: int, /) -> None: ...

        @property
        def area(self) -> int: ...

        @area.setter
        def area(self, arg: int, /) -> None: ...

    class Node_v1:
        def __init__(self) -> None: ...

        @property
        def plane_num(self) -> int: ...

        @plane_num.setter
        def plane_num(self, arg: int, /) -> None: ...

        @property
        def children(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec2i32: ...

        @children.setter
        def children(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec2i32, /) -> None: ...

        @property
        def mins(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec3f32: ...

        @mins.setter
        def mins(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec3f32, /) -> None: ...

        @property
        def maxs(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec3f32: ...

        @maxs.setter
        def maxs(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec3f32, /) -> None: ...

        @property
        def first_face(self) -> int: ...

        @first_face.setter
        def first_face(self, arg: int, /) -> None: ...

        @property
        def num_faces(self) -> int: ...

        @num_faces.setter
        def num_faces(self, arg: int, /) -> None: ...

        @property
        def area(self) -> int: ...

        @area.setter
        def area(self, arg: int, /) -> None: ...

        @staticmethod
        def upgrade(old: BSP.Node_v0) -> BSP.Node_v1: ...

    class TextureInfo_v0:
        def __init__(self) -> None: ...

        @property
        def texture_vector1(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec4f32: ...

        @texture_vector1.setter
        def texture_vector1(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec4f32, /) -> None: ...

        @property
        def texture_vector2(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec4f32: ...

        @texture_vector2.setter
        def texture_vector2(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec4f32, /) -> None: ...

        @property
        def lightmap_vector1(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec4f32: ...

        @lightmap_vector1.setter
        def lightmap_vector1(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec4f32, /) -> None: ...

        @property
        def lightmap_vector2(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec4f32: ...

        @lightmap_vector2.setter
        def lightmap_vector2(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec4f32, /) -> None: ...

        @property
        def flags(self) -> int: ...

        @flags.setter
        def flags(self, arg: int, /) -> None: ...

        @property
        def texture_data(self) -> int: ...

        @texture_data.setter
        def texture_data(self, arg: int, /) -> None: ...

    class Face_v1:
        def __init__(self) -> None: ...

        @property
        def plane_num(self) -> int: ...

        @plane_num.setter
        def plane_num(self, arg: int, /) -> None: ...

        @property
        def side(self) -> int: ...

        @side.setter
        def side(self, arg: int, /) -> None: ...

        @property
        def on_node(self) -> int: ...

        @on_node.setter
        def on_node(self, arg: int, /) -> None: ...

        @property
        def first_edge(self) -> int: ...

        @first_edge.setter
        def first_edge(self, arg: int, /) -> None: ...

        @property
        def num_edges(self) -> int: ...

        @num_edges.setter
        def num_edges(self, arg: int, /) -> None: ...

        @property
        def tex_info(self) -> int: ...

        @tex_info.setter
        def tex_info(self, arg: int, /) -> None: ...

        @property
        def disp_info(self) -> int: ...

        @disp_info.setter
        def disp_info(self, arg: int, /) -> None: ...

        @property
        def surface_fog_volume_id(self) -> int: ...

        @surface_fog_volume_id.setter
        def surface_fog_volume_id(self, arg: int, /) -> None: ...

        @property
        def styles(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec4ui8: ...

        @styles.setter
        def styles(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec4ui8, /) -> None: ...

        @property
        def light_offset(self) -> int: ...

        @light_offset.setter
        def light_offset(self, arg: int, /) -> None: ...

        @property
        def area(self) -> float: ...

        @area.setter
        def area(self, arg: float, /) -> None: ...

        @property
        def lightmap_texture_mins_in_luxels(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec2i32: ...

        @lightmap_texture_mins_in_luxels.setter
        def lightmap_texture_mins_in_luxels(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec2i32, /) -> None: ...

        @property
        def lightmap_texture_size_in_luxels(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec2i32: ...

        @lightmap_texture_size_in_luxels.setter
        def lightmap_texture_size_in_luxels(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec2i32, /) -> None: ...

        @property
        def original_face(self) -> int: ...

        @original_face.setter
        def original_face(self, arg: int, /) -> None: ...

        @property
        def num_prims(self) -> int: ...

        @num_prims.setter
        def num_prims(self, arg: int, /) -> None: ...

        @property
        def first_prim_id(self) -> int: ...

        @first_prim_id.setter
        def first_prim_id(self, arg: int, /) -> None: ...

        @property
        def smoothing_groups(self) -> int: ...

        @smoothing_groups.setter
        def smoothing_groups(self, arg: int, /) -> None: ...

    class Face_v2:
        def __init__(self) -> None: ...

        @property
        def plane_num(self) -> int: ...

        @plane_num.setter
        def plane_num(self, arg: int, /) -> None: ...

        @property
        def side(self) -> int: ...

        @side.setter
        def side(self, arg: int, /) -> None: ...

        @property
        def on_node(self) -> int: ...

        @on_node.setter
        def on_node(self, arg: int, /) -> None: ...

        @property
        def first_edge(self) -> int: ...

        @first_edge.setter
        def first_edge(self, arg: int, /) -> None: ...

        @property
        def num_edges(self) -> int: ...

        @num_edges.setter
        def num_edges(self, arg: int, /) -> None: ...

        @property
        def tex_info(self) -> int: ...

        @tex_info.setter
        def tex_info(self, arg: int, /) -> None: ...

        @property
        def disp_info(self) -> int: ...

        @disp_info.setter
        def disp_info(self, arg: int, /) -> None: ...

        @property
        def surface_fog_volume_id(self) -> int: ...

        @surface_fog_volume_id.setter
        def surface_fog_volume_id(self, arg: int, /) -> None: ...

        @property
        def styles(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec4ui8: ...

        @styles.setter
        def styles(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec4ui8, /) -> None: ...

        @property
        def light_offset(self) -> int: ...

        @light_offset.setter
        def light_offset(self, arg: int, /) -> None: ...

        @property
        def area(self) -> float: ...

        @area.setter
        def area(self, arg: float, /) -> None: ...

        @property
        def lightmap_texture_mins_in_luxels(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec2i32: ...

        @lightmap_texture_mins_in_luxels.setter
        def lightmap_texture_mins_in_luxels(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec2i32, /) -> None: ...

        @property
        def lightmap_texture_size_in_luxels(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec2i32: ...

        @lightmap_texture_size_in_luxels.setter
        def lightmap_texture_size_in_luxels(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec2i32, /) -> None: ...

        @property
        def original_face(self) -> int: ...

        @original_face.setter
        def original_face(self, arg: int, /) -> None: ...

        @property
        def enable_shadows(self) -> bool: ...

        @enable_shadows.setter
        def enable_shadows(self, arg: bool, /) -> None: ...

        @property
        def num_prims(self) -> int: ...

        @num_prims.setter
        def num_prims(self, arg: bool, /) -> None: ...

        @property
        def first_prim_id(self) -> int: ...

        @first_prim_id.setter
        def first_prim_id(self, arg: int, /) -> None: ...

        @property
        def smoothing_groups(self) -> int: ...

        @smoothing_groups.setter
        def smoothing_groups(self, arg: int, /) -> None: ...

        @staticmethod
        def upgrade(arg: BSP.Face_v1, /) -> BSP.Face_v2: ...

    class Edge_v0:
        def __init__(self) -> None: ...

        @property
        def v0(self) -> int: ...

        @v0.setter
        def v0(self, arg: int, /) -> None: ...

        @property
        def v1(self) -> int: ...

        @v1.setter
        def v1(self, arg: int, /) -> None: ...

    class Edge_v1:
        def __init__(self) -> None: ...

        @property
        def v0(self) -> int: ...

        @v0.setter
        def v0(self, arg: int, /) -> None: ...

        @property
        def v1(self) -> int: ...

        @v1.setter
        def v1(self, arg: int, /) -> None: ...

        @staticmethod
        def upgrade(arg: BSP.Edge_v0, /) -> BSP.Edge_v1: ...

    class SurfEdge_v0:
        def __init__(self) -> None: ...

        @property
        def surf_edge(self) -> int: ...

        @surf_edge.setter
        def surf_edge(self, arg: int, /) -> None: ...

    class BrushModel_v0:
        def __init__(self) -> None: ...

        @property
        def min(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec3f32: ...

        @min.setter
        def min(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec3f32, /) -> None: ...

        @property
        def max(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec3f32: ...

        @max.setter
        def max(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec3f32, /) -> None: ...

        @property
        def origin(self) -> sourcepp._sourcepp_impl.sourcepp.math.Vec3f32: ...

        @origin.setter
        def origin(self, arg: sourcepp._sourcepp_impl.sourcepp.math.Vec3f32, /) -> None: ...

        @property
        def head_node(self) -> int: ...

        @head_node.setter
        def head_node(self, arg: int, /) -> None: ...

        @property
        def first_face(self) -> int: ...

        @first_face.setter
        def first_face(self, arg: int, /) -> None: ...

        @property
        def num_faces(self) -> int: ...

        @num_faces.setter
        def num_faces(self, arg: int, /) -> None: ...

    class GameLump:
        __init__: wrapper_descriptor = ...

        class Signature(enum.Enum):
            STATIC_PROPS = 1886548083

            DETAIL_PROPS = 1886548068

            DETAIL_PROP_LIGHTING_LDR = 1953263716

            DETAIL_PROP_LIGHTING_HDR = 1751937124

        @property
        def signature(self) -> BSP.GameLump.Signature: ...

        @signature.setter
        def signature(self, arg: BSP.GameLump.Signature, /) -> None: ...

        @property
        def is_compressed(self) -> int: ...

        @is_compressed.setter
        def is_compressed(self, arg: int, /) -> None: ...

        @property
        def version(self) -> int: ...

        @version.setter
        def version(self, arg: int, /) -> None: ...

        @property
        def offset(self) -> int: ...

        @offset.setter
        def offset(self, arg: int, /) -> None: ...

        @property
        def uncompressed_length(self) -> int: ...

        @uncompressed_length.setter
        def uncompressed_length(self, arg: int, /) -> None: ...

        @property
        def data(self) -> bytes: ...

        @data.setter
        def data(self, arg: bytes, /) -> None: ...

    class Lump(enum.Enum):
        UNKNOWN = -1

        ENTITIES = 0

        PLANES = 1

        TEXDATA = 2

        VERTEXES = 3

        VISIBILITY = 4

        NODES = 5

        TEXINFO = 6

        FACES = 7

        LIGHTING = 8

        OCCLUSION = 9

        LEAFS = 10

        FACEIDS = 11

        EDGES = 12

        SURFEDGES = 13

        MODELS = 14

        WORLDLIGHTS = 15

        LEAFFACES = 16

        LEAFBRUSHES = 17

        BRUSHES = 18

        BRUSHSIDES = 19

        AREAS = 20

        AREAPORTALS = 21

        S2004_PORTALS = 22

        UNUSED0 = 22

        SL4D2_PROPCOLLISION = 22

        S2004_CLUSTERS = 23

        UNUSED1 = 23

        SL4D2_PROPHULLS = 23

        S2004_PORTALVERTS = 24

        UNUSED2 = 24

        SL4D2_PROPHULLVERTS = 24

        S2004_CLUSTERPORTALS = 25

        UNUSED3 = 25

        SL4D2_PROPTRIS = 25

        DISPINFO = 26

        ORIGINALFACES = 27

        PHYSDISP = 28

        PHYSCOLLIDE = 29

        VERTNORMALS = 30

        VERTNORMALINDICES = 31

        S2004_DISP_LIGHTMAP_ALPHAS = 32

        UNUSED4 = 32

        DISP_VERTS = 33

        DISP_LIGHTMAP_SAMPLE_POSITIONS = 34

        GAME_LUMP = 35

        LEAFWATERDATA = 36

        PRIMITIVES = 37

        PRIMVERTS = 38

        PRIMINDICES = 39

        PAKFILE = 40

        CLIPPORTALVERTS = 41

        CUBEMAPS = 42

        TEXDATA_STRING_DATA = 43

        TEXDATA_STRING_TABLE = 44

        OVERLAYS = 45

        LEAFMINDISTTOWATER = 46

        FACE_MACRO_TEXTURE_INFO = 47

        DISP_TRIS = 48

        S2004_PHYSCOLLIDESURFACE = 49

        UNUSED5 = 49

        SL4D2_PROP_BLOB = 49

        WATEROVERLAYS = 50

        S2006_XBOX_LIGHTMAPPAGES = 51

        LEAF_AMBIENT_INDEX_HDR = 51

        S2006_XBOX_LIGHTMAPPAGEINFOS = 52

        LEAF_AMBIENT_INDEX = 52

        LIGHTING_HDR = 53

        WORLDLIGHTS_HDR = 54

        LEAF_AMBIENT_LIGHTING_HDR = 55

        LEAF_AMBIENT_LIGHTING = 56

        XBOX_XZIPPAKFILE = 57

        FACES_HDR = 58

        MAP_FLAGS = 59

        OVERLAY_FADES = 60

        L4D_OVERLAY_SYSTEM_LEVELS = 61

        UNUSED6 = 61

        L4D2_PHYSLEVEL = 62

        UNUSED7 = 62

        ASW_DISP_MULTIBLEND = 63

        UNUSED8 = 63

    def __bool__(self) -> bool: ...

    @staticmethod
    def create(path: str, version: int = 21, map_revision: int = 0) -> BSP: ...

    @property
    def version(self) -> int: ...

    @version.setter
    def version(self, arg: int, /) -> None: ...

    @property
    def map_revision(self) -> int: ...

    @map_revision.setter
    def map_revision(self, arg: int, /) -> None: ...

    @property
    def l4d2(self) -> bool: ...

    @l4d2.setter
    def l4d2(self, arg: bool, /) -> None: ...

    @property
    def console(self) -> bool: ...

    @console.setter
    def console(self, arg: bool, /) -> None: ...

    def has_lump(self, lump_index: BSP.Lump) -> bool: ...

    def is_lump_compressed(self, lump_index: BSP.Lump) -> bool: ...

    def get_lump_version(self, lump_index: BSP.Lump) -> int: ...

    def get_lump_data(self, lump_index: BSP.Lump, no_decompression: bool = False) -> object: ...

    def get_lump_data_for_entities(self) -> list[BSP.EntityKeyValues]: ...

    def get_lump_data_for_planes(self) -> list[BSP.Plane_v0]: ...

    def get_lump_data_for_texdata(self) -> list[BSP.TextureData_v0]: ...

    def get_lump_data_for_vertexes(self) -> list[BSP.Vertex_v0]: ...

    def get_lump_data_for_nodes(self) -> list[BSP.Node_v1]: ...

    def get_lump_data_for_texinfo(self) -> list[BSP.TextureInfo_v0]: ...

    def get_lump_data_for_faces(self) -> list[BSP.Face_v2]: ...

    def get_lump_data_for_edges(self) -> list[BSP.Edge_v1]: ...

    def get_lump_data_for_surfedges(self) -> list[BSP.SurfEdge_v0]: ...

    def get_lump_data_for_models(self) -> list[BSP.BrushModel_v0]: ...

    def get_lump_data_for_originalfaces(self) -> list[BSP.Face_v2]: ...

    def get_lump_data_for_game_lump(self) -> list[BSP.GameLump]: ...

    def set_lump(self, lump_index: BSP.Lump, version: int, data: bytes, compress_level: int = 0) -> None: ...

    def set_lump_for_entities(self, version: int, data: Sequence[BSP.EntityKeyValues], compress_level: int) -> None: ...

    def is_game_lump_compressed(self, signature: BSP.GameLump.Signature) -> bool: ...

    def get_game_lump_data(self, signature: BSP.GameLump.Signature) -> object: ...

    def set_game_lump(self, signature: BSP.GameLump.Signature, version: int, data: "std::span<std::byte const ,-1>", compress_level: int = 0) -> bool: ...

    def reset_lump(self, lump_index: BSP.Lump) -> None: ...

    def reset(self) -> None: ...

    def create_lump_patch_file(self, lump_index: BSP.Lump) -> None: ...

    def set_lump_from_patch_file(self, lump_file_path: str) -> bool: ...

    def bake(self, output_path: str = '') -> bool: ...

BSP_SIGNATURE: int = 1347633750

BSP_LUMP_COUNT: int = 64

BSP_LUMP_ORDER: list = ...

BSP_EXTENSION: str = '.bsp'

class PakLump(sourcepp._sourcepp_impl.vpkpp.PackFile):
    __init__: wrapper_descriptor = ...

    @staticmethod
    def open(path: str, callback: Callable[[str, sourcepp._sourcepp_impl.vpkpp.Entry], None] | None = None) -> sourcepp._sourcepp_impl.vpkpp.PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""
