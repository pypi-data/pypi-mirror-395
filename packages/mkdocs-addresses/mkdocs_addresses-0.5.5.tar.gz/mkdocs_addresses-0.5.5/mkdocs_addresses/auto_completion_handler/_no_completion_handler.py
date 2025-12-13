


from typing import ClassVar, Dict, TYPE_CHECKING
from dataclasses import dataclass

from mkdocs_addresses.toolbox import plugin_dump_padder
from ._vsc_handlers import VscAutoCompletion, VscAutoAddress, VscAutoInclude

if TYPE_CHECKING:
    from mkdocs_addresses.addresses_plugin import AddressAddressesPlugin




@dataclass
class NoAutoCompletion(VscAutoCompletion):
    """ Keep building the snippets/logic, but  """

    filename: ClassVar[str] = 'addresses_identifiers.txt'



    @classmethod
    def build_snippets_code(cls, plugin:'AddressAddressesPlugin'=None, as_json=False):
        if plugin is not None:
            data = plugin.global_handler.references.gen_refs_items()
        else:
            data = ()
        if as_json:
            code = "{" + "".join( f"{ plugin_dump_padder(identifier+':') } { file } \n"
                                    for identifier,file in sorted(data) ) + '}'
        else:
            code = "Identifier | Target\n--------------------\n\n" \
                + "".join( f"{ plugin_dump_padder(identifier+':') } { file } \n"
                            for identifier,file in sorted(data) )
        return code





@dataclass
class NoAutoAddress(VscAutoAddress): pass

@dataclass
class NoAutoInclude(VscAutoInclude): pass
