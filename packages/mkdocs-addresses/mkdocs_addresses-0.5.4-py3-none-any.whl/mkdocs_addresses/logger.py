"""
See: https://github.com/mkdocs/mkdocs/discussions/3241
"""
from argparse import Namespace
import platform
import traceback
import logging

from typing import TYPE_CHECKING, Any, MutableMapping, Optional, Tuple
from functools import wraps

from mkdocs_addresses.exceptions import AbortError, AddresserError
from mkdocs_addresses.toolbox import plugin_dump_padder

if TYPE_CHECKING:
    from .addresses_plugin import AddressAddressesPlugin






class LogMessages(Namespace):
    """ Holds all the INFO level messages """

    on_config_in        = "Setup config and plugin instance"
    setup_non_md_files  = "Add references for non md files in docs_dir"
    on_nav_in           = "Gather references definitions in all pages..."
    on_env_in           = "Replace references with addresses, checking them..."
    on_post_build_none  = "No code snippets created"
    on_post_build_out   = "Code snippets dump successful"
    on_post_build_only  = '"Code snippets only" mode: abort mkdocs build.'
    cross_ref_check     = "Check for outdated references in unmodified files"

    # --- log_more ---
    setup_snippets      = "Extract existing code snippets"
    watch_inclusions    = "Add inclusions directories and/or external links file to mkdocs watch array"
    build_inclusions    = "Build code snippets for inclusions"
    setup_links         = "Extract external links"









class Logger(logging.LoggerAdapter):
    """A logger adapter to prefix messages with the originating package name."""

    is_in_tests = False

    def __init__(self, prefix: str, logger: logging.Logger):
        """Initialize the object.

        Arguments:
            prefix: The string to insert in front of every message.
            logger: The logger instance.
        """
        super().__init__(logger, {})
        self.prefix = prefix
        if platform.system() != 'Windows':
            self.prefix = f"\033[35m{ prefix }\033[0m"

    def process(self, msg: str, kwargs: MutableMapping[str, Any]) -> Tuple[str, Any]:
        """Process the message.

        Arguments:
            msg: The message:
            kwargs: Remaining arguments.

        Returns:
            The processed message.
        """
        return f"{self.prefix}: {msg}", kwargs








def get_plugin_logger(name: str) -> Logger:
    """Return a logger for plugins.

    Arguments:
        name: The name to use with `logging.getLogger`.

    Returns:
        A logger configured to work well in MkDocs,
            prefixing each message with the plugin package name.
    """
    _logger = logging.getLogger(f"mkdocs.plugins.{name}")
    return Logger(name.split(".", 1)[0], _logger)




logger = get_plugin_logger(__name__.replace('_','-'))



def addresses_auto_log_plugin_on(
    is_event:               bool = False,
    display:                str  = "",
    joiner:                 str  = '\n  ',
    step_name:              Optional[str] = None,
    log_errors:             bool = True,
    log_exceptions_count:   bool = False,
    always_logged_and_raised: Tuple = (),
):
    """ Wrap a method of AddressAddressesPlugin and automatically log:
            - DEBUG: When entering the decorated method
            - ERROR: the raised error with custom informations:
                - the error kind
                - the method name
                - info about the arguments (see @display)

        @is_event:  True if the decorated method is one of the plugin event method (identify
                    entry points, to not raise from there, if fail_fast option is false).
        @display:   A space separated string in the format "name" or "name:index", which tells
                    what to add to the log message, and how to find it in the varargs/kwargs:
                       "name" => search in kwargs / "name:i" => use varargs[int(i)]

                    WARNING about arguments with default values: they are in the signatures, but
                    aren't showing up in the *a and **kw of the decorators! => simplest way out of
                    this: just pass the default value explicitly (or avoir default values...).
        @joiner:    String to use to join the "extras" infos (see @display)
        @step_name: if defined, replace the method name in the log, when an error is logged.
        @log_errors: allow to not log when there is already a nested call logging stuff, or
                    when an upper level will do it

        The arguments are transformed using the functions in TRANSFORM, associating a
        transformation to a name. By default, not transformation are done.
    """

    display_lst = display and display.split()
    transforms = {
        'page': lambda page: repr(page.file.src_uri),
        'tag':  lambda tag:  repr(tag.name),
    }

    def build_info_getter(prop:str, i:Optional[str]=None):
        trans = transforms.get(prop, repr)
        if i is None:
            return lambda _,kw: f"{ prop }={ trans(kw[prop]) }"
        else:
            return lambda a,__: f"{ prop }={ trans(a[int(i)]) }"

    extras = [ build_info_getter(*chunk.split(':')) for chunk in display_lst ]

    def decorator(method):
        @wraps(method)
        def wrapper(self:'AddressAddressesPlugin', *a, **kw):

            if self.plugin_off:
                return

            # pages context exceptions global count must be shown before the information about
            # entering on_post_build is given to the user:

            if log_exceptions_count and self.has_exceptions_stored():
                warn_message = (
                    'running with fail_fast=false...\n' +
                    'Summary of the exceptions raised while managing the references in the pages:' +
                    self.get_exceptions_msg()
                )
                logger.warning(warn_message)


            more_info  = joiner.join( get_info(a,kw) for get_info in extras)
            tail_entry = more_info and " with " + more_info
            where      = step_name or method.__name__

            more_verbose   = getattr(self, 'more_verbose', False)     # fails for non obvious reason => default to False...
            entry_log_func = logger.info if is_event and more_verbose else logger.debug
            entry_log_func(f"\033[34m{ where }{ tail_entry }\033[0m")

            try:
                return method(self, *a, **kw)

            except Exception as exc:                        # pylint: disable=all
                do_raise = (
                    isinstance(exc, always_logged_and_raised)       # special case
                    or self.fail_fast                               # _do_ fail
                    or not is_event                                 # always raise from deeper levels
                )
                do_log = log_errors or isinstance(exc, always_logged_and_raised)
                if do_log:
                    exc_name      = exc.__class__.__name__
                    intro         = ( f"\033[31m{ exc_name }\033[0m - { where }(...)"
                                    +  "\n  " * bool(more_info) )
                    formatted_exc = f"\033[34m{ exc }\033[0m"
                    log_msg       = f"{ intro }{ more_info }\n  { formatted_exc }"
                    if not isinstance(exc, AddresserError):
                        log_msg += '\n' + traceback.format_exc()

                    logger.error(log_msg)

                if do_raise:
                    if logger.is_in_tests or (          # tests need the actual error to check logic correctness
                        (not self.fail_fast or log_errors or not is_event)
                        and not isinstance(exc, always_logged_and_raised)
                    ):
                        raise
                    else:
                        # here, the error already got logged to the console, but mkdocs will log
                        # it's message again with its own logger. So throw something else to avoid
                        # the duplicated message
                        raise AbortError('Build cancelled from mkdocs-addresses (fail_fast is true)') from exc

        return wrapper
    return decorator
