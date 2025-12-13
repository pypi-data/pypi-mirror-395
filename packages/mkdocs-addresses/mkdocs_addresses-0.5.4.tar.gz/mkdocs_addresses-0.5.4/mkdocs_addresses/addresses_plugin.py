import json
import re

from typing import List, Literal, Set, NamedTuple, Type, Union
from collections import Counter
from pathlib import Path

from bs4.element import Tag

from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files, File
from mkdocs.structure.nav import Navigation

from mkdocs.plugins import BasePlugin, event_priority
from mkdocs.config.defaults import MkDocsConfig
from mkdocs_addresses import path_manager
from mkdocs_addresses.other_plugins_handling.autorefs import (
    gen_invalid_external_links_when_autorefs_used,
)

from mkdocs_addresses.soup_excluding_codes import PluginSoupExcludingCodes
from mkdocs_addresses.static_handler.types_aliases import PathCwd, SourceRef, UriCwdPathStr, UriDocsPathStr


from .exceptions import (
    AddresserConfigError,
    DumpOnlyException,
    InvalidIdentifierError,
    LeadingSlashAddressError,
    NonAbsoluteAddressError,
    OutdatedReferenceError,
    UnknownExternalLinkIdentifierError,
    UnknownIdentifierError,
)
from .auto_completion_handler import (
    RefKind,
    AutoCompletion,
    IdeKind,
    PLUGIN_MARK,
)
from .config_plugin import (
    AddressAddressesConfig,
    ConfigDescriptor,
    NO_DUMP,
    DUMP_ONLY,
)
from .static_handler import StaticHandler
from .toolbox import (
    extract_external_links_refs_in_md,
    plugin_dump_padder,
    fatal_if
)
from .addresses_checker import AddressChecker, AddressKind
from .logger import LogMessages, logger, addresses_auto_log_plugin_on





#from ._test_data_extraction import LiveDataExtractor               ##>
#extractor = LiveDataExtractor()
#logger.error('Creating global LiveDataExtractor object')           ##<





class SoupTag(NamedTuple):
    """ helper... """
    tag: Tag
    attr: str
    kind: RefKind
    identifier: str








#-----------------------------------------------------------------------------
# Functions used for decorated methods (StaticHandler/cache related logistic):
#
# These functions are here to entirely decorelate the cache logic from the
# actual signatures of the plugin methods.
#-----------------------------------------------------------------------------



def plugin_file_prop_extractor(prop:str):
    """ Generate a getter extracting the path file for the given property """
    def getter(self:'AddressAddressesPlugin', *_, **__) -> PathCwd:
        """ Extract a filename from a plugin property.
            WARNING: those are relative to cwd, not to docs_dir!
        """
        file: PathCwd = getattr(self, prop)
        return file
    return getter


def cwd_path_arg_extractor_page_hook(
    plugin:'AddressAddressesPlugin',
    *_,
    page:Page,
    **_kw
) -> PathCwd:
    """ Extract the PathCwd of the page argument from a page related plugin event """
    return path_manager.get_cwd_path_from_docs_dir_and_uri(plugin.uni_docs_dir, page.file.src_uri)


def page_arg_extractor_page_hooks(_plugin, *_args, page:Page, **_kw) -> Page:
    """ Extract the page argument for the StaticHandler """
    return page


def cwd_path_arg_extractor_other_files(_plugin, path:PathCwd, _file:File) -> PathCwd:
    """ Extract the PathCwd argument for the StaticHandler """
    return path


def cwd_path_arg_extractor_inclusions(_plugin, file:str, _inclusion_path:str) -> PathCwd:
    """ Extract the PathCwd to the inclusions file from the arguments, for the StaticHandler """
    return path_manager.to_os(file)


#----------------------------------------


def never_skip(*_,**__):
    return False

def skip_if_no_autocompletion_or_no_snippets_file_or_wrong_extension(plugin:'AddressAddressesPlugin', *_, **__) -> bool:
    no_autocomp = not plugin.use_auto_completion
    no_file     = not plugin.dump_snippets_file.is_file()
    wrong_ext   = no_file or plugin.dump_snippets_file.suffix == '.txt'
    return no_autocomp or wrong_ext

def skip_if_no_external_links(plugin:'AddressAddressesPlugin', *_, **__) -> bool:
    return not plugin.external_links_file

def on_page_context_skip(plugin:'AddressAddressesPlugin', _ctx, *, page:Page, **__) -> bool:
    """ Check special reasons to not apply the on_page_context event """
    return plugin.dump_action == DUMP_ONLY or page.url in plugin.ignored_identifiers_or_addresses

def skip_if_file_already_registered(plugin:'AddressAddressesPlugin', cwd_path:PathCwd, _:File) -> bool:
    return plugin.global_handler.references.has_source(cwd_path)


#-------------------------------------------------------------------------------









class AddressAddressesPlugin(BasePlugin[AddressAddressesConfig]):

    activate_cache: bool = ConfigDescriptor()                              # type: ignore

    black_list_pattern: re.Pattern = ConfigDescriptor()                    # type: ignore
    """ Same as ignored_identifiers_or_addresses, but using a regex pattern. """

    docs_dir: str = ConfigDescriptor()                                     # type: ignore
    """ uri segment, from cwd to the directory containing the documentation files """

    dump_action: str = ConfigDescriptor()                                  # type: ignore
    """ 'normal', 'none', 'only' """

    dump_snippets_file: PathCwd = ConfigDescriptor()                       # type: ignore
    """ Relative to cwd """

    external_links_file: Union[PathCwd, Literal[""]] = ConfigDescriptor()  # type: ignore
    """ Relative to cwd """

    fail_fast: bool = ConfigDescriptor()                                   # type: ignore
    """ If false, information about the exceptions raised by the plugin are logged to the console
        but are caught, to let the executions go.
    """

    ide: IdeKind = ConfigDescriptor()                                      # type: ignore
    """ Ide to use for autocompletion """

    imgs_extension_pattern: re.Pattern = ConfigDescriptor()                # type: ignore
    """ Regex pattern used to decide what should be considered a file or an image.
        This will decide the prefix used ('!!' for images and '++' for files)
    """

    ignore_auto_headers: bool = ConfigDescriptor()                         # type: ignore
    """ If true, the plugin will try to spot headers without specific id attribute and won't
        generate identifier for them (this allow to have the same title in different places
        without raising a DuplicateIdentifierError).
    """

    ignored_classes: Set[str] = ConfigDescriptor()                         # type: ignore
    """ When gathering references in the html code, tags holding one of these classes
        will be ignored
    """

    skip_identifiers_definitions_in_pages : Set[str] = ConfigDescriptor()   # type: ignore
    """ When gathering references, these pages are skipped.
    """

    ignored_identifiers_or_addresses: Set[str] = ConfigDescriptor()        # type: ignore
    """ When gathering tags in html code, tags holding an id, a href or a src attribute present
        in this set will be ignored.
    """

    inclusions: List[PathCwd] = ConfigDescriptor()                         # type: ignore
    """ Relative to the cwd. List of the directories containing files that can be included
        using --8<-- in the docs.
    """

    # inclusions_with_root: bool = ConfigDescriptor()
    # """ Include or not the inclusion root directory in the snippet suggestion """

    more_verbose: bool = ConfigDescriptor()                                # type: ignore
    """ If true, the plugin will log more thing at INFO level. This allow to get more feedback
        without using "mkdocs serve -v', which will literally get the console  swarmed.
    """

    plugin_off: bool = ConfigDescriptor()                                  # type: ignore
    """ Bypass all behaviors if True """

    uni_docs_dir: PathCwd = ConfigDescriptor()                             # type: ignore
    """ Relative to cwd """

    use_directory_urls: bool = ConfigDescriptor()                          # type: ignore
    """ keep track of the config value """

    strict_anchor_check: bool = ConfigDescriptor()                         # type: ignore

    verify_only: Set[UriDocsPathStr] = ConfigDescriptor()                  # type: ignore
    """ Set of files to verify during on_page_context. If empty, all (updated) files are checked,
        otherwise, only the files listed here are checked (if they have been updated, when the
        cache is activated).
    """




    # Plugin specific:
    is_dirty: bool
    global_handler: StaticHandler
    completion: Type[AutoCompletion]

    @property
    def use_auto_completion(self) -> bool:
        return self.ide != 'none'


    def __str__(self):
        props_to_show = set(self.__class__.__annotations__.keys()) \
                      - {'global_handler', 'completion'}
        plugin = {
            prop: (
                ['...'] if prop=='global_handler' else
                list(val) if isinstance((val:=getattr(self,prop,None)),set) else
                [str(p) for p in val] if prop=='inclusions' else
                val.pattern if isinstance(val, re.Pattern) else
                str(val) if isinstance(val, Path) else
                val
            )
            for prop in sorted(props_to_show)
        }
        if hasattr(self, 'global_handler'):
            plugin.update({
                "references": dict(self.global_handler.references.id_to_data),
            })
        return f'{ self.__class__.__name__ }:\n{ json.dumps(plugin, indent=4) }'


    def is_to_skip(self, some:str) -> bool:
        """
        Return True of the given input matches some of the exclusion rules :
            - black_list_pattern
            - ignored_identifiers_or_addresses
        """
        return some in self.ignored_identifiers_or_addresses or bool(self.black_list_pattern.match(some))


    def uncache_file_at(self, cwd_uri:UriCwdPathStr):
        """
        Allow to remove a file from the global cache, to ensure it will be rendered again.
        This is to be called by external plugins when needed.
        """
        logger.warning(
            "AddressAddressesPlugin.uncache_file_at(...) is deprecated. Use the uncache_page(...) method."
        )
        if not self.plugin_off:
            self.global_handler.files_tracker.remove_as_cwd_uri(cwd_uri)


    def uncache_page(self, page:Page):
        """
        Allow to remove a page from the global cache, to ensure it will be rendered again.
        This is to be called by external plugins when needed.
        """
        if not self.plugin_off:
            path =path_manager.get_cwd_path_from_docs_dir_and_uri(self.uni_docs_dir, page.file.src_uri)
            self.global_handler.files_tracker.remove_as_cwd_path(path)


    #-------------------------------------------------------------------
    #                           Plugin Events
    #-------------------------------------------------------------------


    def on_startup(self, command:str, dirty:bool):
        self.is_dirty = dirty


    @addresses_auto_log_plugin_on(
        True, always_logged_and_raised=(AddresserConfigError,)
    )
    def on_config(self, config:'MkDocsConfig', **_):
        """
        Extract the config data and compute all the "globally useful" properties for the plugin
        """
#        logger.error(f"\n\n plugin instance id: {id(self)}\n\n")    ##!LOCK
        self.log(LogMessages.on_config_in)
        self._setup(config)
        self._post_setup_config()




    @event_priority(-200)        # pylint: disable-next=unused-argument
    def on_nav(self, _:Navigation=None, *, files:Files, config:MkDocsConfig=None, **__):
        """ Build the references/identifiers for all non markdown files in the docs_dir,
            and log some info for the user to know at what point the executions are.
        """

        if self.plugin_off:
            return

        self._build_identifiers_for_all_files_in_docs_dir_except_markdowns(files)

        self.log(LogMessages.on_nav_in)
#        extractor.refs_snapshot_at('on_nav', self)              ##!





    @addresses_auto_log_plugin_on(
        True, display='page'
    )
    @StaticHandler.on_page_content_cached_with(
        cwd_path_arg_extractor_page_hook,
        never_skip
    )
    def on_page_content(self, html:str, *, page:Page, **_):
        """
        Explore the base html content of the page and extract/build:
            - The references/identifiers defined in the page and their related targets
            - The code snippets (if needed)
            - Store all the identifiers used as targets in the page

        Throw:
            InvalidIdentifierError:     If the identifier is empty ( "{: # oops_space }")
            DuplicateIdentifierError:   If the identifier has already been used (snippets)
            DuplicateIdentifierError:   If the identifier has already been used (references)
        """

        logger.debug('Add file markdown references')
        id_, _ = self.add_links(page, None)                                  ##!
#        extractor.add_html_and_markdown(page, html)                         ##!
#        id_,_def_link = self.add_links(page, None)                          ##!
#        extractor.add(self, page, id_, '(File on HDD...)', _def_link)       ##!


        logger.debug(f'Gather all references used in page: { page.file.src_uri !r}')
        # Done first because og the soup.decompose_header_to_kebab step, which will mutate
        # the content of the html soup tree...

        soup = PluginSoupExcludingCodes(html, self)

        for tag, attr, _, identifier in soup.gen_targeted_addresses_data():
            if self.completion.href_is_possible_ref(identifier):
                logger.debug(f'  Reference used: <{ tag.name } { attr }="{ identifier }">')
                self.global_handler.used_refs.add_id(page,identifier)

        all_external_refs = Counter(extract_external_links_refs_in_md(page.markdown))
        refs_in_code_tags = Counter( soup.get_external_refs_in_codes() )
        actual_refs       = all_external_refs - refs_in_code_tags
        for identifier in actual_refs:
            logger.debug(f'  External link reference used: [...][{ identifier }]')
            self.global_handler.used_refs.add_id(page,identifier)

        if page.file.src_uri in self.skip_identifiers_definitions_in_pages:
            logger.debug(f'Identifiers definitions in page { page.file.src_uri !r} are skipped.')
            return

        logger.debug(f'Add references defined in page: { page.file.src_uri !r}')

        for tag in soup.get_tags_with_ids():

            id_   = tag['id']
            is_h  = re.fullmatch(r'h\d+', tag.name)
            kebab = (
                is_h
                and self.ignore_auto_headers
                and soup.decompose_header_to_kebab(tag)
                or None
            )
            logger.debug(f"Handle tag <{tag.name}>, txt={tag.text} (KEBAB={kebab})")
            if kebab == id_:
                self.log_more(f"\033[35mignore_auto_header=true:\033[0m skipped { id_ !r} id.")
                continue

            self.add_links(page, id_)                                       ##!
#            id_,_def_link = self.add_links(page, id_)                       ##>
#            extractor.add(self, page, id_, tag, _def_link)                  ##<







    @event_priority(-200)
    def on_env(self, *_,**__):
        """ * Setup the counter of exceptions (used in fail_fast=False mode)
            * Log the suppressed and added references (either at debug or info level,
              depending on more_verbose)
            * Inform the user before starting the on_page_context actions (because it can be
              long, so better give a hint that something is still happening...)
        """
        if self.plugin_off:
            return

        suppressed, added = self.global_handler.references.get_update_refs_definitions_info()

        if suppressed:
            data = ''.join( f'\n  {ref} -> {to}' for ref,to in sorted(suppressed.items()) )
            self.log_more("suppressed references:"+data)

        if added:
            data = ''.join( f'\n  {ref} -> {to}' for ref,to in sorted(added.items()) )
            self.log_more("added references..."+data)


        if self.dump_action != DUMP_ONLY:
            self.log(LogMessages.on_env_in)


#        extractor.refs_snapshot_at('on_env', self)              ##!






    @addresses_auto_log_plugin_on(
        True, display='page', log_errors=False
    )
    @StaticHandler.on_page_context_cached_with(
        cwd_path_arg_extractor_page_hook,
        on_page_context_skip,
        page_arg_extractor_page_hooks,
    )
    def on_page_context(self, _ctx, *, page:Page, **__):
        """
        Take a peek at the page.content (html), and extract all the links and images, then:
            1. Replace plugin references with the actual relative path (computed accordingly
               to the current "page location to be")
            2. Validate all the addresses (their final/built version, meaning, all the addresses
               in the final html file: either typed manually or built through the plugin), to
               check that a file actually exists. Raise an error otherwise.

        Note: addresses can be marked as ignored (one way or another). If they are, their validation
              is skipped and no error will (should...) be thrown.

        Throw during path building:
            LeadingSlashAddressError:   If the target address starts with a slash and isn't
                                        ignored (one way or another)
            UnknownIdentifierError:     If an unknown reference identifier is found

        Throw during path checking:
            AddressError:               If use_directory_urls=True, the source file isn't an
                                        index.md file, and the address doesn't start with '../'
            EmptyAnchorError:           If the identifier following an anchor is empty
            ImageWithAnchorError:       If an address used for an image contains an anchor
            AnchorUnknownError:         If an anchor is used but doesn't match with any of the
                                        references stored by the plugin
            AnchorNotInPageError:       If an anchor is used but isn't defined in the current page
            TooManyAnchorsError:        If several anchors are found in the address
            NonRelativeAddressError:    If an address passed the leading slash case but is
                                        not considered relative here (ie starting with a dot)
            NotAnImageAddressError:     If the file is supposed to be an image, but the address
                                        used doesn't match against the imgs_extension_pattern
            NotAFileAddressError:       If a file isn't found (image, internal document, or if
                                        the built url, when turned back into a file uri according
                                        to the current configuration doesn't match a markdown file
            TrailingSlashAddressError:  If use_directory_urls is False and an address is ending with
                                        a slash
        """

#        extractor.add_start_ctx(page)             ##!


        to_check = not self.verify_only or page.file.src_uri in self.verify_only

        soup = PluginSoupExcludingCodes(page.content, self)

        for tag, attr, kind, identifier in soup.gen_targeted_addresses_data():
            logger.debug(f'  Build path for: <{ tag.name } { attr }="{ identifier }">')

            if self.fail_fast:
                self._build_address_and_check_it(page, tag, attr, kind, to_check)
            else:
                try:
                    self._build_address_and_check_it(page, tag, attr, kind, to_check)
                except Exception as exc:                                # pylint: disable=broad-exception-caught
                    exc_name   = exc.__class__.__name__
                    identifier =  f'{ exc_name } | { tag[attr] }'
                    self.global_handler.exceptions_counter.add_id(page, identifier)

        page.content = str(soup)


        # Search now (see warning below) for external links references that would not have been
        # converted because of a wrong reference: at this point, any `[...][...]` still present
        # in the html content, this is NOT in a code tag, is an invalid external link that has
        # not been replaced by mkdocs.
        #
        # WARNING: this is a destructing operation, on the soup instance!
        soup.destroy_codes()

        markdown_no_code_tags = soup.get_text()
        invalid_external_refs = extract_external_links_refs_in_md(markdown_no_code_tags)

        invalid_external_refs.extend(
            gen_invalid_external_links_when_autorefs_used(soup, self.global_handler.references)
        )

        for wrong_ref in invalid_external_refs:
            if self.fail_fast:
                raise UnknownExternalLinkIdentifierError(
                    f"Unknown identifier { wrong_ref !r}, found in file { page.file.src_uri !r}"
                )
            else:
                exc_name   = UnknownExternalLinkIdentifierError.__name__
                identifier =  f'{ exc_name } | { wrong_ref }'
                self.global_handler.exceptions_counter.add_id(page, identifier)



        logger.debug(
            f"on_page_context for page={page.file.src_path!r}: html content update & check done."
        )
#        extractor.add_end_ctx(page)               ##!




    # DO NOT decorate the post build event with cache logic: too much branching logics to
    # apply here, and better to not cache anything (that part won't cost much time anyway!)
    @addresses_auto_log_plugin_on(
        True, log_exceptions_count=True
    )
    def on_post_build(self, *_, **__):
        """ 1) If using VSC, dump all the snippets in the project user snippets file.
            2) Compare the state of the references before the current build and their state
            right now, then warn the user about possible inconsistencies.
            3) raise DumpOnlyError if needed, to abort the build
        """
        if self.dump_action == NO_DUMP:
            self.log(LogMessages.on_post_build_none)
        else:
            self._dump_snippets()

        self._compare_current_state_with_starting_state()

#        extractor.refs_snapshot_at('on_post_build', self)      ##>
#        extractor.flow_dump(self)
#        # extractor.dump(self)                                 ##<

        abort = self.dump_action == DUMP_ONLY
        fatal_if(
            abort, LogMessages.on_post_build_only, DumpOnlyException
        )





    #---------------------------------------------------------------------------




    def log(self, msg:str, with_color=True):
        """ Log with color on the message (unless with_color=False), at INFO level """
        if with_color:
            msg = f"\033[32m{ msg }\033[0m"
        logger.info(msg)



    def log_more(self, msg:str):
        """ Log with color on the message (unless with_color=False), at INFO level """
        show_log = logger.info if self.more_verbose else logger.debug
        show_log(msg)


    def has_exceptions_stored(self):
        return bool(self.global_handler.exceptions_counter)


    def get_exceptions_msg(self):
        return self.global_handler.exceptions_counter.get_errors_info()



    #---------------------------------------------------------------------------





    def _setup(self, config:MkDocsConfig):
        """ First inner step of on_config hook (helps with testing) """
        if self.is_dirty:
            logger.info("Dirty mode: the cache is disabled")
            self.config.activate_cache = False

        self.completion = self.config.validate_and_process(config)
        self.global_handler = StaticHandler.inject(self, config)
                            # Inject ONLY after validation/preprocessing of the config
        self._update_watch_list(config)



    @addresses_auto_log_plugin_on(
        step_name="updating the watch list with inclusions and/or external link file",
        log_errors=False,
    )
    def _update_watch_list(self, config:MkDocsConfig):

        has_includes       = self.use_auto_completion and self.inclusions
        has_external_links = self.external_links_file

        if not has_includes and not has_external_links:
            return

        watching: List[str] = config['watch']
        uri_links = path_manager.to_uri(self.external_links_file) if has_external_links else None

        if has_includes:
            self.log_more(LogMessages.watch_inclusions)

            for inclusion in self.inclusions:
                uri = path_manager.to_uri(inclusion)
                if uri not in watching:
                    watching.append(uri)

        if has_external_links and uri_links not in watching:
            watching.append(uri_links)



    def _post_setup_config(self):
        """ Second inner step of on_config hook (helps with testing) """
        self._extract_and_cleanup_current_snippets_file()
        self._build_inclusions_snippets()
        self._add_external_links_if_needed()






    @addresses_auto_log_plugin_on(
        step_name="extracting the existing code snippets file",
        log_errors=False,
    )
    @StaticHandler.snippets_extraction_cached_with(
        plugin_file_prop_extractor('dump_snippets_file'),
        skip_if_no_autocompletion_or_no_snippets_file_or_wrong_extension,
    )
    def _extract_and_cleanup_current_snippets_file(self):
        """ If using VSC and a code snippets file is provided, extract it and check if the user
            added anything not related to the plugin. If so, store that for the next dump.
            Every entry related to the plugin is discarded.
        """
        self.log_more(LogMessages.setup_snippets)
        snippets = self.dump_snippets_file.read_text()
        self.completion.store_other_snippets(snippets)




    @addresses_auto_log_plugin_on(
        step_name="building files inclusions snippets",
        log_errors=False,
    )
    def _build_inclusions_snippets(self):
        """ Travel recursively through the content of each paths in the inclusions and build
            the related snippets.
        """
        if self.use_auto_completion and self.inclusions:

            self.log_more(LogMessages.build_inclusions)

            for root_include in self.inclusions:
                for file in root_include.rglob('./*'):
                    if file.is_file():
                        self._gather_inclusions_in(file, root_include)


    @StaticHandler.other_files_cached_with(
        cwd_path_arg_extractor_inclusions,
        skip_if_file_already_registered,
    )
    def _gather_inclusions_in(self, file:PathCwd, root_inclusion:Path):
        uri = path_manager.to_uri(file)
        root_inclusion_uri = path_manager.to_uri(root_inclusion)
        self._add_snippets(
            file, RefKind.Include, uri, uri,
            root_inclusion=root_inclusion_uri,
            # inclusions_with_root=self.inclusions_with_root
        )






    @addresses_auto_log_plugin_on(
        step_name="extracting the external links from a specific file",
        log_errors=False,
    )
    @StaticHandler.external_links_cached_with(
        plugin_file_prop_extractor('external_links_file'),
        skip_if_no_external_links,
    )
    def _add_external_links_if_needed(self):
        """ Add external links

            Note: The references of those links aren't stored, and only the autocompletion
                  informations are actually interesting, because mkdocs will replace the identifiers
                  on it's own. But the equivalent references are stored anyway so that the txt file
                  dumped when use_auto_completion=false still contains everything.
        """
        self.log_more(LogMessages.setup_links)
        code = self.external_links_file.read_text()
        self._add_external_links(code)


    def _add_external_links(self, code:str):
        """ Unconditional addition of the external links contained in the given markdown code.
            (separated from _add_external_links_if_needed to help with testing)
        """
        matches   = re.findall(r'^\[([^\]]+)\]:\s*(\S+)', code, flags = re.MULTILINE)
        rel_paths = ''.join( f"\n    { id !r}: { link !r}"
                                for id,link in matches
                                if not self.black_list_pattern.match(link) )
        fatal_if(
            rel_paths,
            f"All links in the external_links_file ({ self.external_links_file !r}) "
            f"should be absolute, but got:{ rel_paths }\n"
            "(update the configuration property links_white_match, to bypass this).\n",
            NonAbsoluteAddressError
        )
        for identifier, link in matches:
            self.__add_data(self.external_links_file, RefKind.Ext, identifier, link)






    @addresses_auto_log_plugin_on(
        step_name="building the identifiers for all non markdown files in the docs_dir"
    )
    def _build_identifiers_for_all_files_in_docs_dir_except_markdowns(self, files:Files):
        """ Add all fixed files in the docs directory:, except for markdown ones
            (let mkdocs build the urls for those, according to the user's settings)
        """
        self.log(LogMessages.setup_non_md_files)

        for file in files:
            cwd_path = self.uni_docs_dir / file.src_path
            uri = file.src_uri

            is_md = uri.endswith('.md')
            is_builtin = is_md or (
                uri.startswith('assets/javascripts/')
                or uri.startswith('assets/stylesheets/')
                or uri == 'assets/images/favicon.png'       # mkdocs default config
            )
            is_to_skip = is_builtin or self.is_to_skip(str(cwd_path))
            if not is_to_skip:
                self.add_file_infos(cwd_path, file)




    @StaticHandler.other_files_cached_with(
        cwd_path_arg_extractor_other_files,
        skip_if_file_already_registered,
    )
    def add_file_infos(self, _:PathCwd, file:File):
        """ Add the reference and code snippet for a specific file (non markdown)
            Notes:
                - first argument needed for the other_file_arg_extractor function
                - all files are in the docs_dir, here

            ---

            Only the file existence is needed here, not its content, so "up_to_date" has
            actually no useful meaning for any of this.
            The only reason to go through the decoration/cache thing is to keep track of
            the references of the files, to spot later outdated references in the docs.
        """
        is_img   = self.imgs_extension_pattern.search( file.src_uri )
        kind     = RefKind.Img if is_img else RefKind.File
        cwd_path = self.uni_docs_dir / file.src_uri
        self.__add_data(cwd_path, kind, file.src_uri, file.url)








    def __add_data(
        self,
        src: SourceRef,
        kind: RefKind,
        identifier: str,
        def_link: str,
    ):
        final_id = self._add_snippets(src, kind, identifier, def_link)
        msg = f"For {identifier=!r}, add a reference as {final_id=!r} pointing to {def_link=!r}"
        logger.debug(msg)
        self.global_handler.references.add_id(src, final_id, def_link, identifier)

        return final_id         # investigation purpose only



    def _add_snippets(
        self,
        src:SourceRef,
        kind:RefKind,
        identifier:str,
        def_link:str,
        **extras
    ) -> str :
        """ Add a code snippet to the Reference object.

            @src:        page, or PathCwd to the file generating the snippet
            @kind:       Kind of references (see RefKind)
            @identifier: Bare identifier that will be used to build the code snippet prefix
                         (for example: "plain-address" -> "--plain-address" for a RefKind.Link,
                         or "code_ex.py" -> "<<py code_ex.py" for a RefKind.Include, ...)
            @def_link:   Target document/link for the snippet(s) (as uri)
            @**extras:   Extra arguments that will be passed to the VscAutoCompletion.build_snippet
                         method.
        """
        completer = self.completion.get_for(kind)
        final_id  = completer.get_final_identifier(identifier)

        if self.use_auto_completion:
            logger.debug(f"Adding code snippet(s) for {identifier=!r}: {def_link=!r}")
            for json_id,snippet in completer.build_snippet(identifier, def_link, **extras):
                self.global_handler.references.add_snippet(src, json_id, snippet)

        return final_id




    #-----------------------------------------------------------------------------------





    def add_links(self, page:Page, identifier: Union[str,None]):
        """ Add an id reference to the current References object, building the needed url
            relative to the docs root directory (in the built static site!).
            If no @id is provided or @id is None, build the link for the "bare" file itself.
        """
        logger.debug(f"Adding { identifier !r} reference from page { page.file.src_uri !r}")
        if identifier is None:
            identifier = def_link = page.url or './'
            # Note: page.url can be empty only when using use_directory_url=true

        else:
            # Security check (may happen on mistaken attr: "{: # deep-stuff }") :
            fatal_if(
                not identifier,
                "\n '' (empty) identifier found. Check you didn't make any typo, like "
                "\"{: # oops }\" which has an extra space.",
                InvalidIdentifierError)

            def_link = f"{ page.url }#{ identifier }"

        identifier = self.__add_data(page, RefKind.Link, identifier, def_link)

        return identifier, def_link         # investigation purpose only



    def __build_path_from_caller_to_id(self, caller:Page, identifier:str):
        """ Given an identifier and the Page from where it's used, build the appropriate
            relative path for the built site and returns it.
        """
        refs = self.global_handler.references
        fatal_if(
            not refs.has_id(identifier),
            f"Unknown identifier { identifier !r}, found in file { caller.file.src_uri !r}",
            UnknownIdentifierError
        )

        n_upper       = caller.url.count('/')
        up_to_docs    = '../' * n_upper or './'
        relative_link = up_to_docs + refs.get_ref_target_address(identifier)

        logger.debug(f"Built relative path for {identifier=!r}: {relative_link=!r}")
        return relative_link




    @addresses_auto_log_plugin_on(
        display="page:0 tag:1 attr:2", joiner=' ',
        step_name="Replacing the identifier with the relative address and checking their validity",
    )
    def _build_address_and_check_it(
        self,
        page: Page,
        tag: Tag,
        attr: str,
        kind: AddressKind,
        to_check: bool,
    ):
        identifier = target = tag[attr]
        is_built_ref = False

        # Forbid accidental addresses with leading slash:
        fatal_if(
            to_check and identifier.startswith('/'),
            f"No leading slash address allowed: {identifier!r}.\nIf you absolutely need it, "
            'mark it as ignored, one way or another (black_list_pattern, or '
            'ignored_identifiers_or_addresses).',
            LeadingSlashAddressError
        )

        if self.completion.href_is_possible_ref(identifier):
            logger.debug(f"Build the correct relative path for \"{identifier}\"...")
            target    = self.__build_path_from_caller_to_id(page, identifier)
            tag[attr] = target
            logger.debug(f"\"{ identifier }\" built as: { target !r}")
            is_built_ref = True


        # If not bare anchor and not any obvious "relative" indications, enforce the
        # relative aspect of the target, because that's how mkdocs will finally handle
        # the address in the built site (note: this ahs been added in the logic because
        # the leading dot might be lost on images addresses, specifically...):
        if not target.startswith('.') and not re.match('[/#]', target):
            target = './' + target
            logger.debug(f"Enforced relative path to: {target=!r}")


        # Check the address only if it has not been built by the plugin (this is assuming
        # it will do a proper job... :p )
        if to_check and not is_built_ref:
            AddressChecker.check(self, page, target, kind)



    def build_snippets_code(self):
        """ Build all snippets """
        code = self.completion.build_snippets_code(self)
        return code



    def _dump_snippets(self):
        logger.debug(f"Building data to dump (ide={ self.ide })")

        code = self.build_snippets_code()
        self.dump_snippets_file.parent.mkdir(exist_ok=True)
        self.dump_snippets_file.write_text(code)
        self.global_handler.files_tracker.mark_file(self.dump_snippets_file)

        self.log(LogMessages.on_post_build_out)



    @addresses_auto_log_plugin_on(
        step_name="comparing references defined on last run with the current one",
        log_errors=False,
    )
    def _compare_current_state_with_starting_state(self):
        self.log(LogMessages.cross_ref_check)
        oops_lst = self.global_handler.get_missing_refs_infos()
        fatal_if(
            oops_lst,
            "References found in existing documents that do not point anywhere (the reference "
            +"isn't defined anymore):"
            +''.join(oops_lst),
            OutdatedReferenceError
        )
