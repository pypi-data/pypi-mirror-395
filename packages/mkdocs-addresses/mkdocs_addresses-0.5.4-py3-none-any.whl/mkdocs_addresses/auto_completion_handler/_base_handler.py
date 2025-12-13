import re

from typing import ClassVar, Dict, List, Tuple, TYPE_CHECKING
from enum import auto, IntEnum
from dataclasses import dataclass, field


if TYPE_CHECKING:
    from mkdocs_addresses.addresses_plugin import AddressAddressesPlugin







PLUGIN_MARK = "VSC-REF"

OPEN, CLOSE = '{', '}'

SNIPPETS_TARGET = '"markdown"'



class RefKind(IntEnum):
    Link = auto()
    File = auto()
    Img  = auto()
    Ext  = auto()
    Include = auto()





@dataclass
class AutoCompletion:
    """
    An AutoCompletion instance holds the whole logic to build individual code snippets as
    strings, for a given kind of data.
    """

    kind: RefKind               # Snippet type
    head: str                   # Prefix identifier (used to spot them in the html code)

    snippet_start: str = ''     # Element coming before the "[...]" initial part
    tail_wrap: Tuple[str,str] = '(',')'     # open+close for the last section (after "[...]")
    with_short: bool = True     # Also generate the short snippet version (head+identifier only)
    attrs: str = ""             # string of attributes to always add at the end of the body


    filename: ClassVar[str]     # Default dump file location (CwdPath)

    other_snippets: ClassVar[List[str]] = []
                                # Store all existing snippet unrelated to the plugin (if any)


    @classmethod
    def setup_handlers(cls, handlers:Dict[RefKind,'AutoCompletion']):
        AutoCompletion.__LINK_BUILDER          = handlers
        AutoCompletion.__POTENTIAL_REF_PATTERN = re.compile(
            '|'.join( re.escape(o.head) for o in AutoCompletion.__LINK_BUILDER.values() if o.head)
        )


    @classmethod
    def href_is_possible_ref(cls, href):
        return cls.__POTENTIAL_REF_PATTERN.match(href)


    @classmethod
    def get_for(cls, kind:RefKind) -> 'AutoCompletion':
        return cls.__LINK_BUILDER[kind]


    @classmethod
    def clear_other_snippets(cls):
        """ Clear the content of the snippets unrelated to the plugin """
        cls.other_snippets.clear()


    @classmethod
    def store_other_snippets(cls, data:str):
        """ Extract some possible snippets unrelated to the plugin, if any, receiving the data as
            a bare string.
        """
        raise NotImplementedError("Subclasses must override this method")


    @classmethod
    def build_snippets_code(cls, plugin:'AddressAddressesPlugin'=None, as_json=True):
        """ Rebuild the full snippets/identifiers data as a string, combining the "other_snippets"
            with the data coming from the References.
        """
        raise NotImplementedError("Subclasses must override this method")


    @classmethod
    def build_other_snippet(cls, name:str, dct:Dict):
        """ Build one snippet string for the snippets unrelated to the plugin """
        raise NotImplementedError("Subclasses must override this method")


    #------------------------------------------------------------------


    def build_snippet(self, identifier, src_link, **_):
        """ Generate code snippet entries for the given (bare) identifier, pointing toward the
            given source (which will, in the end, be the targeted element).
            @identifier: the bare identifier, without the "head" part ("!!", "--", ...)
            @src_link is the path of the source, relative to the cwd ("development wise")
            Automatically add the "shorthand" version of the snippet, if the kind requires it.
        """
        raise NotImplementedError("Subclasses must override this method")


    def get_final_identifier(self, identifier:str, with_head=True):
        """ Add the "head_link" part to the identifier if needed, and format the identifier
            to avoid they generate warnings during the builds
        """
        return with_head * self.head + identifier


