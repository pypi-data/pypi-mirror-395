
import os

from dataclasses import dataclass, field
from typing import Dict

from mkdocs_addresses import path_manager
from mkdocs_addresses.logger import logger

from .types_aliases import PathCwd, UriCwdPathStr







@dataclass
class FilesTracker:
    """ Somewhat "augmented" version of mkdocs.Files, tracking the source files and their date
        of last modification:
                - path (OS, relative to cwd) -> time
    """

    real_path_to_time: Dict[PathCwd,float] = field(default_factory=dict)


    def mark_file(self, source:PathCwd):
        self.real_path_to_time[source] = source.stat().st_mtime


    def is_file_up_to_date(self, source:PathCwd):
        """ Check if the source file has been updated since the last build.
            NOTES:
                - the file HAS to exist, here.
                - the path must be "os", and given relatively to the cwd
        """
        is_cached     = source in self.real_path_to_time
        cached_at     = is_cached and self.real_path_to_time[source]
        still_here    = is_cached and source.is_file()
        current       = still_here and source.stat().st_mtime
        is_up_to_date = is_cached and cached_at == current

        if not is_cached:
            logger.debug(f"Not cached yet: {source}")
        elif not is_up_to_date:
            logger.debug(f"File to update: {source}")

        return is_up_to_date


    def remove_as_cwd_uri(self, uri:UriCwdPathStr):
        """ Untrack a file, given its uri path (relative to cwd) """
        real = path_manager.to_os(uri)
        if real in self.real_path_to_time:
            del self.real_path_to_time[real]


    def remove_as_cwd_path(self, real:PathCwd):
        """ Untrack a file, given its OS path (relative to cwd) """
        if real in self.real_path_to_time:
            del self.real_path_to_time[real]


    def get_uris_and_paths(self):
        """ Returns a tuple fo pairs (CachePairPath) for all the tracked files,
            relative to the cwd.
        """
        return tuple(self.real_path_to_time)
