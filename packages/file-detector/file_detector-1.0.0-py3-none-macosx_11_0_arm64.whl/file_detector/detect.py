import os
import sys
import ctypes
from ctypes import c_char_p, c_size_t, c_uint8, c_bool, c_uint16, Structure
from typing import NamedTuple
from enum import IntEnum

PathLike = str | bytes | os.PathLike[str]

# Resolve shared library name
if sys.platform.startswith("win"):
    _LIB_NAME = "_file_detect.dll"
elif sys.platform == "darwin":
    _LIB_NAME = "_file_detect.dylib"
else:
    _LIB_NAME = "_file_detect.so"

_DIR = os.path.dirname(__file__)

# Load the library beside this package or from current working dir
_lib_path = os.path.join(_DIR, _LIB_NAME)
_db_path = os.path.join(_DIR, "magic.mgc")

if not os.path.exists(_lib_path):
    # Fall back to letting the linker search path resolve it
    _lib_path = _LIB_NAME

_lib = ctypes.CDLL(_lib_path)

class _fd_kind_t(Structure):
    _fields_ = [("category", c_uint8),
                ("_align", c_uint8),
                ("subtype", c_uint16)]

# Prototypes
_lib.fd_detect_file_kind.argtypes = [c_char_p]
_lib.fd_detect_file_kind.restype = _fd_kind_t

_lib.fd_detect_buffer_kind.argtypes = [ctypes.c_void_p, c_size_t]
_lib.fd_detect_buffer_kind.restype = _fd_kind_t

_lib.fd_set_default_magic_db_path.argtypes = [c_char_p]
_lib.fd_set_default_magic_db_path.restype = None

_lib.fd_set_thread_local_magic_db_path.argtypes = [c_char_p]
_lib.fd_set_thread_local_magic_db_path.restype = None

_lib.fd_detect_file_mime.argtypes = [c_char_p]
_lib.fd_detect_file_mime.restype = c_char_p

_lib.fd_detect_buffer_mime.argtypes = [ctypes.c_void_p, c_size_t]
_lib.fd_detect_buffer_mime.restype = c_char_p

_lib.fd_set_debug_log_file.argtypes = [c_char_p]
_lib.fd_set_debug_log_file.restype = None

# the library should handle closing on thread shutdown
_lib.fd_close_for_thread.argtypes = []
_lib.fd_close_for_thread.restype = None


# Public API

class FileCategory(IntEnum):
    UNKNOWN    = 0
    TEXT       = 1
    DOCUMENT   = 2
    IMAGE      = 3
    ARCHIVE    = 4
    EXECUTABLE = 5
    DATABASE   = 6
    AUDIO      = 7
    VIDEO      = 8
    FONT       = 9
    MODEL_3D   = 10


class FileSubtype(IntEnum):
    GENERIC         = 0

    TXT_MARKDOWN    = 1
    TXT_HTML        = 2
    TXT_PYTHON      = 4
    TXT_C           = 5
    TXT_CPP         = 6
    TXT_JS          = 7
    TXT_TS          = 8
    TXT_SHELL       = 9
    TXT_JSON        = 10
    TXT_YAML        = 11
    TXT_TOML        = 12
    TXT_XML         = 13
    TXT_CSV         = 14
    TXT_PERL        = 38
    TXT_INI         = 45
    TXT_JAVA        = 46
    TXT_PO          = 50
    TXT_PEM         = 59
    TXT_SSH_KEY     = 60
    TXT_TROFF       = 62
    TXT_ALGOL       = 63
    TXT_RUBY        = 67
    TXT_TEX         = 68
    TXT_ASM         = 69
    TXT_FORTRAN     = 71
    TXT_OBJECTIVE_C = 72
    TXT_MAKEFILE    = 74
    TXT_DIFF        = 126
    TXT_HEX         = 127
    TXT_SSL_PRIV    = 128
    TXT_ICS         = 85
    TXT_MAGIC       = 145
    TXT_AFFIX       = 146
    TXT_SETUPSCRIPT = 147
    TXT_BAT         = 150
    TXT_CSS         = 151
    TXT_LUA         = 152
    TXT_PPL         = 153
    TXT_PHP         = 154
    TXT_GO          = 155
    TXT_SWIFT       = 156
    TXT_KOTLIN      = 157
    TXT_RUST        = 158
    TXT_SQL         = 159
    TXT_CONF        = 160
    TXT_J2          = 161
    TXT_LOG         = 162
    TXT_QSS         = 163
    TXT_VUE         = 164
    TXT_ENV         = 165
    TXT_PBXPROJ     = 166
    TXT_PLIST       = 167
    TXT_LUI         = 177
    TXT_CSHARP      = 178
    TXT_R           = 179  # R language
    TXT_SCALA       = 180  # Scala
    TXT_CLOJURE     = 181  # Clojure
    TXT_DART        = 182  # Dart
    TXT_ELM         = 183  # Elm
    TXT_ERLANG      = 184  # Erlang
    TXT_ELIXIR      = 185  # Elixir
    TXT_FSHARP      = 186  # F#
    TXT_HASKELL     = 187  # Haskell
    TXT_JULIA       = 188  # Julia
    TXT_OCAML       = 189  # OCaml
    TXT_NIM         = 190  # Nim
    TXT_PASCAL      = 191  # Pascal
    TXT_VB          = 192  # Visual Basic
    TXT_ZIG         = 193  # Zig
    TXT_D           = 194  # D language
    TXT_CRYSTAL     = 195  # Crystal
    TXT_V           = 196  # V language
    TXT_PROTO       = 197  # Protocol Buffers
    TXT_THRIFT      = 198  # Apache Thrift
    TXT_GRAPHQL     = 199  # GraphQL
    TXT_PRISMA      = 200  # Prisma schema
    TXT_TERRAFORM   = 201  # Terraform
    TXT_HCL         = 202  # HashiCorp Configuration Language
    TXT_GRADLE      = 203  # Gradle
    TXT_SBT         = 204  # SBT
    TXT_BAZEL       = 205  # Bazel
    TXT_NINJA       = 206  # Ninja
    TXT_MESON       = 207  # Meson
    TXT_GLSL        = 208  # GLSL shader
    TXT_HLSL        = 209  # HLSL shader
    TXT_METAL       = 210  # Metal shader
    TXT_WGSL        = 211  # WebGPU shader
    TXT_GDSCRIPT    = 212  # GDScript
    TXT_INK         = 213  # Ink narrative
    TXT_ODIN        = 243  # Odin programming language
    TXT_JAI         = 244  # Jai programming language
    TXT_PONY        = 245  # Pony programming language
    TXT_RED         = 246  # Red programming language
    TXT_REBOL       = 247  # Rebol programming language
    TXT_FACTOR      = 248  # Factor programming language
    TXT_FORTH       = 249  # Forth programming language
    TXT_LISP        = 250  # Lisp programming language
    TXT_SCHEME      = 251  # Scheme programming language
    TXT_RACKET      = 252  # Racket programming language
    TXT_PROLOG      = 253  # Prolog programming language
    TXT_CAPNP       = 254  # Cap'n Proto schema files
    TXT_FLATBUF     = 255  # FlatBuffers schema files
    TXT_NOMAD       = 256  # HashiCorp Nomad configuration
    TXT_CONSUL      = 257  # HashiCorp Consul configuration
    TXT_VAULT       = 258  # HashiCorp Vault configuration
    TXT_PACKER      = 259  # HashiCorp Packer configuration
    TXT_VAGRANT     = 260  # Vagrant configuration
    TXT_MILL        = 261  # Mill build tool
    TXT_BUCK        = 262  # Buck build system
    TXT_PANTS       = 263  # Pants build system
    TXT_WAF         = 264  # Waf build system
    TXT_SCONS       = 265  # SCons build system
    TXT_CARTFILE    = 266  # Carthage dependency file
    TXT_REQUIREMENTS = 267  # Requirements files
    TXT_CONSTRAINTS = 268  # Constraint files
    TXT_CG          = 272  # Cg shader language
    TXT_TSCN        = 273  # Godot scene files
    TXT_TRES        = 274  # Godot resource files
    TXT_BOO         = 275  # Boo programming language
    TXT_MONKEY      = 276  # Monkey programming language
    TXT_BMX         = 277  # BlitzMax programming language
    TXT_BB          = 278  # BlitzBasic programming language
    TXT_AGS         = 279  # Adventure Game Studio scripts
    TXT_TWINE       = 280  # Twine interactive fiction
    TXT_YARN        = 281  # Yarn Spinner dialogue system
    TXT_STORY       = 282  # Story files
    TXT_NARRATIVE   = 283  # Narrative files
    TXT_SCRIPT      = 284  # Script files
    TXT_SCENARIO    = 285  # Scenario files
    TXT_QC          = 289  # Source engine QC files
    TXT_VMT         = 290  # Source engine material files

    DOC_PDF         = 15
    DOC_EPUB        = 61
    DOC_CHM         = 66
    DOC_XLSX        = 76
    DOC_ODT         = 77
    DOC_ODS         = 78
    DOC_ODP         = 79
    DOC_DOC         = 80
    DOC_PPT         = 81
    DOC_XLS         = 82
    DOC_PS          = 84
    DOC_VCF         = 86
    DOC_HWP         = 133
    DOC_HWPX        = 134
    DOC_SXC         = 142
    DOC_SXD         = 143
    DOC_RTF         = 149
    DOC_OLE         = 41
    DOC_CDF         = 44
    DOC_MBOX        = 64
    DOC_LNK         = 104
    DOC_TEXI        = 269  # Texinfo documentation
    DOC_INFO        = 270  # Info documentation
    DOC_HELP        = 271  # Help files

    IMG_PNG         = 16
    IMG_JPEG        = 17
    IMG_GIF         = 18
    IMG_BMP         = 19
    IMG_WEBP        = 20
    IMG_TIFF        = 21
    IMG_ACO         = 47
    IMG_ICO         = 52
    IMG_ANI         = 55
    IMG_PCX         = 58
    IMG_DJVU        = 87
    IMG_ICNS        = 88
    IMG_PSD         = 89
    IMG_PBM         = 90  # Netpbm
    IMG_PGM         = 91  # Netpbm
    IMG_GODOT_STEX  = 131
    IMG_TGA         = 138
    IMG_TIM         = 139
    IMG_ATARI_DEGAS = 140
    IMG_AWARD_BIOS  = 141
    IMG_AVIF        = 168
    IMG_SVG         = 3
    IMG_FITS        = 70
    IMG_VTF         = 241  # Source texture

    AR_ZIP          = 22
    AR_TAR          = 23
    AR_GZIP         = 24
    AR_BZIP2        = 25
    AR_XZ           = 26
    AR_7Z           = 27
    AR_RAR          = 28
    AR_ZLIB         = 39
    AR_COMPRESS     = 48
    AR_CAB          = 92
    AR_RPM          = 93
    AR_DEB          = 94
    AR_ZSTD         = 95
    AR_ARJ          = 96
    AR_DMG          = 97
    AR_APK          = 98
    AR_AR           = 99  # Unix ar (.a)
    AR_SZDD         = 100 # InstallShield SZDD
    AR_GPKG         = 132
    AR_KEYMAN_KMP   = 136
    AR_JAR          = 36
    AR_PAK          = 220  # Package files
    AR_WAD          = 221  # WAD files
    AR_VPK          = 222  # VPK files

    EXE_ELF         = 29
    EXE_PE          = 30
    EXE_MACHO       = 31
    EXE_OBJ         = 42
    EXE_COFF        = 43
    EXE_MSI         = 101
    EXE_MST         = 129
    EXE_WASM        = 34
    EXE_JAVA_CLASS  = 35
    EXE_PYTHON_BYTECODE = 37
    EXE_SPIRV       = 242  # SPIR-V binary

    DB_SQLITE       = 32
    DB_PCAP         = 33
    DB_GIT          = 40
    DB_SIMH         = 49
    DB_MO           = 51
    DB_MAT          = 56
    DB_NETCDF       = 57
    DB_NPY          = 65
    DB_MS_PDB       = 73
    DB_DBF          = 102
    DB_DBASE_NDX    = 103
    DB_TORRENT      = 105
    DB_PNF          = 130
    DB_KEYMAN_KMX   = 135
    DB_MAGIC_MGC    = 144
    DB_PGP_KEYS     = 148
    DB_BSON         = 214  # Binary JSON
    DB_MSGPACK      = 215  # MessagePack
    DB_CBOR         = 216  # CBOR
    DB_AVRO         = 217  # Apache Avro
    DB_PARQUET      = 218  # Apache Parquet
    DB_ORC          = 219  # Apache ORC
    DB_SAVE         = 286  # Game save files
    DB_DAT          = 287  # Data files
    DB_BSP          = 288  # BSP (Binary Space Partitioning) files
    DB_PKL          = 308  # Python pickle files
    DB_H5           = 309  # HDF5 files
    DB_ONNX         = 310  # ONNX model files
    DB_PB           = 311  # Protocol Buffer binary files
    DB_CKPT         = 312  # Checkpoint files
    DB_SAFETENSORS  = 313  # SafeTensors files

    AUD_WAV         = 110
    AUD_MP3         = 111
    AUD_OGG         = 112
    AUD_AIFF        = 113
    AUD_AU          = 114
    AUD_AAC_LATM    = 115
    AUD_DFF         = 116
    AUD_DSF         = 117
    AUD_AMR         = 137
    AUD_M4A         = 170
    AUD_FLAC        = 171
    AUD_WMA         = 172
    AUD_F4A         = 240  # F4A audio
    AUD_F4B         = 307  # F4B audio format

    VID_AVI         = 118
    VID_MP4         = 119
    VID_WEBM        = 120
    VID_MKV         = 121
    VID_FLV         = 122
    VID_MOV         = 123
    VID_MPEG_TS     = 124
    VID_SWF         = 125
    VID_WMV         = 173
    VID_M4V         = 174
    VID_H264        = 175
    VID_BINK        = 230  # Bink video
    VID_SMACKER     = 231  # Smacker video
    VID_THEORA      = 232  # Theora video
    VID_OGV         = 233  # Ogg video
    VID_3GP         = 234  # 3GP video
    VID_ASF         = 235  # ASF video
    VID_RM          = 236  # RealMedia
    VID_VOB         = 237  # VOB video
    VID_M2TS        = 238  # M2TS video
    VID_F4V         = 239  # F4V video
    VID_ROQ         = 304  # ROQ video format
    VID_3G2         = 305  # 3G2 video format
    VID_F4P         = 306  # F4P video format

    FONT_EOT        = 53
    FONT_OTF        = 54
    FONT_TEX_TFM    = 75
    FONT_WOFF       = 107
    FONT_WOFF2      = 108
    FONT_SFNT       = 109
    FONT_TTF        = 169

    M3D_GLB         = 176
    M3D_BLEND       = 106
    M3D_FBX         = 223  # FBX model
    M3D_DAE         = 224  # COLLADA
    M3D_X3D         = 225  # X3D
    M3D_PLY         = 226  # PLY
    M3D_STL         = 227  # STL
    M3D_3DS         = 228  # 3DS
    M3D_OBJ         = 229  # Wavefront OBJ
    M3D_MDL         = 291  # Model files
    M3D_MESH        = 292  # Mesh files
    M3D_SKELETON    = 293  # Skeleton files
    M3D_ANIMATION   = 294  # Animation files
    M3D_MAX         = 295  # 3ds Max files
    M3D_MA          = 296  # Maya ASCII files
    M3D_MB          = 297  # Maya Binary files
    M3D_C4D         = 298  # Cinema 4D files
    M3D_LWO         = 299  # LightWave Object files
    M3D_LWS         = 300  # LightWave Scene files
    M3D_XSI         = 301  # Softimage files
    M3D_HRC         = 302  # Hierarchy files
    M3D_SMD         = 303  # Source model files

    COUNT           = 314

    # Add any others if missed


class Kind(NamedTuple):
    category: FileCategory
    subtype: FileSubtype


def detect_file(path: PathLike) -> Kind:
    """
    Detect file kind by path. Returns (category, subtype).
    """
    p = os.fsencode(path)
    res = _lib.fd_detect_file_kind(p)

    try:
        cat_e = FileCategory(int(res.category))
    except ValueError:
        cat_e = FileCategory.UNKNOWN

    try:
        sub_e = FileSubtype(int(res.subtype))
    except ValueError:
        sub_e = FileSubtype.GENERIC

    return Kind(cat_e, sub_e)


def bytes_like_to_memory(bytes_like: bytes | bytearray | memoryview) -> tuple[...]:  # what is the type?
    mv = memoryview(bytes_like)

    # Ensure 1-D C-contiguous
    if mv.ndim != 1 or not mv.c_contiguous:
        mv = memoryview(mv.tobytes())  # copy to contiguous

    n = mv.nbytes
    if mv.readonly:
        baff = (ctypes.c_char * n).from_buffer_copy(mv) # copy
        keepalive = baff
    else:
        baff = (ctypes.c_char * n).from_buffer(mv) # zero-copy
        keepalive = (mv, baff)

    ptr = ctypes.c_void_p(ctypes.addressof(baff))
    return ptr, c_size_t(n), keepalive


def detect_buffer(bytes_like: bytes | bytearray | memoryview) -> Kind:
    """
    Detect buffer kind. Returns (category, subtype).
    """
    ptr, size, _keepalive = bytes_like_to_memory(bytes_like)
    res = _lib.fd_detect_buffer_kind(ptr, size)

    try:
        cat_e = FileCategory(int(res.category))
    except ValueError:
        cat_e = FileCategory.UNKNOWN

    try:
        sub_e = FileSubtype(int(res.subtype))
    except ValueError:
        sub_e = FileSubtype.GENERIC

    return Kind(cat_e, sub_e)


class Mime_Charset(NamedTuple):
    mime: str
    charset: str


def detect_file_mime_and_charset(path: PathLike) -> Mime_Charset:
    p = os.fsencode(path)
    res = _lib.fd_detect_file_mime(p)
    if not res:
        return Mime_Charset("", "")
    mime, _, charset = res.decode('utf-8', errors='replace').partition("; charset=")
    return Mime_Charset(mime, charset)


def detect_buffer_mime_and_charset(bytes_like: bytes | bytearray | memoryview) -> Mime_Charset:
    ptr, size, _keepalive = bytes_like_to_memory(bytes_like)
    res = _lib.fd_detect_buffer_mime(ptr, size)
    if not res:
        return Mime_Charset("", "")
    mime, _, charset = res.decode('utf-8', errors='replace').partition("; charset=")
    return Mime_Charset(mime, charset)


# Advanced API for thread-specific magic database paths

def set_default_magic_db_path(path: PathLike) -> None:
    """
    Set the default magic database path that new threads will inherit.
    This affects all future threads that don't have their own path set.
    """
    _lib.fd_set_default_magic_db_path(os.fsencode(path))


def set_thread_local_magic_db_path(path: PathLike) -> None:
    """
    Set a custom magic database path for the current thread only.
    Pass None to clear the thread-specific path and use the default.
    """
    _lib.fd_set_thread_local_magic_db_path(os.fsencode(path))


# Set the magic database path once at module import time
# The C library will now handle thread-local storage automatically
set_default_magic_db_path(_db_path)
