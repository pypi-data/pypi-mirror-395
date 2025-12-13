from .detect import (
    detect_file,
    detect_buffer,
    detect_file_mime_and_charset,
    detect_buffer_mime_and_charset,
    FileCategory,
    FileSubtype,
    Kind,
)

# PROUD   - Bump when you are proud of the release.
# DEFAULT - Just normal/okay releases.
# SHAME   - Bump when fixing things too embarrassing to admit.
#       PROUD.DEFAULT.SHAME
#            \   |   /
__version__ = "1.0.0"
__version_info__ = tuple(int(i) for i in __version__.split('.'))
__all__ = [
    "detect_file",
    "detect_buffer",
    "detect_file_mime_and_charset",
    "detect_buffer_mime_and_charset",
    "FileCategory",
    "FileSubtype",
    "Kind",
]
