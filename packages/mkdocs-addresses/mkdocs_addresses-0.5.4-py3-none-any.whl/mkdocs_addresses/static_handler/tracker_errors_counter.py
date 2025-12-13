

from collections import defaultdict
from typing import Dict, List, Set

from mkdocs.structure.pages import Page
from mkdocs_addresses import path_manager

from mkdocs_addresses.static_handler.tracker_data_pages import PageDataTracker
from mkdocs_addresses.toolbox import plugin_dump_padder

from .types_aliases import PathCwd



JOINER = ' | '


class ContextExceptionsTracker(PageDataTracker):
    """ Keep track of the sources files (as uris) that are using references, like:

            ![alt](!!logo_svg)

        References can only be _used_ in pages, so the sources are the page.file.src_uri.
        Normally, n need for OSCwdPath thingy or so... BUT, to get a homogeneous behavior
        of the whole plugin, store the cwd rooted paths instead.
    """


    def archive_current(self, uni_docs_dir:PathCwd):
        """ Dump a deepcopy of the to internal structures: (id_to_sources, source_to_ids) """
        super().archive_current(uni_docs_dir)


    def add_exc(self, exc_name:str, ref:str, page:Page):
        key = f'{ exc_name }{ JOINER }{ ref }'
        self.add_id(page, key)


    def get_errors_info(self):
        """ Build an error message listing all the errors that are still registered
        """
        # rebuild data "per exception kind":
        dct = defaultdict(list)
        for k,files in self.id_to_sources.items():
            exc_name,ref = k.split(JOINER)
            for cwd_path in files:
                uri = path_manager.to_uri(cwd_path)
                dct[exc_name].append( (uri,ref) )

        sorted_items = sorted(dct.items(), key=lambda it: -len(it[1]))
        info_message = ''.join(
            self.__format_exc_and_info(exc_name, sorted(data)) for exc_name,data in sorted_items
        )
        return info_message


    @staticmethod
    def __format_exc_and_info(exc_name:str, lst_infos:List[str]):
        title = f'\n\033[31m{ PAD4 }{plugin_dump_padder(exc_name+":")} { len(lst_infos) } \033[0m'
        lines = "".join(f"\n{ PAD6 }{plugin_dump_padder(uri)} { ref }" for uri,ref in lst_infos)
        return title + lines



PAD4 = '    '
PAD6 = '      '
MIDDLE_MSG = "used in file"  # this is used in the tests to cut properly a line into the original information
