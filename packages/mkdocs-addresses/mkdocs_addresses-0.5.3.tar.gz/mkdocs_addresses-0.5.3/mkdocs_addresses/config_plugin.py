from argparse import Namespace
import os
from pathlib import Path
import re

from typing import Any, Callable, List, Literal, Optional, Set, Tuple, TYPE_CHECKING, Type, Union

from mkdocs.config import config_options  as C
from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig

from . import path_manager
from .logger import logger
from .exceptions import AddresserConfigError, InvalidOperationError
from .auto_completion_handler import (
    AutoCompletion,
    IDE_OPTIONS, VSC, IdeKind,
    validate_config_and_get_auto_completion_handler,
)


if TYPE_CHECKING:
    from .addresses_plugin import AddressAddressesPlugin






# Definition used for mkdocstrings
class PluginOptions(Namespace):


    activate_cache: bool = True
    """
    Exploring the resulting html content of a page to gather and cross-check all the identifiers
    and addresses can be rather time-consuming. This means the plugin can significantly slow down
    the serve operations when the number of documents or their size become increase.

    To mitigate the issue, the plugin utilizes a cache (activated by default).

    When activated, only the recently modified markdown files will be re-evaluated during the next
    serve operation. This drastically reduces the serving time without changing the underlying
    logic of the plugin.

    Note that when mkdocs starts, all pages must be explored at least once, so the first serve
    operation can be very slow on big documentations.
    """


    black_list_pattern: str = "https?://|ftps?://|file:///|www\\."
    """
    Regex string: all addresses or identifiers that will
    [`re.match`](https://docs.python.org/3/library/re.html#re.match){: target=_blank } with it will be ignored.

    This allows to register absolute addresses, external links, or any other unusual scenarios you could
    think of, so that errors are not raised by the plugin when handling them.
    """

    black_listed_patterns: List[str] = []
    """
    Alternative to black_list_pattern, to get simpler declarations. Both will be merge with OR.
    """


    dump_action: str = 'normal'
    """
    The plugin normally dumps information about all the available references  on each serve
    (either as a file of code snippets, or as a text file. See
    [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file]
    option). The `dump_action` may change that behavior:

    * `normal`: the plugin recreates the informations on each serve.
    * `none`: the plugin behaves normally, but the
      [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file]
      is not updated.
    * `only`: the plugin gather the identifiers definitions, skips all verifications, dump the
      [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file]
      and finally raises [`DumpOnlyException`](--mkdocs_addresses_exceptions_DumpOnlyException)
      to stop serving.

        This option is useful when there's a need to regenerate code snippets while something
        in the addresses verifications steps causes a crash.
    """


    dump_snippets_file: str = ''
    """
    Define the location, relative to the cwd, of the file where the information regarding all
    the identifiers (either code snippets configuration or plain text) will be stored.

    There are restrictions about the name of this file:

    * The file cannot be in the `docs_dir` (it should never be anyway).
    * The extension of the file must be compatible with the value chosen for the
    [`ide`][mkdocs_addresses.config_plugin.PluginOptions.ide] option (see table below).
    * If left undefined, the filename is automatically defined, depending on the value of the
      [`ide`](--mkdocs_addresses_config_plugin_PluginOptions_ide) option:

    | `ide` | Default `dump_snippets_file` | Required file extension |
    |:-|:-|:-|
    | `none` | `addresses_identifiers.txt` | `.txt` |
    | `vsc` | `.vscode/links.code-snippets` | `.code-snippets` |
    """


    external_links_file: str = ''
    """
    Location of the file where are defined the global links/references, if any:

    ```markdown
    [mkdocs]: https://www.mkdocs.org/ "mkdocs - home"
    [id]: address "tooltip"
    ...
    ```

    If this option is defined:

    - This file cannot be in the docs_dir itself (it should never be anyway).
    - All links defined in the file must be absolute. If not, the plugin will raise a
      [NonAbsoluteAddressError](--mkdocs_addresses_exceptions_NonAbsoluteAddressError).
      It is possible to bypass this restriction by marking the address as ignored, using
      [`black_list_pattern`](--mkdocs_addresses_config_plugin_PluginOptions_black_list_pattern) or
      [`ignored_identifiers_or_addresses`](--mkdocs_addresses_config_plugin_PluginOptions_ignored_identifiers_or_addresses))
      configuration options.
    - This file should be appended automatically to all files through the
      [`pymdownx.snippets`][PyMdown-snippets]{: target=_blank } markdown extension, directly from
      the `mkdocs.yml` file. For example:

        ```yaml
        markdown_extensions:
            - pymdownx.snippets:
                check_paths: true
                auto_append: ["docs_logistic/external-links.md"]

        plugins:
            - mkdocs-addresses:
                external_links_file: docs_logistic/external-links.md
        ```
    """


    fail_fast: bool = False
    """
    This option determines whether the errors raised by the plugin will completely stop the
    serving process or will only provide information in the console without causing interruptions.

    During the documentation creation process, it can be advantageous to set this option to false.
    This way, there is no need to restart the server each time the plugin finds an incorrect link.
    Instead, you can continue working and address errors one by one.

    If `fail_fast` is set to false, a summary of all the wrong addresses found will be displayed
    once all the pages have been checked. This is especially helpful when there are a lot of
    errors and the content of the console becomes overwhelming.

    The summary is formatted like this:

    ```
    WARNING -  mkdocs-addresses: running with fail_fast=false...
               Summary of the exceptions raised while managing the references in the pages:
                   {error name}:    {error count}
                     {file location}     {identifier triggering the error}
    ```

    In these summaries, if the same identifier triggers several times the same error on the same
    page, it is counted only once.

    Note that some errors will appear separately from these summaries. Specifically,
    [`OutDatedReferenceError`](--mkdocs_addresses_exceptions_OutdatedReferenceError), which is
    checked at a different point during the validation process.
    """


    ide: IdeKind = VSC
    """
    Controls the kind of IDE used, for the autocompletion features. Possible values are:

    * `none`: no autocompletion activated. A simple txt file with all the available identifiers will
      be generated (see [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file]).

    * In any other case, code snippets will be automatically generated and saved in the appropriate
      [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file].

    Note:
        Remember that this option determines the kind of file used for the
        [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file]
        option: if a filename is assigned to it, its extension has to match with the chosen value
        for `ide` (see the [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file]
        section above).
    """


    ignore_auto_headers: bool = True
    """
    Controls whether the "bare headers" will be taken into account when the plugin collects
    identifiers from the documentation.
    <br>Note that both options have their advantages and disadvantages. For more details, see the
    section about [handling automatic mkdocs headers](--identifiers-handling-headers).

    In essence:

    * `ignore_auto_headers=true` (recommended):

        The same titles can be used in different locations, but headers must be explicitly marked
        with ids for the plugin to gather them.

        ```markdown
        ## Content
        ... is ignored

        ## Content
        ... is also ignored, hence, no error raised

        ## Content {: #hey-there }
        ... is gathered as --hey-there

        ### Hall of fame! {: #hall-of-fame }
        This example would result in a false negative and be ignored,
        because the id would be considered identical to the content.
        ```


    * `ignore_auto_headers=false`:

        In this case, all headers must be unique or have an id attribute (or
        [configured as ignored](--auto-headers-false)), otherwise a
        [`DuplicateIdentifierError`](--mkdocs_addresses_exceptions_DuplicateIdentifierError)
        is raised.

        ```markdown
        ## Content
        ... is gathered

        #### Content
        ... this one would raises DuplicateIdentifierError

        ## Content {: #precedence-over-content }
        ...this title wouldn't raise, because its id will be used instead
        ```
    """


    ignored_classes: List[str] = []
    """
    If defined, each string represent an html class name that will be ignored when collecting
    the identifiers and checks the addresses. Example of definition:

    ```yaml
    plugins:
        - mkdocs-addresses:
            ignored_classes:        # or: ignored_classes: ["class-name-1", "non-gathered"]
                - class-name-1
                - non-gathered
    ```

    !!! tip
        The class "headerlink" will systematically be excluded. This allows the plugin to ignore
        the permalinks generated by the [`toc`][toc]{: target=_blank } markdown extension.
    """

    skip_identifiers_definitions_in_pages: List[str] = []
    """
    List of uri strings, relative to the docs, of pages where identifiers definitions won't
    be gathered.

    May also be a `#!py Path.glob` uri pattern. Patterns are identified as such when the
    `#!py "*"` character is used in them.

    Constraints:
    - Patterns have to be written relative to the docs_dir
    - Patterns are not recursive by default, but can be when using `#!py "**"` in them (keep in
    mind this means "0 or more", with `Path.glob`)
    - Patterns have to specifically target the md file, so they have to end with `#!py "*.md"`.
    """


    ignored_identifiers_or_addresses: List[str] = []
    """
    If defined, each string represents an html id or a plugin identifier or an address (`<a href>`,
    or `<img src>` attributes) that will be ignored when the plugin collects and checks identifiers
    or addresses.
    Example of definition:

    ```yaml
    plugins:
        - mkdocs-addresses:
            ignored_identifiers_or_addresses:
                - subtitle
                - skip-this-id
                - --skip-this-also
                - ../meta/invalid/skipped.anyway
    ```

    !!! tip
        Ids starting with double underscores will always be ignored, because some plugins create
        and utilize them to mark some tags for their internal logic.
    """


    imgs_extension_pattern: str = "(?i)\\.(jpg|jpeg|bmp|png|svg)$"
    """
    Regex pattern used to identify files that are images, using
    [`re.search`](https://docs.python.org/3/library/re.html#re.search){: target=_blank }.
    """


    inclusions: List[str] = []
    """
    Slash separated paths, relative to the cwd, that point to directories containing files
    to be included using the "scissors" operator: `--<8--` (requires the `pymdownx.snippets`
    markdown extension).

    More information about the resulting code snippets in the [autocompletion section](--inclusions-snippets).

    !!! note
        The directories specified under `inclusions` are not supposed to be in the `docs_dir`.
        If they are, mkdocs will generate warnings about files not included in the nav.
    """


    # inclusions_with_root: bool = False
    # """
    # Define if the parent inclusion directory will be part of the code snippet identifier.

    # This is to prevent potential conflicts of  snippets identifiers when several inclusions
    # directories are used. See details in the [autocompletion section](--inclusions-snippets).
    # """


    more_verbose: bool = False
    """
    Controls the verbosity level of the plugin. It set to `true`, the verbosity is slightly
    increased, without affecting the level of verbosity of the mkdocs logger.

    If mkdocs is run in verbose mode (using `mkdocs serve -v`), this option is ignored and
    the verbosity of the plugin's logger is also set to DEBUG level.
    """


    plugin_off: bool = False
    """
    If true, completely deactivates the plugin.

    This may speed up the serve steps, but the whole verification logic of the plugin will be lost.
    """


    strict_anchor_check: bool = True
    """
    During anchors validations, when `strict_anchor_check` is set to true, an anchor has to match
    an identifier to be considered valid.
    If set to false, the plugin will no longer raise errors regarding unknown anchors. Instead,
    it will display a warning in the console.

    !!!note "Rationale"
        Users are encouraged to use the plugin's identifiers but:

        1. They could use bare anchors to write links within the current document.
        1. They could have added the plugin to an old project which utilizes the "old-fashion"
           addresses (`../a/b/c.md`).

        By essence, neither of these situations is problematic but, when
        [`ignore_auto_headers`][mkdocs_addresses.config_plugin.PluginOptions.ignore_auto_headers]
        is set to true (which is the default value...), the plugin cannot know anymore about the
        automatic headers and will assume the anchor is wrong if it doesn't match any of its
        registered identifiers.

        This behavior can be turned off by setting `strict_anchor_check` to false. However, keep
        in mind this is discouraged because doing so significantly reduces the level of
        assurance the plugin can provide regarding the correctness of all the addresses within
        the documentation.

        In summary:

        * Setting `strict_anchor_check` to false is not recommended, as it diminishes the
          reliability of the plugin's verifications.
        * But it might be useful to facilitate the integration of the plugin into older projects.
    """

    # LEGACY:
    use_vsc: Union[bool,None] = None
    # """
    # Controls the kind of file the plugin will generate with all the collected identifiers.

    # * If true, a VSC `.code-snippets` file will be created, enabling autocompletion features.
    #   This file is located at the value specified for the
    #   [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file]
    #   option.
    # * If false, the plugin overall behavior remains unchanged, but a simple `.txt` file is
    #   generated instead, containing the identifiers and the related targeted address.

    # Note:
    #     Remember that this option determines the kind of file used for the
    #     [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file]
    #     option. This means that if you assigned a filename to that option, its extension has
    #     to match with the chosen value for `use_vsc` (see the
    #     [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file]
    #     section above).
    # """


    verify_only: List[str] = []
    """
    Each entry denotes the location of the only files (slash separated, and relative to the
    _^^`docs_dir`^^_) that will be validated by the plugin. All other operations proceed as usual.

    If the list remains empty, the plugin validates all markdown files within the `docs_dir`.

     For example, to solely validate the `docs/subdir/blabla.md` file, use:
    ```yaml
    plugins:
        - mkdocs-addresses:
            verify_only:
                - subdir/blabla.md
    ```
    """


CONFIG_ANNOTATIONS = set(PluginOptions.__annotations__) - { "dump_file_vsc", "dump_file_txt" }






DUMP_OPTIONS = tuple('normal only none'.split())
NORMAL, DUMP_ONLY, NO_DUMP = DUMP_OPTIONS
assert PluginOptions.dump_action in DUMP_OPTIONS, "Invalid plugin setup"




# Config types definitions...:

ConfigErrors   = List[Tuple[str,bool,str,Optional[Exception]]]
ConfigWarnings = List[Tuple[str,str]]
FatalCbk       = Callable





class AddressAddressesConfig(Config):

    activate_cache = C.Type(bool, default=PluginOptions.activate_cache)

    dump_action = C.Choice(DUMP_OPTIONS, default=PluginOptions.dump_action)

    dump_snippets_file = C.Type(str, default='')      # Automatically overridden at validation time

    external_links_file = C.Type(str, default=PluginOptions.external_links_file)

    fail_fast = C.Type(bool, default=PluginOptions.fail_fast)

    ide = C.Choice(IDE_OPTIONS, default=PluginOptions.ide)

    imgs_extension_pattern = C.Type(str, default=PluginOptions.imgs_extension_pattern)

    ignore_auto_headers = C.Type(bool, default=PluginOptions.ignore_auto_headers)

    skip_identifiers_definitions_in_pages = C.ListOfItems(C.Type(str), default=PluginOptions.skip_identifiers_definitions_in_pages)

    ignored_identifiers_or_addresses = C.ListOfItems(C.Type(str), default=PluginOptions.ignored_identifiers_or_addresses)

    ignored_classes = C.ListOfItems(C.Type(str), default=PluginOptions.ignored_classes)

    inclusions = C.ListOfItems(C.Type(str), default=PluginOptions.inclusions)

    # inclusions_with_root = C.Type(bool, default=PluginOptions.inclusions_with_root)

    black_list_pattern = C.Type(str, default=PluginOptions.black_list_pattern)

    black_listed_patterns = C.ListOfItems(C.Type(str), default=PluginOptions.black_listed_patterns)

    more_verbose = C.Type(bool, default=PluginOptions.more_verbose)

    plugin_off = C.Type(bool, default=PluginOptions.plugin_off)

    strict_anchor_check = C.Type(bool, default=PluginOptions.strict_anchor_check)

    # LEGACY:
    use_vsc = C.Optional(C.Choice((True,False,None), default=PluginOptions.use_vsc))

    verify_only = C.ListOfItems(C.File(exists=True), default=PluginOptions.verify_only)

#TypeError: AddressAddressesConfig.use_vsc: Setting 'required' is unsupported in class-based configs. All values are required, or can be wrapped into config_options.Optional

    #----------------------------------------------
    def _validate(self):
        return super()._validate()

    def _pre_validate(self):
        return super()._pre_validate()

    def _post_validate(self):
        return super()._post_validate()


    def validate_and_process(self, config:MkDocsConfig):
        """ Performs the basic, then extras validations on each property, and also apply the
            post conversions to the data structures that need it.
            Add on the fly the needed fields from the mkdocs config.
        """
        # Enforce no unexpected option name (because this is boring AF...)
        if 'plugins' in config and 'mkdocs-addresses' in config.plugins:
            settings = set(config.plugins['mkdocs-addresses'].config)
            base_settings = set(dir(config.plugins['mkdocs-addresses'].__class__.mro()[1]))
            user_settings = settings - base_settings
        else:
            # when testing in mkdocs-addresses, the plugin isn't in the yml file (must change
            # that: see use of entry-points in pyodide-mkdocs-theme):
            user_settings = set(self.user_configs[-1])

        nope = user_settings - CONFIG_ANNOTATIONS
        if nope:
            nope    = ''.join( '\n   '+key for key in sorted(nope))
            options = ''.join( '\n   '+key for key in sorted(CONFIG_ANNOTATIONS))
            raise AddresserConfigError(
                f"Unexpected option(s) name(s):{ nope }\n\n Available options are:{options}"
            )

        # Extract completion handler class, handling use_vsc, ide and dump_snippets_file defaults
        # (no validation):
        completion_class = validate_config_and_get_auto_completion_handler(self)


        # Perform "~~post"~~" PRE-conversions:       (yeah, "post"... lol...)
        #-------------------------------------

        maybe_abs = path_manager.to_os(config['docs_dir'])
        self.uni_docs_dir = maybe_abs.absolute().relative_to(Path.cwd())

        for prop in 'docs_dir  use_directory_urls'.split():
            setattr(self, prop, config[prop])

        self.black_list_pattern = "|".join(
            [self.black_list_pattern] + self.black_listed_patterns
        ).strip('|')

        post_conversions: List[Tuple[Callable[[str],Any], str]] = [
            (re.compile, 'imgs_extension_pattern  black_list_pattern'),
            (set,        'ignored_identifiers_or_addresses ignored_classes verify_only inclusions skip_identifiers_definitions_in_pages'),
        ]
        for conversion,props in post_conversions:
            for prop in props.split():
                value = getattr(self, prop)
                try:
                    post = conversion(value)
                    setattr(self, prop, post)
                except Exception as e:                              # pylint: disable=all
                    e.args = ( f"{ prop }: { e.args[0] }",)
                    raise

        self.ignored_classes.add('headerlink')      # this avoids to consider mkdocs permalinks in headers, when used

        # More specific validations and post conversions:
        #------------------------------------------------

        self._validate_inclusions_dir()
        self._validate_black_list_pattern()
        self._validate_external_links_file()
        self._validate_verify_only_md_files()
        self._validate_verify_only_md_files()
        self._resolve_patterns_and_validate_skip_identifiers_definitions_in_pages()
        self._validate_auto_completion_config(completion_class)
        self._validate_dump_extension_vs_ide(completion_class)

        return completion_class


    #----------------------------------------------


    def _check_not_in_docs(self, prop:str, path:Union[str,Path]):
        rel = os.path.relpath(path, self.uni_docs_dir)
        if not rel.startswith('..'):
            raise AddresserConfigError(
                f"{prop}: {path!r} should not be inside the docs_dir directory"
            )


    #----------------------------------------------


    def _validate_inclusions_dir(self):
        self.inclusions = sorted(map( path_manager.to_os, self.inclusions))
        oops = [location for location in self.inclusions if not location.is_dir() ]
        if oops:
            raise AddresserConfigError(
                f"'inclusions' should be a list of directories, but found invalid paths: ({ oops !r})"
            )

        for path in self.inclusions:
            self._check_not_in_docs('inclusions', path)



    def _validate_black_list_pattern(self):
        if not self.black_list_pattern.pattern:      # this is now a pattern, not a string anymore!
            raise AddresserConfigError(
                "black_list_pattern should never be an empty string. Note that not using at "
                "least the default pattern will definitely cause problems..."
            )



    def _validate_external_links_file(self):
        if not self.external_links_file:
            return

        self.external_links_file = p = path_manager.to_os(self.external_links_file)
        if not p.is_file() or not p.suffix=='.md':
            raise AddresserConfigError(
                "'external_links_file' is configured, but is not an existing markdown file "
                f'("{ self.external_links_file }")'
            )
        self._check_not_in_docs('external_links_file', self.external_links_file)



    def _validate_auto_completion_config(self, completion_class:Type[AutoCompletion]):
        self.dump_snippets_file = path_manager.to_os(self.dump_snippets_file)
        self._check_not_in_docs('dump_snippets_file', self.dump_snippets_file)


    def _validate_dump_extension_vs_ide(self, completion_class:Type[AutoCompletion]):
        # Note: separated from _validate_auto_completion_config for testing purpose.
        needed_suffix:str = path_manager.to_os(completion_class.filename).suffix
        if self.dump_snippets_file.suffix != needed_suffix:
            raise AddresserConfigError(
                "Inconsistent configuration:\n"
                f"   ide: {self.ide}\n"
                f"   dump_snippets_file: {self.dump_snippets_file}"
            )



    def _validate_verify_only_md_files(self):
        invalids = [ file for file in self.verify_only
                          if not path_manager.to_os(file).suffix=='.md']
        if invalids:
            raise AddresserConfigError(
                "All options for `verify_only` should be valid markdown files, relative to the cwd.\n"
                +"Invalid entries:" + "".join('\n    '+file for file in invalids)
            )

    def _resolve_patterns_and_validate_skip_identifiers_definitions_in_pages(self):

        # Handle patterns:
        patterns = {p for p in self.skip_identifiers_definitions_in_pages if "*" in p}
        self.skip_identifiers_definitions_in_pages -= patterns

        # Validate all files:
        invalids = [
            file for file in map(Path, self.skip_identifiers_definitions_in_pages)
                 if not ('docs' / file).is_file()
        ]
        if invalids:
            raise AddresserConfigError(
                "The following files do not exist, relative to the docs_dir:"
                +"".join(f'\n    { file.as_posix() }' for file in invalids)
            )
        # Validate patterns:
        invalid_patterns = [
            p for p in patterns if not p.endswith("*.md")
        ]
        if invalid_patterns:
            raise AddresserConfigError(
                "The following patterns are not valid: patterns have to end with '*.md'."
                +"".join(f'\n    {p}' for p in invalid_patterns)
            )

        logger.info('Pages exclusions patterns applied:' + ''.join(f"\n    - {p!r}" for p in patterns))

        # Add md files found from pattern matching (non recursive by default. Use "**" if needed)
        from_patterns: List[str] = []
        docs = Path('docs')
        for pattern in patterns:
            for file in docs.glob(pattern):
                if file.suffix == '.md':
                    as_posix = file.as_posix()
                    from_patterns.append(as_posix)

        # Rebuild the actual content needed (string uri, without "docs/" to match
        # against page.file.src_uri):
        skip_docs_slash = len('docs/')
        self.skip_identifiers_definitions_in_pages.update(
            file[skip_docs_slash:] for file in from_patterns
        )











class ConfigDescriptor:
    """ Dynamic relay data descriptor, to articulate the plugin and its configuration """

    prop: str

    def __set_name__(self, _, prop:str):
        self.prop = prop

    def __get__(self, obj:'AddressAddressesPlugin', _:type):
        return getattr(obj.config, self.prop)

    def __set__(self, obj:'AddressAddressesPlugin', value:Any):
        # setter needed to make this a data descriptor, but should never be used.
        raise InvalidOperationError(
            "Config properties should never be reassigned from the plugin instance."
        )








def __check_config_annotations_consistency():
    """
    Verification that no option of PluginOptions has been forgotten in AddressAddressesConfig:
    """
    implemented = set(AddressAddressesConfig.__annotations__) - {
        "_schema",                  # inherited
        "config_file_path",         # inherited
    }
    missing = implemented - CONFIG_ANNOTATIONS
    assert not missing, f"Not implemented: { ', '.join(missing) }"

__check_config_annotations_consistency()
