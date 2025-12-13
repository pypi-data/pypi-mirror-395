

from typing import Any, Dict, Set



from mkdocs_addresses.exceptions import DuplicateIdentifierError
from mkdocs_addresses.static_handler.tracker_data_pages import PageDataTracker
from .types_aliases import Ref, PathCwd, SnipDescription, SourceRef







SRC_TO_IDS_TYPE = set




class References(PageDataTracker):
    """
    Keep track of each reference definition (headers, explicit ids, files, external links in a
    dedicated file):
        - identifier
        - associated source to point to when the identifier will be used
        - file location of the identifier (as "source uri")
          WARNING: the path is relative to the cwd.
        - code snippets associated to each identifier, if use_auto_completion is True
        - ensure that all identifiers (references or those used for the code snippets) are
          unique, otherwise raise DuplicateIdentifierError

    Note about the external links: they are stored only to build the code snippets/info file
    about the available references? Mkdocs actually already handles their transformation into
    proper urls.
    """

    id_to_data:  Dict[Ref,Any]
    """ Dict "identifier -> data" in the built site. Depending on what's registered:

        | Identifier | Data |
        |:-|:-|
        | A link/img ref<br>(`--link`/`!!img`) | Url page/file in the rendered website, relative to the docs_dir |
        | A file ref (`++file`) | Url of the file in the rendered website, relative to the docs_dir |
        | An external link ref (`BusService`) | the url of the link |
        | Description of a snippet | complete code, as string, of the item for the snippet |
    """

    snippets: Dict[SnipDescription,str]
    """ Dict "snippet description -> full snippet item code (as string)"
        The snippet description is the key used to identify a snippet in the final file.
    """

    _old_refs: Set[Ref]
    """ Registered references during the previous build """


    UNIQUE_SRC = True       # override


    def __init__(self, uni_docs_dir:PathCwd):
        super().__init__(uni_docs_dir)
        self.id_to_data = {}
        self.snippets   = {}
        self._old_refs  = set()



    #--------------------------------------------------------------
    # Snippets related logistic



    def add_snippet(self, src:SourceRef, identifier:str, snippet:str):
        here = self.format_source(src)
        if identifier in self.snippets:
            there = next(iter(self.id_to_sources[identifier]))
            raise DuplicateIdentifierError(
                f"{ identifier !r} is already used.\n"
                f"  - Attempt to add it to snippets\n"
                f"  - Adding from file { here }\n"
                f"  - Already registered with file {there}\n"
            )

        self.snippets[identifier] = snippet
        self.id_to_sources[identifier].add(here)
        self.source_to_ids[here].add(identifier)



    #--------------------------------------------------------------


    def add_id(
        self,
        source:SourceRef,
        identifier:str,
        data:Any,
        id_declared_as:str=None,
):
        """ Store the given data, associated to the given id, for the given page.
            Raise DuplicateIdentifierError if @id has already been used before.
            @source: uri if the source file. This will be converted to an OsCwdPath.
            @id_declared_as: original version of the identifier in the source file, if
                             different from id.
        """
        super().add_id(source, identifier, id_declared_as)
        self.id_to_data[identifier] = data


    def remove_source(self, source:SourceRef):
        src,ids = super().remove_source(source)
        for identifier in ids:
            self.id_to_data.pop(identifier, None)
            self.snippets.pop(identifier, None)
        return src, ids                         # just to respect the interface of the parent...
                                                # but never used (so far)

    # def remove_id(self, identifier:str):
    #     self.id_to_data.pop(identifier, None)
    #     self.snippets.pop(identifier, None)
    #     srcs = super().remove_id(identifier)
    #     return srcs                             # just to respect the interface of the parent...
    #                                             # but never used (so far)


    #---------------------------------


    def gen_refs_items(self):
        """ Return an iterator of items (and not just DictItems). """
        return iter(self.id_to_data.items())


    def get_ref_target_address(self, identifier:str):
        """ Return the data associated to an identifier """
        return self.id_to_data[identifier]


    #---------------------------------


    def archive_current(self, uni_docs_dir:PathCwd):
        super().archive_current(uni_docs_dir)
        self._old_refs = self.id_to_data.copy()



    def get_update_refs_definitions_info(self):
        """ Gather intel about all the references definitions, comparing the current state
            with the previous run of the plugin, and return:
                - a set of all the references that have been suppressed
                - a set of all the references that have been added

            This is mostly to give feedback to the user in the console.
        """
        fresh      = set(self.id_to_data)
        old        = set(self._old_refs)
        suppressed = old-fresh
        added      = fresh-old
        return (
            { ref: self._old_refs[ref]  for ref in suppressed },
            { ref: self.id_to_data[ref] for ref in added },
        )
