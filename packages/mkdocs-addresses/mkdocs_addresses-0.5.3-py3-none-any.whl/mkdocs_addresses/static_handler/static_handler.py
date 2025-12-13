#from threading import Lock      ##!LOCK


from typing import TYPE_CHECKING, Any, Callable

from functools import wraps

from mkdocs.structure.pages import Page
from mkdocs.config.defaults import MkDocsConfig
from mkdocs_addresses.auto_completion_handler import COMPLETION_CLASSES_CONFIG


from mkdocs_addresses.logger import logger
from mkdocs_addresses.exceptions import (
    NoStaticHandlerError,
#    ConcurrentPluginError,                                 ##!LOCK
)
from mkdocs_addresses.static_handler.tracker_errors_counter import ContextExceptionsTracker


from .files_tracker import FilesTracker
from .types_aliases import PathCwd
from .tracker_addresses_usage_pool import AddressesUsagePool
from .tracker_references import References


if TYPE_CHECKING:
    from mkdocs_addresses.addresses_plugin import AddressAddressesPlugin




FileNameExtractor = Callable[ [Any], PathCwd]
""" Function used to extract the source uri (as string) and the actual PathCwd of the file
    related to a decorated plugin method.
    The received arguments are those of the decorated method, _self included_.

    The function has to return a PathCwd (Path), which is the actual path of the related
    file on the disk, rooted at the cwd.
"""


DecoratorEventCbk = Callable
""" Arguments of the decorated method, prepended with the uri and the real path of the "file of
    interest" for the decorated method. Hence:

    `function( src:UriPath, real:PathCwd, plugin, *args, **kw )`

    WARNING:

        src may be relative to the docs_dir, or to the cwd, depending on the decorated function,
        and is not an actual path anyway. It's more like the identifier of a file in mkdocs.
"""



#---------------------------------------------------------



def clear_other_snippets(_, plugin:'AddressAddressesPlugin', *ça,**_kw):
    logger.debug("Clear snippets unrelated to the plugin")
    plugin.completion.clear_other_snippets()


def clear_references_from_src(cwd_path, *_,**__):
    logger.debug(f"Clear previous references for the file {cwd_path=!r}")
    StaticHandler.HANDLER.clear_file_related_data(cwd_path)


def mark_src_as_up_to_date(cwd_path, *_, **__):
    logger.debug(f"Mark file {cwd_path=!r} as updated")
    StaticHandler.HANDLER.files_tracker.mark_file(cwd_path)










class StaticHandler:
    """
    Global object that will manage everything needed to handle more gracefully the performances
    of the plugin:

    * keep track of the last modified files (timestamp based)
    * wrap the hooks of the plugin to bypass useless calls, depending on the plugin configuration
    * store the global internal state(s)


    One unique instance will be created during the on_config event if it doesn't already exist,
    and then reused on each new build.
    Teardown automatically occurs with on_shutdown, when the thread is closed.
    """


    used_refs: AddressesUsagePool
    """ Associate all the references to identifiers with the page they are used in:
            id_to_sources:  reference -> set of all pages using this reference
            source_to_ids:  source    -> set of all references used in that source file
    """

    references: References
    """ Associate all the identifiers with their actual target:
            id_to_data:     "--duh" -> target of the defined identifier
            id_to_source:   "--duh" -> source = the file where the identifier is declared:
                                       page.file.src_uri or filename (slash separated)
                                       (this is the target link, stripped of any anchor, actually)
            source_to_ids:  for the given file, register all the identifiers defined there
    """

    exceptions_counter: ContextExceptionsTracker
    """ Keep track of the errors found by the plugin on previous builds, to keep the feedback
        consistent for the user.
    """

    files_tracker: FilesTracker
    """ Keeps track of the time of last modifications of various files in the project """



    HANDLER: 'StaticHandler' = None
    ACTIVATE_CASH = True

    # testing purpose only
#    LOCK = Lock()                                                           ##>LOCK
#    USE_LOCK = False                                                         ##<LOCK


    @classmethod
    def inject(cls, plugin:'AddressAddressesPlugin', config:MkDocsConfig):
        """
        Inject the plugin in the StaticHandler "context", handling its singleton instance.
        """

        cls.ACTIVATE_CASH = plugin.config.activate_cache

#        if cls.USE_LOCK:                                                    ##>LOCK
#            if cls.LOCK.locked():
#                raise ConcurrentPluginError("Already locked")
#            cls.LOCK.acquire()                                              ##<LOCK

        # if the cache is not activated, also rebuild a fresh instance:
        if not cls.HANDLER:
            plugin.log_more("Initiate cache manager")
            cls.HANDLER = StaticHandler(plugin, config)

        elif not cls.ACTIVATE_CASH:
            plugin.log_more("Cache manager deactivated")
            cls.HANDLER.clean_up(plugin, config)

        else:
            plugin.log_more("Refresh cache manager")
            cls.HANDLER.rebuild_with(plugin, config)

        return cls.HANDLER



#    @classmethod                                                            ##>LOCK
#    def unlock(cls):
#        if not cls.LOCK.locked():
#            raise ConcurrentPluginError("Wasn't locked yet")
#        cls.LOCK.release()                                                  ##<LOCK




    #---------------------------------------------------------------------------


    _config:       MkDocsConfig                 # archive just in case (but most likely useless)
    _plugin:      'AddressAddressesPlugin'      # archive just in case


    def __init__(self, plugin:'AddressAddressesPlugin', config:MkDocsConfig):
        """ Instantiate only with an already validated/preprocessed plugin instance """
        self.clean_up(plugin, config)


    def clean_up(self, plugin:'AddressAddressesPlugin'=None, config:MkDocsConfig=None):
        """
        Reset the internals of the global StaticHandler, but keeping the current global innstance
        alive (testing purpose, mostly)
        """
        if plugin:
            self._plugin = plugin
        if config:
            self._config = config

        self.used_refs          = AddressesUsagePool(uni_docs_dir=plugin.uni_docs_dir)
        self.exceptions_counter = ContextExceptionsTracker(uni_docs_dir=plugin.uni_docs_dir)
        self.files_tracker      = FilesTracker()
        self.references         = References(uni_docs_dir=plugin.uni_docs_dir)

        for TopClass,*_ in COMPLETION_CLASSES_CONFIG.values():
            TopClass.clear_other_snippets()

        return self


    def rebuild_with(self, plugin:'AddressAddressesPlugin', config:MkDocsConfig):
        """ On a new build, use the fresh instances, checking if a global rebuild of the
            internal data must be made or note.
            This happens on_build only.
        """
        self._plugin = plugin
        self._config = config
        self.used_refs.archive_current(plugin.uni_docs_dir)
        self.references.archive_current(plugin.uni_docs_dir)
        self.exceptions_counter.archive_current(plugin.uni_docs_dir)

        # clean up from any outdated files (deleted since last build)
        uris_and_paths = self.files_tracker.get_uris_and_paths()
        cleared = []
        for cwd_src in uris_and_paths:
            if not cwd_src.is_file():
                cleared.append(cwd_src)
                self.files_tracker.remove_as_cwd_path(cwd_src)
                self.clear_file_related_data(cwd_src)

        if cleared:
            msg = 'Removed files:' + ''.join(f'\n   {file}' for file in cleared)
            self._plugin.log_more(msg)


    def clear_file_related_data(self, src:PathCwd):
        """ Remove all references or snippets data related to the given src_uri """
        logger.debug(f"Cleared references of the { src !r} file")
        self.used_refs.remove_source(src)
        self.references.remove_source(src)
        self.exceptions_counter.remove_source(src)


    def get_missing_refs_infos(self):
        return self.used_refs.get_missing_refs_infos( self.references.id_to_data )



    #---------------------------------------------------------------------------



    @classmethod
    def __cached_call_decorator(
        cls,
        filename_extractor: FileNameExtractor,
        skip_if: Callable[[Any],str],
        *,
        before_method_call:  DecoratorEventCbk=None,
        after_method_call:   DecoratorEventCbk=None,
        # finally_after_call:  DecoratorEventCbk=None,
        # on_errors: Dict[Type[Exception], DecoratorEventCbk] = {},
        apply_if_not_called: DecoratorEventCbk=None,
    ):
        """ Decorator to add caching logic to plugin methods.

            Overall idea: Each call must be relatable to one file on the disk. So:

            1. Extract the name of the related file, using the filename_extractor callback.
               WARNING: the filename_extractor callback has to return the PathCwd of the file.

            2. Check if:
                - the plugin config ask for skipping the call or not, using a specifically named
                  method: skip_{...}_if(plugin, *args, **kw). This method can apply other kind of
                  considerations to forbid the call, if needed.
                - that file has been modified or not since the last call

            3.a. If the call to the decorated method must be done, this call is surrounded with
                 other callbacks calls, so that logic to handle things related to the cached data
                 can be applied:
                    a. Call the "before" callback
                    b. Call the decorated method
                    c. Call the "after" callback
            3.b. If the method must not be called, the apply_if_not_called callback is used instead.

            All callbacks, except the filename extractor and the skip ones, are optional.

            WARNING:
              * Exceptions in the call are NOT handled here, so the "after_method_call" logic
                might not always be applied. This is to keep in mind, but generally, this means
                the files won't be marked as up to date, so it's ok.
              * On the other hand, Exceptions that _are_ caught in the wrapped function might
                cause problems if a failure has occurred but the "after_method_call" is executed
                anyway. Generally, it's not a big problem, because the user will have the feedback
                in the console, will update the file, and so everything will be alright. But to
                limit the potential problems, better to wrap this decorator with the auto_logger
                one than the opposite (since the logger might swallow some exceptions...).
        """
        # pylint: disable=multiple-statements, protected-access

        def decorator(method:Callable):

            # Note: The checks on ACTIVATED_CASH and the cbks definitions must be made at run time
            #       only, incase the state changes in between calls.

            @wraps(method)
            def wrapper(self:'AddressAddressesPlugin', *args, **kwargs):

                if self.plugin_off:
                    return

                if not cls.HANDLER:
                    raise NoStaticHandlerError(
                        "Wrong use of one of the StaticHandler decorators: the global HANDLER "
                        "instance should have been already defined"
                    )

                cached_file = filename_extractor(self, *args, **kwargs)
                # cls.HANDLER.__check_src_uri(cached_file)
                to_skip     = skip_if(self, *args, **kwargs)
                up_to_date  = to_skip or cls.HANDLER.files_tracker.is_file_up_to_date(cached_file)

                need_to_run = not (to_skip or up_to_date)
                if not cls.ACTIVATE_CASH or need_to_run:
                    # Always use this branch if caching is deactivated

                    if before_method_call and cls.ACTIVATE_CASH:
                        before_method_call(cached_file, self, *args, **kwargs)

                    # If the cash isn't activated, the skip check did not occur so, done here
                    # so that the behaviors stay consistent:
                    if cls.ACTIVATE_CASH or not skip_if(self, *args, **kwargs):
                        method(self, *args,  **kwargs)

                    if after_method_call and cls.ACTIVATE_CASH:
                        after_method_call(cached_file, self, *args, **kwargs)

                elif apply_if_not_called:
                    apply_if_not_called(cached_file, self, *args, **kwargs)

            return wrapper
        return decorator





    #---------------------------------------------------------------------------
    #       Decorators (as class methods) to wrap around the plugin logic
    #---------------------------------------------------------------------------



    @classmethod
    def snippets_extraction_cached_with(cls, filename_extractor:Callable, skip_if:Callable):
        """ If the snippets file is valid and has been modified (or is not cached yet):
                - before: clear any previous data for snippets entries that wouldn't be related
                          to the plugin itself.
                - call:   apply the logic of extraction
                - after:  register the last modification date of the file
        """
        return cls.__cached_call_decorator(
            filename_extractor,  skip_if,
            before_method_call = clear_other_snippets,
            after_method_call  = mark_src_as_up_to_date,
        )



    @classmethod
    def external_links_cached_with(cls, filename_extractor:Callable, skip_if:Callable):
        """ TODO: finish (or just check it's ok like this...) """

        return cls.__cached_call_decorator(
            filename_extractor,  skip_if,
            before_method_call = clear_references_from_src,
            after_method_call  = mark_src_as_up_to_date,
        )



    @classmethod
    def other_files_cached_with(cls, filename_extractor:Callable, skip_if:Callable):
        """ TODO: finish (or just check it's ok like this...) """

        return cls.__cached_call_decorator(
            filename_extractor,  skip_if,
            before_method_call = clear_references_from_src,
            after_method_call  = mark_src_as_up_to_date,
        )



    @classmethod
    def on_page_content_cached_with(cls, filename_extractor:Callable, skip_if:Callable):
        """ 'on_page_content' gathers the information needed for the identifiers and the snippets
            only, and does so working on one single page (ie .md) file, so:

            If the file has been changed or is not cached yet:
                1. before: remove any snippet/ref related to that file
                2. call

            Note: do NOT mark the file now, otherwise on_page_context won't apply.
        """
        return cls.__cached_call_decorator(
            filename_extractor,  skip_if,
            before_method_call = clear_references_from_src,
        )



    @classmethod
    def on_page_context_cached_with(
        cls,
        filename_extractor:Callable,
        skip_if:Callable,
        page_arg_extractor_page_hooks:Callable,
    ):
        """ 'on_page_context' parses the rendered html file, replaces all the identifiers,
            computing the needed relative paths to reach the targets from the current file, and
            check that all the addresses in the page are compliant with the plugin rules, so:

            If the file has been changed or is not cached yet, and if the plugin is not in
            "dump_only" mode:
                1. call
                2. after: cache the page.content value and register the last modification
                          date of the file.
            If the above condition wasn't met, the cached value of page.content is restored,
            so that the built page is still the expected one.
        """

        def after_mark_page_and_cache_content(cwd_path, plugin, *args, **kw):
            cls.HANDLER.files_tracker.mark_file(cwd_path)
            page:Page = page_arg_extractor_page_hooks(plugin, *args, **kw)
            cache[cwd_path] = page.content

        def apply_restore_from_cache(cwd_path, plugin:'AddressAddressesPlugin', *args, **kw):
            plugin.log_more(f"Restore cached content for { cwd_path }")
            if cwd_path in cache:
                page:Page = page_arg_extractor_page_hooks(plugin, *args, **kw)
                page.content = cache[cwd_path]

        cache = {}     # Will never get purged until the server is stopped, but hey... ;p

        return cls.__cached_call_decorator(
            filename_extractor,  skip_if,
            after_method_call   = after_mark_page_and_cache_content,
            apply_if_not_called = apply_restore_from_cache,
        )
