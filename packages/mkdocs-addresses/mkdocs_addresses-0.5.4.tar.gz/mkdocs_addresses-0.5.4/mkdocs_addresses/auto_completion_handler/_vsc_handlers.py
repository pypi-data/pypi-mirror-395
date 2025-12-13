import os
import json
from textwrap import dedent
from dataclasses import dataclass
from typing import ClassVar, Dict, TYPE_CHECKING

from ._base_handler import AutoCompletion, RefKind, OPEN, CLOSE, SNIPPETS_TARGET, PLUGIN_MARK


if TYPE_CHECKING:
    from mkdocs_addresses.addresses_plugin import AddressAddressesPlugin






@dataclass
class VscAutoCompletion(AutoCompletion):

    filename: ClassVar[str] = '.vscode/links.code-snippets'


    @classmethod
    def store_other_snippets(cls, data:str):
        """ Extract some possible snippets unrelated to the plugin, if any, receiving the data as
            a bare string.
        """
        json_as_dict = json.loads(data).items()
        cls.other_snippets.extend(
            cls.build_other_snippet(name, d)
                for name,d in json_as_dict
                if 'description' not in d or PLUGIN_MARK not in d['description']
        )


    @classmethod
    def build_snippets_code(cls, plugin:'AddressAddressesPlugin'=None, _=True):
        if plugin is not None:
            data = (*cls.other_snippets, *plugin.global_handler.references.snippets.values())
        else:
            data = cls.other_snippets
        code = "{\n" + ",\n".join(sorted(data)) + "\n}"
        return code


    @classmethod
    def build_other_snippet(cls, name:str, dct:Dict):
        item = f'"{name}": { json.dumps(dct, indent=4) }'
        return item





@dataclass
class VscAutoAddress(VscAutoCompletion):
    """ Build snippets for links, ids, extras, files, images """


    def get_final_identifier(self, identifier:str, with_head=True):

        assets = 'assets/'
        if identifier.startswith(assets):
            identifier = identifier[len(assets):]
        return with_head * self.head + identifier.replace('.','_')


    def build_snippet(self, identifier, src_link, **_):

        clean_id = self.get_final_identifier(identifier, False)
        prefix   = f"{ self.kind.name }.{ clean_id }"       # Img.identifier or so...
        body     = self.__build_body(clean_id)
        yield self._build_snippet(prefix, body, src_link, "Md")

        if self.with_short:
            prefix = self.head + clean_id                   # !!identifier or so...
            body   = f"${ OPEN }0:{ self.head }{ CLOSE }{ clean_id }"
            yield self._build_snippet(prefix, body, src_link, "Reference")


    def __build_body(self, clean_id:str):
        """ helper... """
        L,R     = self.tail_wrap
        content = self._get_content(clean_id)
        body    = self.snippet_start + "[${0:" + content + "}]" + f"{ L }{ self.head }{ clean_id }{ R }"
        if self.attrs:
            body += "{: " + self.attrs + " }"
        return body


    def _get_content(self, clean_id:str):
        if self.kind == RefKind.Ext:
            return clean_id
        return 'content'


    def _build_snippet(self, prefix:str, body:str, src_link:str, name_prefix=''):
        if name_prefix:
            name_prefix += " - "
        json_id = f"{ name_prefix }{ self.kind.name }: { src_link !r}"
        return json_id, dedent(f"""\
            "{ json_id }": { OPEN }
                "prefix": "{ prefix }",
                "scope": { SNIPPETS_TARGET },
                "body": ["{ body }"],
                "description": "{ PLUGIN_MARK }"
            { CLOSE }""")






@dataclass
class VscAutoInclude(VscAutoAddress):
    """ Build snippets for markdown code inclusions (ie: "--8<--" ) """


    # pylint: disable-next=arguments-differ
    def build_snippet(self, identifier:str, src_link:str, *, root_inclusion:str): #, inclusions_with_root:bool):
        # root_inclusion: one of the path s given in plugin.inclusions (as uri)

        #i_truncate = len(root_inclusion)+(not inclusions_with_root)   # Extra slash to account for
        i_truncate = len(root_inclusion) + 1   # extra slash to account for
        _, ext     = os.path.splitext(identifier)
        short_uri  = identifier[i_truncate:]
        body       = f'--8<-- \\"{ identifier }\\"'
        prefix     = f"{ self.head }{ ext.strip('.') } { short_uri }"
        snippet    = self._build_snippet(prefix, body, identifier)
        yield snippet
