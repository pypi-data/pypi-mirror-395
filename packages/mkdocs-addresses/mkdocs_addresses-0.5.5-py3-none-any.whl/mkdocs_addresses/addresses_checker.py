# pylint: disable=unused-private-member

import os

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any
from enum import IntEnum, auto

from mkdocs.structure.pages import Page

from mkdocs_addresses import path_manager
from mkdocs_addresses.auto_completion_handler import RefKind, AutoCompletion
from mkdocs_addresses.logger import logger


from .exceptions import (
    AbstractAddressError,
    AnchorNotInPageError,
    AnchorUnknownError,
    EmptyAnchorError,
    ImageWithAnchorError,
    MarkdownLinkError,
    NoMoveUpDirOnNonIndexPageUrlsAsDirAddressError,
    NonRelativeAddressError,
    NotAnImageAddressError,
    NotAFileAddressError,
    TooManyAnchorsError,
    TrailingSlashAddressError,
)

if TYPE_CHECKING:
    from .addresses_plugin import AddressAddressesPlugin





class AddressKind(IntEnum):
    """ Enum representing the different kind of attribute/addresses that will be
        handled through the plugin.
    """
    HREF = auto()       # <a href=...> => link
    SRC  = auto()       # <img src=.../> => img




@dataclass
class AddressChecker:
    """
    Class centralizing the logic to check the validity of various urls in the final html pages
    """

    plugin:     'AddressAddressesPlugin' # Plugin instance...
    page:        Page                    # Page from where the link address is used
    address:     str                     # The address to validate, as shown in the html code
    kind:        AddressKind             # Identify the context in which the address is used
    #-----------------------------
    # auto-computed in post init:
    has_trailing_slash: bool = field(init=False)      # True if the address ends with '/'
    is_html_file:bool        = field(init=False)      # True if the address ends with '.html(#...)?'
    caller_dir:  str         = field(init=False)      # Current (relative) directory containing the source file
    src_address: str         = field(init=False)      # Debugging purpose
    univ_address:Path        = field(init=False)      # OS dependent version of the given address to validate
    full_address:Path        = field(init=False)      # OS dependent version of the real path of the address
    anchor:      str         = field(init=False)      # Any anchor spotted in the address


    def __post_init__(self):
        self.src_address  = self.address        # archive for debugging purpose

        # Prevent little jokes... (and may become useful for "wrongish use" of mkdocstrings...)
        if self.address.startswith('./#'):
            self.address = self.address[2:]


        self.__validate_hashtag_and_reassign_address_and_anchor(self.address)
        if self.address is None:
            # Actually found a bare anchor (yeah, not obvious, I know...)
            return

        self.has_trailing_slash = self.address.endswith('/')
        self.is_html_file       = self.address.endswith('.html')
        self.caller_dir         = os.path.dirname(self.page.file.src_path)


        if self.plugin.use_directory_urls and not self.page.file.src_uri.endswith('index.md'):
            # NOTE: bare anchors have already been handled (see above) and are not subject to
            #       use this branch of logic.
            # The paths are "computed" according to the final built site, but when checking
            # validity of the addresses, the concrete dev version must be used.
            # This introduces a discrepancy when use_directory_urls is true and the current
            # file is not an index.md file: the current file will be converted to a directory
            # containing its own index.html file. This extra layer is "included" in the logic
            # building the relative paths, which means all relative paths from a "non index.md"
            # file will generate an extra `../` that must be removed, before checking the
            # address.
            # This is done by removing one leading dot, which allow to keep the consistency for
            # the checks about "a valid link should be relative, hence start with a dot" done
            # later in the code.

            self.__fatal_if(
                not self.address.startswith('../'),         # security check (used in the tests)
                "Address from a non index.md file should always have in a leading '../' but got: "
                f"{ self.src_address !r}",
                NoMoveUpDirOnNonIndexPageUrlsAsDirAddressError
            )
            # Remove one leading dot to match the actual tree hierarchy at build time:
            self.address = self.address[1:]

        self.univ_address = path_manager.to_os(self.address)
        full_address      = self.plugin.uni_docs_dir / self.caller_dir / self.univ_address
        self.full_address = path_manager.to_os(os.path.realpath(full_address))
            # WARNING: the above shenanigan (Path -> os -> Path) is needed because on Windows,
            # Path.resolve may fail if an url reaches this code (if it's not ignored)



    def __validate_hashtag_and_reassign_address_and_anchor(self, address:str):

        # Addresses for img.src stay unchanged (just check no anchors are in there...)
        if self.kind == AddressKind.SRC:
            self.__fatal_if(
                '#' in address, "img.src address should never contain '#'",
                ImageWithAnchorError,
            )
            self.address = address

        # Handle direct links to anchors in the current file itself:
        elif address.startswith('#'):
            self.__validate_anchor(address[1:], True)
            self.address = None         # will indicate that the address is actually valid  # type: ignore

        else:
            # Handle possible trailing anchor:
            lst = address.split('#')
            if len(lst)==2:
                self.address, self.anchor = lst
                self.__fatal_if(
                    not self.anchor,
                    f"Invalid link: Empty anchor identifier: { address !r}",
                    EmptyAnchorError,
                )
                self.__validate_anchor(self.anchor, False)

            self.__fatal_if(
                len(lst)>2,
                f"Invalid link: contains more than one anchor: { address !r}",
                TooManyAnchorsError,
            )


    def __str__(self):
        return f"""AddressChecker data:
    { self.page.file.src_uri =}
    { self.page.url =}
    { self.caller_dir =}
    { self.src_address =}
    { self.has_trailing_slash =}
    { self.is_html_file =}
    { self.address =}
    { self.univ_address =}
    { self.full_address =}
    cwd = { os.getcwd() }
"""


    @classmethod
    def check(cls, plugin:'AddressAddressesPlugin', page:Page, address:str, kind:AddressKind):
        """
        Entry point, providing all the needed data, then defining the validations to do and
        performing them.

        WARNING:
            It's important to keep in mind that, at this point, the addresses in the html
            are all written in a relative way, hance might be like "../../assets/...)".
            It's only in the built site that they are shown as "resolved"/absolute.

        @throws: AddresserError, subclasses of AddresserError, NotAFileAddressError.
        """

        checker = cls(plugin, page, address, kind)     # see __post_init__ validations...

        if checker.address is None:
            return     # valid bare hashtag identifier, kind cannot be IMG, here.

        is_not_relative = not checker.address.startswith('.')
        checker.__fatal_if(
            is_not_relative,
            f"{ checker.address !r} should be relative path (starting with at least one dot)",
            NonRelativeAddressError,
        )

        is_md = checker.full_address.suffix == '.md'
        checker.__fatal_if(
            is_md,
            "Links to markdown files should never be used in the final documentation. "
            "If this is intended, mark this address as ignored in the plugins configuration.",
            MarkdownLinkError
        )

        # Pick the validation logic to use:
        if checker.kind == AddressKind.SRC:
            checker.__validate_img_src_attr()

        elif checker.plugin.use_directory_urls:
            checker.__validate_with_docs_as_dirs()

        else:
            checker.__validate_with_docs_as_html()



    def __validate_anchor(self, anchor:str, is_bare):

        completer  = AutoCompletion.get_for(RefKind.Link)
        identifier = completer.get_final_identifier(anchor)
        references = self.plugin.global_handler.references
        unknown_id = not references.has_id(identifier)

        # The id should always exist, except in one case: if ignore_auto_headers is true, the user
        # might be pointing at one of the unregistered anchors... In that case, and if the user
        # didn't ask for a strict check of anchors, just issue a warning in the console.
        if unknown_id and self.plugin.ignore_auto_headers and not self.plugin.strict_anchor_check:
            logger.warning(
                "An anchor that doesn't match any identifier has been found while "
                "ignore_auto_headers is set to true: there is no way to know if this anchor is "
                "valid or not:\n"
                f"    File: { self.page.file.src_uri }\n"
                f"    Address: { self.full_address }"
            )
            return

        self.__fatal_if(
            unknown_id,
            f'Unknown anchor: "#{ anchor }"',
            AnchorUnknownError
        )

        not_in_page = not references.is_identifier_in_source(identifier, self.page)
        self.__fatal_if(
            is_bare and not_in_page,
            f'Anchor: "#{ anchor }" is not defined in the current page',
            AnchorNotInPageError
        )



    def __validate_img_src_attr(self):
        is_file = self.full_address.is_file()     # check first (testing purpose)
        self.__fatal_if(
            not is_file,
            f"{ self.full_address !r}",
            NotAFileAddressError
        )
        is_img  = self.plugin.imgs_extension_pattern.search(self.full_address.name)
        self.__fatal_if(
            not is_img,
            f"{ self.full_address !r} is not identified as an image",
            NotAnImageAddressError
        )



    def __validate_with_docs_as_dirs(self):
        # (note: anchors (if any) have already been validated)

        is_file         = self.full_address.is_file()
        actually_dir    = self.full_address.is_dir()

        maybe_doc_file  = self.full_address.parent / (self.full_address.stem + '.md')
        actually_doc_md = maybe_doc_file.is_file()

        maybe_index     = self.full_address / 'index.md'
        actually_index  = maybe_index.is_file()

        if not self.has_trailing_slash:
            # HAS to be an existing file, then:
            self.__fatal_if(not is_file, self.full_address, exc=NotAFileAddressError)

        elif actually_dir:
            # If it's a directory, this one has to contain a index.md file
            self.__fatal_if(
                not actually_index,
                f"{ maybe_index } should not point to an actual directory. If this is intended, "
                "mark this address as ignored",
                exc=NotAFileAddressError
            )

        else:
            self.__fatal_if(not actually_doc_md, maybe_doc_file, exc=NotAFileAddressError)



    def __validate_with_docs_as_html(self):
        # (note: anchors (if any) have already been validated)

        is_dir  = self.full_address.is_dir()
        is_file = self.full_address.is_file()

        # Forbid pointing to an actual directory in "html mode":
        self.__fatal_if(
            is_dir or self.has_trailing_slash,
            f"{self.full_address!r} address is not supposed to be a directory, if mkdocs "
            "use_directories_url is false. If it's intended, mark this address as ignored.",
            TrailingSlashAddressError if self.has_trailing_slash else NotAFileAddressError
        )

        if not is_file:
            # If the address points to a "currently non existent file" on the disk, while the
            # address is an html one, the address is always wrong:
            self.__fatal_if(not self.is_html_file, self.full_address, NotAFileAddressError)

            # If the uri points to an html file and that file has not been actually found, it HAS
            # to be a markdown documentation file:
            maybe_doc_file = self.full_address.parent / (self.full_address.stem + '.md')
            is_md          = maybe_doc_file.is_file()
            self.__fatal_if(not is_md, maybe_doc_file, NotAFileAddressError)





    def __fatal_if(self, truthy, msg:Any, exc=AbstractAddressError):
        if truthy:
            tail = f'\n(Source address: {self.src_address!r} in file {self.page.file.src_uri!r})'
            raise exc(str(msg) + tail)
