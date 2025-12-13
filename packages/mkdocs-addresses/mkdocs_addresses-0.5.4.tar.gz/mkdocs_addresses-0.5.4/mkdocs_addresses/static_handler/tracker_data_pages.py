
import json
from pathlib import Path

from typing import TYPE_CHECKING, Dict, Iterable, Set
from collections import defaultdict
from abc import ABCMeta

from mkdocs_addresses.exceptions import DuplicateIdentifierError

from .types_aliases import SourceRef, PathCwd


if TYPE_CHECKING:
    from mkdocs_addresses.addresses_plugin import AddressAddressesPlugin



class PageDataTracker(metaclass=ABCMeta):
    """ Abstract class providing the general logic for data structures that are tracking
        information contained in some docs pages.

        Only holds the general behaviors, assuming the subclass will always have  at least
        those two data structures:

            id_to_sources: Dict[str,Set[str]]
            source_to_ids: Dict[PathCwd,Set[str]]
    """
    UNIQUE_SRC: bool = False        # can be registered once only

    _uni_docs_dir: PathCwd

    id_to_sources: Dict[str,Set[PathCwd]]
    source_to_ids: Dict[PathCwd,Set[str]]


    def __init__(self, uni_docs_dir:Path):
        self._uni_docs_dir = uni_docs_dir
        self.id_to_sources = defaultdict(set)
        self.source_to_ids = defaultdict(set)


    def __str__(self):
        rep_s = ''.join(
            f"  { prop }: { json.dumps({id: list(vs) for id,vs in getattr(self,prop)}, indent=4) }"
            for prop in ('id_to_sources', "source_to_ids")
        )
        return f"{ self.__class__.__name__ }({ rep_s })"


    def __bool__(self):
        return bool(self.id_to_sources)



    #------------------------------------------------------


    def format_source(self, source:SourceRef) -> PathCwd:
        """ Converts the given source information into a Path rooted at cwd.
            If the input is not a mkdocs Page, assume it's already given appropriately rooted.
        """
        # Does NOT check against Page class because of the fake Pages used in the tests.
        src = (
               source if isinstance(source,Path) else
               Path(source) if isinstance(source,str) else
               self._uni_docs_dir / source.file.src_uri
        )
        return src


    #------------------------------------------------------


    def add_id(
        self,
        source:         SourceRef,
        identifier:     str,
        id_declared_as: str = None
):
        """ Store the given data, associated to the given id, for the given page.
            Raise DuplicateIdentifierError if @id has already been used before while
            self.UNIQUE is True.
            Returns the source (as PathCwd) so that a child class can store more additional
            logic if needed.
        """
        cwd_path   = self.format_source(source)
        known_srcs = self.id_to_sources[identifier]

        if self.UNIQUE_SRC and known_srcs:
            there = next(iter(known_srcs))
            info  = "" if id_declared_as is None else f"(found written as \033[31m{ id_declared_as !r}\033[34m)"
            raise DuplicateIdentifierError(
                f"{ identifier !r} is already used.\n"
                f"  - Attempt to add it to references\n"        # this line is used in the tests: do not modify
                f"  - Adding from file { cwd_path }{ info }\n"
                f"  - Already registered with file \033[35m{there}\033[34m\n"
            )

        known_srcs.add(cwd_path)
        self.source_to_ids[cwd_path].add(identifier)

        return cwd_path



    def remove_source(self, source:SourceRef):
        """ Remove all the informations related to the given page from the data structure.
            Does nothing if the page isn't registered.
            Returns the PathCwd involved, as well as the corresponding ids to the caller.
        """
        src = self.format_source(source)
        ids: Iterable[str] = self.source_to_ids.pop(src, ())
        for identifier in ids:
            sources_pool = self.id_to_sources[identifier]
            sources_pool.discard(src)
            if not sources_pool:
                del self.id_to_sources[identifier]

        return src, ids



    # def remove_id(self, identifier:str):
    #     """ Remove all the informations related to the given identifier from the data structure.
    #         Does nothing if the reference isn't registered.
    #         Returns the sources where the identifier was found.
    #     """
    #     sources: Iterable[str] = self.id_to_sources.pop(identifier, ())
    #     for source in sources:
    #         ids_pool = self.source_to_ids[source]
    #         ids_pool.discard(identifier)
    #         if not ids_pool:
    #             del self.source_to_ids[source]
    #     return sources


    #------------------------------------------------------


    def has_id(self, identifier:str):
        return identifier in self.id_to_sources

    def has_source(self, source:SourceRef):
        src = self.format_source(source)
        return src in self.source_to_ids

    def is_identifier_in_source(self, identifier:str, source:SourceRef):
        """ Tells if the given identifier has been/is still declared in the given source """
        cwd_src = self.format_source(source)
        return identifier in self.source_to_ids[cwd_src]





    # def get_sources_with_id(self, identifier:str):
    #     """ Extract all filenames using the given @identifier """
    #     return self.id_to_sources[identifier]

    # def get_ids_in_source(self, source:SourceRef):
    #     """ Extract all identifiers used the given @page (Page or filename) """
    #     src = self.format_source(source)
    #     return self.source_to_ids[src]


    #---------------------------------


    def archive_current(self, uni_docs_dir:PathCwd):
        """ Only takes care of the uni_docs_dir logistic part. Actual archiving must be done
            by the child class.
        """
        self._uni_docs_dir = uni_docs_dir
