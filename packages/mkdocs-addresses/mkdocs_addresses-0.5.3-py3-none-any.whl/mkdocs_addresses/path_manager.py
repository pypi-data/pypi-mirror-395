"""
Group of cached functions, to not recompute again and again the very same paths conversions...
"""


# pylint: disable=all

import os
from pathlib import Path
from itertools import chain

from typing import TYPE_CHECKING, Union
from functools import lru_cache

from mkdocs_addresses.static_handler.types_aliases import PathCwd



if TYPE_CHECKING:
    from .addresses_plugin import AddressAddressesPlugin





@lru_cache(None)
def to_uri(path:Union[Path,str], *segments:str):
    """ Take a string, potentially os dependent path, and rebuild a slash separated
        version from it.
        If additional segments are given, they'll be considered new directories, up
        to a final segment that will be considered a file.

        Behavior for trailing separators on @path:
            - If @segments is not given, trailing separators on @path are kept (to
              keep behaviors consistent with "hidden" index.html files in the address).
            - If any @segments is given, trailing separators on @path are removed
              before joining @path and @segments.
    """
    if isinstance(path,str):
        path = Path(path)
    joined = "/".join(path.parts + segments)
    joined = joined.replace('\\','/')
        # Because windows path behave weirdly when given a "root-like" path, starting with a slash

    if joined.startswith('//'):      # may happen on absolute paths (linux)
        joined = '/' + joined.lstrip('/')
    return joined


@lru_cache(None)
def to_os(uri:str, *segments:str):
    """ Takes a path as string and converts it to an OS dependant version """
    return Path(uri, *segments)


#---------------------------------------------------------------------


@lru_cache(None)
def get_cwd_path_from_docs_dir_and_uri(uni_docs_dir:Path, src_uri:str) -> PathCwd:
    """ Specific to page_filename_arg_extractor... """
    return uni_docs_dir / src_uri
