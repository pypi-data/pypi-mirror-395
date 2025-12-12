from collections.abc import Callable, Sequence
import enum
from typing import overload


class Attribute(enum.Enum):
    NONE = 0

    ARCHIVE_INDEX = 1

    LENGTH = 2

    CRC32 = 4

    PCK_MD5 = 8

    VPK_PRELOADED_DATA = 16

class Entry:
    __init__: wrapper_descriptor = ...

    @property
    def flags(self) -> int: ...

    @flags.setter
    def flags(self, arg: int, /) -> None: ...

    @property
    def archive_index(self) -> int: ...

    @archive_index.setter
    def archive_index(self, arg: int, /) -> None: ...

    @property
    def length(self) -> int: ...

    @length.setter
    def length(self, arg: int, /) -> None: ...

    @property
    def compressed_length(self) -> int: ...

    @compressed_length.setter
    def compressed_length(self, arg: int, /) -> None: ...

    @property
    def offset(self) -> int: ...

    @offset.setter
    def offset(self, arg: int, /) -> None: ...

    @property
    def extra_data(self) -> bytes: ...

    @extra_data.setter
    def extra_data(self, arg: bytes, /) -> None: ...

    @property
    def crc32(self) -> int: ...

    @crc32.setter
    def crc32(self, arg: int, /) -> None: ...

    @property
    def unbaked(self) -> bool: ...

    @unbaked.setter
    def unbaked(self, arg: bool, /) -> None: ...

class EntryCompressionType(enum.Enum):
    NO_OVERRIDE = -1

    NO_COMPRESS = 0

    DEFLATE = 8

    BZIP2 = 12

    LZMA = 14

    ZSTD = 93

    XZ = 95

class BakeOptions:
    def __init__(self) -> None: ...

    @property
    def zip_compression_type_override(self) -> EntryCompressionType: ...

    @zip_compression_type_override.setter
    def zip_compression_type_override(self, arg: EntryCompressionType, /) -> None: ...

    @property
    def zip_compression_strength(self) -> int: ...

    @zip_compression_strength.setter
    def zip_compression_strength(self, arg: int, /) -> None: ...

    @property
    def gma_write_crcs(self) -> bool: ...

    @gma_write_crcs.setter
    def gma_write_crcs(self, arg: bool, /) -> None: ...

    @property
    def vpk_generate_md5_entries(self) -> bool: ...

    @vpk_generate_md5_entries.setter
    def vpk_generate_md5_entries(self, arg: bool, /) -> None: ...

class EntryOptions:
    def __init__(self) -> None: ...

    @property
    def zip_compression_type(self) -> EntryCompressionType: ...

    @zip_compression_type.setter
    def zip_compression_type(self, arg: EntryCompressionType, /) -> None: ...

    @property
    def zip_compression_strength(self) -> int: ...

    @zip_compression_strength.setter
    def zip_compression_strength(self, arg: int, /) -> None: ...

    @property
    def vpk_preload_bytes(self) -> int: ...

    @vpk_preload_bytes.setter
    def vpk_preload_bytes(self, arg: int, /) -> None: ...

    @property
    def vpk_save_to_directory(self) -> bool: ...

    @vpk_save_to_directory.setter
    def vpk_save_to_directory(self, arg: bool, /) -> None: ...

EXECUTABLE_EXTENSION0: str = '.exe'

EXECUTABLE_EXTENSION1: str = '.bin'

EXECUTABLE_EXTENSION2: str = '.x86_64'

class PackFile:
    __init__: wrapper_descriptor = ...

    class OpenProperty(enum.Flag):
        DECRYPTION_KEY = 0

    @staticmethod
    def open(path: str, callback: Callable[[str, Entry], None] | None = None, request_callback: Callable[[PackFile, PackFile.OpenProperty], Sequence["std::byte"]] | None = None) -> PackFile: ...

    @staticmethod
    def get_openable_extensions() -> list[str]: ...

    @property
    def guid(self) -> str: ...

    @property
    def has_entry_checksums(self) -> bool: ...

    def verify_entry_checksums(self) -> list[str]: ...

    @property
    def has_pack_file_checksum(self) -> bool: ...

    def verify_pack_file_checksum(self) -> bool: ...

    @property
    def has_pack_file_signature(self) -> bool: ...

    def verify_pack_file_signature(self) -> bool: ...

    @property
    def is_case_sensitive(self) -> bool: ...

    def has_entry(self, path: str, include_unbaked: bool = True) -> bool: ...

    def __contains__(self, path: str) -> bool: ...

    def find_entry(self, path: str, include_unbaked: bool = True) -> Entry | None: ...

    def read_entry(self, path: str) -> bytes | None: ...

    def __getitem__(self, path: str) -> bytes | None: ...

    def read_entry_text(self, path: str) -> str | None: ...

    @property
    def is_read_only(self) -> bool: ...

    def add_entry_from_file(self, entry_path: str, filepath: str, options: EntryOptions = ...) -> None: ...

    def add_entry_from_mem(self, entry_path: str, buffer: bytes, options: EntryOptions = ...) -> None: ...

    @overload
    def add_directory(self, entry_base_dir: str, dir: str, options: EntryOptions = ...) -> None: ...

    @overload
    def add_directory(self, entry_base_dir: str, dir: str, creation: Callable[[str], EntryOptions]) -> None: ...

    def rename_entry(self, old_path: str, new_path: str) -> bool: ...

    def rename_directory(self, old_dir: str, new_dir: str) -> bool: ...

    def remove_entry(self, path: str) -> bool: ...

    def __delitem__(self, path: str) -> bool: ...

    def remove_directory(self, dir: str) -> int: ...

    def bake(self, output_dir: str = '', bake_options: BakeOptions = ..., callback: Callable[[str, Entry], None] | None = None) -> bool: ...

    def extract_entry(self, entry_path: str, filepath: str) -> bool: ...

    def extract_directory(self, dir: str, output_dir: str) -> bool: ...

    def extract_all(self, output_dir: str, create_under_pack_file_dir: bool = True) -> bool: ...

    def extract_all_if(self, output_dir: str, predicate: Callable[[str, Entry], bool], strip_shared_dirs: bool = True) -> bool: ...

    def get_entry_count(self, include_unbaked: bool = True) -> int: ...

    def run_for_all_entries(self, operation: Callable[[str, Entry], None], include_unbaked: bool = True) -> None: ...

    def run_for_all_entries_under(self, parent_dir: str, operation: Callable[[str, Entry], None], recursive: bool = True, include_unbaked: bool = True) -> None: ...

    @property
    def filepath(self) -> str: ...

    @property
    def truncated_filepath(self) -> str: ...

    @property
    def filename(self) -> str: ...

    @property
    def truncated_filename(self) -> str: ...

    @property
    def filestem(self) -> str: ...

    @property
    def truncated_filestem(self) -> str: ...

    @property
    def supported_entry_attributes(self) -> Attribute: ...

    def __str__(self) -> str: ...

    @staticmethod
    def escape_entry_path_for_write(arg: str, /) -> str: ...

class PackFileReadOnly(PackFile):
    __init__: wrapper_descriptor = ...

    @property
    def is_read_only(self) -> bool: ...

    def __str__(self) -> str: ...

FGP_SIGNATURE: int = 5261126

FGP_EXTENSION: str = '.grp'

FGP_HASHED_FILEPATH_PREFIX: str = '__hashed__/'

FGP_SOURCEPP_FILENAMES_SIGNATURE: int = 6003110640112455760

class FGP(PackFile):
    __init__: wrapper_descriptor = ...

    @staticmethod
    def create(path: str) -> PackFile: ...

    @staticmethod
    def open(path: str, callback: Callable[[str, Entry], None] | None = None) -> PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""

    @property
    def loading_screen_filepath(self) -> str: ...

    @loading_screen_filepath.setter
    def loading_screen_filepath(self, arg: str, /) -> None: ...

    @staticmethod
    def hash_filepath(arg: str, /) -> int: ...

FPX_SIGNATURE: int = 843185971

FPX_DIR_SUFFIX: str = '_fdr'

FPX_EXTENSION: str = '.fpx'

class VPK(PackFile):
    __init__: wrapper_descriptor = ...

    @staticmethod
    def create(path: str, version: int = 2) -> PackFile: ...

    @staticmethod
    def open(path: str, callback: Callable[[str, Entry], None] | None = None) -> PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""

    @staticmethod
    def generate_keypair_files(name: str) -> bool: ...

    def sign_from_file(self, filename: str) -> bool: ...

    def sign_from_mem(self, private_key: bytes, public_key: bytes) -> bool: ...

    @property
    def version(self) -> int: ...

    @version.setter
    def version(self, arg: int, /) -> None: ...

    @property
    def chunk_size(self) -> int: ...

    @chunk_size.setter
    def chunk_size(self, arg: int, /) -> None: ...

class FPX(VPK):
    __init__: wrapper_descriptor = ...

    @staticmethod
    def create(path: str) -> PackFile: ...

    @staticmethod
    def open(path: str, callback: Callable[[str, Entry], None] | None = None) -> PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""

GCF_EXTENSION: str = '.gcf'

class GCF(PackFileReadOnly):
    __init__: wrapper_descriptor = ...

    @staticmethod
    def open(path: str, callback: Callable[[str, Entry], None] | None = None, request_callback: Callable[[PackFile, PackFile.OpenProperty], Sequence["std::byte"]] | None = None) -> PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""

    @property
    def version(self) -> int: ...

    @property
    def appid(self) -> int: ...

    @property
    def appversion(self) -> int: ...

GMA_SIGNATURE: int = 1145130311

GMA_EXTENSION: str = '.gma'

class GMA(PackFile):
    __init__: wrapper_descriptor = ...

    @staticmethod
    def open(path: str, callback: Callable[[str, Entry], None] | None = None) -> PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""

HOG_SIGNATURE: str = 'DHF'

HOG_EXTENSION: str = '.hog'

class HOG(PackFileReadOnly):
    __init__: wrapper_descriptor = ...

    @staticmethod
    def open(path: str, callback: Callable[[str, Entry], None] | None = None) -> PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""

OL_SIGNATURE: str = 'Worldcraft Prefab Library\r\n\x1a'

OL_EXTENSION: str = '.ol'

class OL(PackFileReadOnly):
    __init__: wrapper_descriptor = ...

    @staticmethod
    def open(path: str, callback: Callable[[str, Entry], None] | None = None) -> PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""

    @property
    def notes(self) -> str: ...

    def get_entry_notes(self, path: str) -> str | None: ...

OO7_EXTENSION: str = '.007'

class OO7(PackFileReadOnly):
    __init__: wrapper_descriptor = ...

    @staticmethod
    def open(path: str, callback: Callable[[str, Entry], None] | None = None) -> PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""

ORE_EXTENSION: str = '.ore'

class ORE(PackFileReadOnly):
    __init__: wrapper_descriptor = ...

    @staticmethod
    def create(path: str) -> PackFile: ...

    @staticmethod
    def open(path: str, callback: Callable[[str, Entry], None] | None = None) -> PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""

PAK_FILENAME_MAX_SIZE: int = 56

PAK_SIGNATURE: int = 1262698832

PAK_SIN_FILENAME_MAX_SIZE: int = 120

PAK_SIN_SIGNATURE: int = 1262571603

PAK_HROT_FILENAME_MAX_SIZE: int = 120

PAK_HROT_SIGNATURE: int = 1414484552

PAK_EXTENSION: str = '.pak'

SIN_EXTENSION: str = '.sin'

class PAK(PackFile):
    __init__: wrapper_descriptor = ...

    class Type(enum.Enum):
        PAK = 0

        SIN = 1

        HROT = 2

    @staticmethod
    def create(path: str, type: PAK.Type = PAK.Type.PAK) -> PackFile: ...

    @staticmethod
    def open(path: str, type: Callable[[str, Entry], None] = PAK.Type.PAK) -> PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""

    @property
    def type(self) -> PAK.Type: ...

    @type.setter
    def type(self, arg: PAK.Type, /) -> None: ...

PCK_SIGNATURE: int = 1129333831

PCK_PATH_PREFIX: str = 'res://'

PCK_EXTENSION: str = '.pck'

class PCK(PackFile):
    __init__: wrapper_descriptor = ...

    @staticmethod
    def create(path: str, version: int = 2, godot_major_version: int = 0, godot_minor_version: int = 0, godot_patch_version: int = 0) -> PackFile: ...

    @staticmethod
    def open(path: str, callback: Callable[[str, Entry], None] | None = None) -> PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""

    @property
    def version(self) -> int: ...

    @version.setter
    def version(self, arg: int, /) -> None: ...

    def get_godot_version(self) -> tuple[int, int, int]: ...

    def set_godot_version(self, major: int = 0, minor: int = 0, patch: int = 0) -> None: ...

VPK_SIGNATURE: int = 1437209140

VPK_DIR_INDEX: int = 32767

VPK_ENTRY_TERM: int = 65535

VPK_DIR_SUFFIX: str = '_dir'

VPK_EXTENSION: str = '.vpk'

VPK_KEYPAIR_PUBLIC_KEY_TEMPLATE: str = ...

VPK_KEYPAIR_PRIVATE_KEY_TEMPLATE: str = ...

VPK_MAX_PRELOAD_BYTES: int = 1024

VPK_DEFAULT_CHUNK_SIZE: int = 209715200

VPK_VTMB_EXTENSION: str = '.vpk'

class VPK_VTMB(PackFile):
    __init__: wrapper_descriptor = ...

    @staticmethod
    def create(path: str) -> PackFile: ...

    @staticmethod
    def open(path: str, callback: Callable[[str, Entry], None] | None = None) -> PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""

VPP_SIGNATURE_LIL: int = 1367935694

VPP_SIGNATURE_BIG: int = 3456797009

VPP_ALIGNMENT: int = 2048

VPP_EXTENSION: str = '.vpp'

VPP_EXTENSION_PC: str = '.vpp_pc'

VPP_EXTENSION_XBOX2: str = '.vpp_xbox2'

class VPP(PackFileReadOnly):
    __init__: wrapper_descriptor = ...

    class Flags(enum.Flag):
        NONE = 0

        COMPRESSED = 1

        CONDENSED = 2

    @staticmethod
    def open(path: str, callback: Callable[[str, Entry], None] | None = None) -> PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""

WAD3_FILENAME_MAX_SIZE: int = 16

WAD3_SIGNATURE: int = 860111191

WAD3_EXTENSION: str = '.wad'

class WAD3(PackFile):
    __init__: wrapper_descriptor = ...

    @staticmethod
    def create(path: str) -> PackFile: ...

    @staticmethod
    def open(path: str, callback: Callable[[str, Entry], None] | None = None) -> PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""

XZP_HEADER_SIGNATURE: int = 2019191152

XZP_FOOTER_SIGNATURE: int = 1484408436

XZP_EXTENSION: str = '.xzp'

class XZP(PackFileReadOnly):
    __init__: wrapper_descriptor = ...

    @staticmethod
    def open(path: str, callback: Callable[[str, Entry], None] | None = None) -> PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""

BEE_EXTENSION: str = '.bee_pack'

BMZ_EXTENSION: str = '.bmz'

FPK_EXTENSION: str = '.fpk'

PK3_EXTENSION: str = '.pk3'

PK4_EXTENSION: str = '.pk4'

PKZ_EXTENSION: str = '.pkz'

ZIP_EXTENSION: str = '.zip'

class ZIP(PackFile):
    __init__: wrapper_descriptor = ...

    @staticmethod
    def create(path: str) -> PackFile: ...

    @staticmethod
    def open(path: str, callback: Callable[[str, Entry], None] | None = None) -> PackFile: ...

    GUID: str = ...
    """(arg: object, /) -> str"""

    def get_entry_compression_type(self, path: str) -> EntryCompressionType: ...

    def set_entry_compression_type(self, path: str, type: EntryCompressionType) -> None: ...

    def get_entry_compression_strength(self, path: str) -> int: ...

    def set_entry_compression_strength(self, path: str, type: int) -> None: ...
