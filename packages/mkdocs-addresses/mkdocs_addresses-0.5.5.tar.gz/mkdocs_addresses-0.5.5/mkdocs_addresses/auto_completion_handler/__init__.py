

from typing import Dict, Literal, Tuple, Type, TYPE_CHECKING

from ._base_handler import RefKind, AutoCompletion, PLUGIN_MARK
from ._vsc_handlers import VscAutoAddress, VscAutoInclude, VscAutoCompletion
from ._no_completion_handler import NoAutoAddress, NoAutoInclude, NoAutoCompletion

if TYPE_CHECKING:
    from mkdocs_addresses.config_plugin import AddressAddressesConfig




IdeKind     = Literal['none','vsc']
NONE,VSC    = 'none','vsc'
IDE_OPTIONS = NONE,VSC


COMPLETION_CLASSES_CONFIG: Dict[IdeKind,Tuple[Type[AutoCompletion],...]]= {
    NONE: (NoAutoCompletion, NoAutoAddress, NoAutoInclude),           # by default...
    VSC:  (VscAutoCompletion, VscAutoAddress, VscAutoInclude),
}



def validate_config_and_get_auto_completion_handler(config:'AddressAddressesConfig') -> Type[AutoCompletion]:
    """
    Build the AutoCompletion instances, for the given type of IDE
    """

    # Handle legacy option
    if config.use_vsc is not None:
        config.ide = VSC if config.use_vsc else NONE
        config.use_vsc = None

    TopKls, KlsAddress, KlsInclude = COMPLETION_CLASSES_CONFIG[config.ide]
    if not config.dump_snippets_file:
        config.dump_snippets_file = TopKls.filename

    handlers = {
        formatter.kind: formatter for formatter in [
            KlsInclude( RefKind.Include, '::'),                     # code inclusions
            KlsAddress( RefKind.Link,    '--'),                     # internal links
            KlsAddress( RefKind.File,    '++'),                     # any internal file
            KlsAddress( RefKind.Img,     '!!', snippet_start='!'),  # images
            KlsAddress( RefKind.Ext,      '', tail_wrap=('[',']'),  # External links
                                              attrs="target=_blank"),
    ]}
    TopKls.setup_handlers(handlers)
    return TopKls
