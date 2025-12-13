

from typing import Dict, Iterable, Set

from mkdocs_addresses.static_handler.tracker_data_pages import PageDataTracker

from .types_aliases import PathCwd






class AddressesUsagePool(PageDataTracker):
    """ Keep track of the sources files (as uris) that are using references, like:

            ![alt](!!logo_svg)

        References can only be _used_ in pages, so the sources are the page.file.src_uri.
        No need for OSCwdPath thingy or so... BUT, to get a homogeneous behavior of the
        whole plugin, store the cwd rooted paths instead.
    """

    _old_id_to_sources: Dict[str,Set[PathCwd]]


    def __init__(self, uni_docs_dir:PathCwd):
        super().__init__(uni_docs_dir)
        self._old_id_to_sources = {}


    #---------------------------------


    def archive_current(self, uni_docs_dir:PathCwd):
        """ Dump a deepcopy of the to internal structures: (id_to_sources, source_to_ids) """
        super().archive_current(uni_docs_dir)
        self._old_id_to_sources = self.id_to_sources.copy()


    def get_missing_refs_infos(self, currently_defined_ids: Iterable[str]):
        """ Compare the archived data references the current ones, to find files that use outdated
            references, and returns a list of strings describing those.
            Needed because the references in pages that are "up to date" won't be checked during
            the on_page_context hook.
        """
        # DROPPED: for normal cases, this is causing double errors, once in page_context, and once
        #          in post_build => too much noise.
        #
        # # Merge old and new references used, in case some of the currently used aren't spotted
        # # as missing: this can happen with some plugins, like mkdocstrings-autoref, which is
        # # transforming the markdown of undefined external refs anyway. So this behavior acts like
        # # "security layer"
        # all_used = defaultdict(set)
        # for dct in (self._old_id_to_sources, self.id_to_sources):
        #     for identifier,sources in dct.items():
        #         all_used[identifier].update(sources)

        missings = set(self._old_id_to_sources) - set(currently_defined_ids)
        err_msgs = [
            f"\n    { ref !r} { MIDDLE_MSG } { src }"
                for ref in sorted(missings)
                for src in self._old_id_to_sources[ref]
        ]
        return err_msgs


MIDDLE_MSG = "used in file"  # this is used in the tests to cut properly a line into the original information
