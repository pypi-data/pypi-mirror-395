# pylint: disable=all

import os
from pathlib import Path
import re
import json
from textwrap import dedent
from typing import Dict, TYPE_CHECKING, Literal, Tuple, Union
from dataclasses import dataclass,field

from bs4.element import Tag
from mkdocs.structure.pages import Page

from mkdocs_addresses import path_manager



if TYPE_CHECKING:
    from .addresses_plugin import AddressAddressesPlugin




#-----------------------------------------------------------
#                  Data extraction tools
#-----------------------------------------------------------



@dataclass
class Content:
    url: str
    target: str

    def to_tests(self):
        return f'''Content(
                    url = { self.url !r},
                    target = { self.target !r},
                ),'''


@dataclass
class Location:
    file_uri: str
    html: str
    data: Tuple[Content,Content]
    md: str = '...'

    @classmethod
    def default(cls, uri:str, html:str):
        return Location(uri, html, (Content('',''), Content('','')))

    def to_json(self):
        return {
            k: getattr(self,k)
            for k in self.__class__.__annotations__     # pylint: disable=no-member
        }

    def to_tests(self):
        sep = "\n                "
        return f'''Location(
                file_uri = { self.file_uri !r},
                html = { self.html !r},
                md = { self.md !r},
                data = ({ ''.join( f"{ sep }{ ct.to_tests() }" for ct in self.data ) }),
            ),'''

@dataclass
class Chunk:
    is_bare:bool
    id:     str
    locations: Dict[str,Tuple[Location,Location]]


    def to_json(self):
        return {
            k: getattr(self,k) if k!='locations' else [
                v.to_json()
                for v in getattr(self,k).values()
            ]
            for k in self.__class__.__annotations__     # pylint: disable=no-member
        }

    def to_tests(self):
        sep = "\n            "
        return f'''\
    Chunk(
        is_bare = { self.is_bare !r},
        id = { self.id !r},
        locations = [{ ''.join( f"{ sep }{ loc.to_tests() }" for loc in self.locations.values() ) }
        ],
    ),\n'''




def dict_to_str(data:dict, name="actual"):
    """ Utility to print a dict to the console """
    return f'\n\n#{ name }:\n' + '{' + ''.join(
        f"\n\t{k!r: <30}: {v!r}," for k,v in sorted(data.items())
    ) + '\n}'


def simplify_ids(id:str):
    return re.sub(r'[ -]other|[ -]?(?<!h)2','',id)



FlowKind = Literal['refs_on_hook','html_content','start_context','end_context']


@dataclass
class LiveDataExtractor:
    """ Tool used to extract various data to build some data sets for the tests """

    dct_misc: Dict[str,Chunk] = field(default_factory=dict)     # not Flow related

    refs_on_hook:  Dict[str,str] = field(default_factory=dict)
    markdown:      Dict[str,str] = field(default_factory=dict)
    html_content:  Dict[str,str] = field(default_factory=dict)
    start_context: Dict[str,str] = field(default_factory=dict)
    end_context:   Dict[str,str] = field(default_factory=dict)


    def clear(self):
        for prop in getattr(LiveDataExtractor,'__annotations__', {}):
            data = getattr(self, prop, None)
            if hasattr(data,'clear'):
                data.clear()

    def refs_snapshot_at(self, hook:str, plugin:'AddressAddressesPlugin'):
        self.refs_on_hook[hook] = plugin.global_handler.references.id_to_data.copy()

    def add_html_and_markdown(self, page:Page, html):
        self.markdown[page.file.src_uri] = page.markdown
        self.html_content[page.file.src_uri] = html

    def add_start_ctx(self, page:Page):
        self.start_context[page.file.src_uri] = page.content

    def add_end_ctx(self, page:Page):
        self.end_context[page.file.src_uri] = page.content



    def flow_dump(self, plugin:'AddressAddressesPlugin'):
        """ To generate the data for all files:

                1. Activate the extractor code: "dev toggle"
                2. Check that everything is fine in yml ad hooks files... (!!)
                3. Set "i_flag = -1" in the mkdocs_dev_hooks.py file
                4. Run successively in the console (until all the flags have been used):
                        dev apply
                        Ctrl+C, start over...
                5. Grab the file "dump/full_flow.json"
        """
        flow     = Flow()
        flow_key = self.get_flow_key(plugin)
        kinds    = 'markdown html_content start_context end_context'.split()
        for kind in kinds:
            flow.push(kind, flow_key, getattr(self,kind))

        kind  = 'refs_on_hook'
        hooks = 'on_nav on_env on_post_build'.split()
        for hook in hooks:
            if hook in self.refs_on_hook:
                flow.push(kind, flow_key, self.refs_on_hook[hook], hook)
        flow.dump()
        self.clear()


    @classmethod
    def get_flow_key(cls, plugin:'AddressAddressesPlugin'):
        docs = plugin.docs_dir
        docs_dir = os.path.basename(docs)
        links_uri, snip_uri = (
            path_manager.to_uri(path_manager.to_os(os.path.relpath(file, docs)))
                for file in (plugin.external_links_file, plugin.dump_snippets_file)
        )
        return (
            f"cache={plugin.activate_cache}, {docs_dir}, vsc={plugin.use_auto_completion}, "
            f"no_headers={plugin.ignore_auto_headers}, { 'fail fast' if plugin.fail_fast else 'skip fail'}, "
            f"ext_links={ links_uri }, snippets_file={ snip_uri }, "
            f"use_dir={plugin.use_directory_urls}"  # at last, because most likely always redundant with docs_dir
        )


    @classmethod
    def get_flow_data(cls, flow_data, plugin:'AddressAddressesPlugin', kind:FlowKind, data:Union[Page,str]):
        key     = cls.get_flow_key(plugin)
        sub_key = data.file.src_uri if isinstance(data,Page) else data
        pif     = flow_data[key]
        paf     = pif[kind]
        value   = paf[sub_key]
        return value


    @classmethod
    def assert_flow(cls, flow_data, plugin:'AddressAddressesPlugin', kind:FlowKind, data:Union[Page,str]):
        expected = cls.get_flow_data(flow_data, plugin, kind, data)
        actual   = data.content if isinstance(data,Page) else plugin.global_handler.references.id_to_data
        assert actual == expected



    #----------------------------------------------------------------------------------
    #                               Non flow routines
    #----------------------------------------------------------------------------------


    def add(self, plugin:'AddressAddressesPlugin', page:Page, id:str, tag:Tag, target:str):
        identifier = simplify_ids(id)
        tag_code = simplify_ids(str(tag))
        if identifier not in self.dct_misc:
            chunk = Chunk('bare-ref' in identifier, identifier, {})
            self.dct_misc[identifier] = chunk
        else:
            chunk = self.dct_misc[identifier]

        loc = chunk.locations.get(page.file.src_uri, Location.default(page.file.src_uri, tag_code))
        chunk.locations[page.file.src_uri] = loc
        use_dir = plugin.use_directory_urls
        loc.data[use_dir].url    = simplify_ids(page.url)
        loc.data[use_dir].target = simplify_ids(target)



    def dump(self, plugin:'AddressAddressesPlugin'):

        with open('dump/dumb.py', mode='w') as f:
            f.write(self.to_tests())
            # f.write('\n#------------------------------------\n#References:\n')

            # for field in 'id_to_data id_to_source source_to_ids snippets'.split():
                # data: dict = getattr(plugin.global_handler.references, field)
                # f.write(dict_to_str(data, field))
            # f.write(str(plugin))
            # f.write(dict_to_str(self.html_content, 'html_content'))
            # f.write(dict_to_str(self.end_context, 'end_context'))



    def to_tests(self):
        return """from .data_classes import *


PAGE_CONTENT_DATA = PoolData([\n""" + "".join(c.to_tests() for c in self.dct_misc.values()) + "\n])\n"





class Flow(dict):
    """
        Flow data structure:
        {
            sources:{
                refs_on_hook:{
                    0: dct,
                    ...
                },
                htmls: {        # holds ANY kind of html code
                    0: dct,
                    ...
                },
                markdown: {
                    0: dct,
                    ...
                }
            },
            flow:{
                flow_key: {
                    refs_on_hook: {
                        hook: "refs_on_hook[i]",
                        ...
                    },
                    markdown: "markdown[i]",
                    html_content: "htmls[i]",
                    start_content: "htmls[i]",
                    end_content: "htmls[i]",
                }
            }
        }
        """

    FILE = Path('dump/full_flow.json')


    def __init__(self, file:Path=None):
        self.file = file or self.FILE
        self.uniques = {}
        flow = self.__load()
        super().__init__(flow)


    def __load(self):
        flow_str = dedent('''
        {
            "sources": {
                "refs_on_hook":{},
                "htmls": {},
                "markdown": {}
            },
            "flow": {}
        }''')
        if self.file.is_file():
            flow_str = self.file.read_text(encoding='utf8') or flow_str

        flow = json.loads(flow_str)
        for source,dct in flow['sources'].items():
            for i,data in dct.items():
                path = f"flow['sources'][{source!r}]['{i}']"
                self.uniques[self.__dct_to_hash(data)] = path
        return flow


    @staticmethod
    def __dct_to_hash(dct:dict):
        return frozenset(dct.items())


    def get_path_for(self, data_kind:str, data:dict):
        key = self.__dct_to_hash(data)
        data_kind = data_kind if data_kind in self['sources'] else 'htmls'

        if key not in self.uniques:
            src = self['sources'][data_kind]
            i = len(src)
            src[i] = data
            path = f"flow['sources'][{ data_kind !r}]['{ i }']"
            self.uniques[key] = path

        return self.uniques[key]


    def push(self, kind:str, flow_key:str, data:dict, hook:str=None):
        if hook is None:
            digging,final_key = ('flow', flow_key), kind
        else:
            digging, final_key = ('flow', flow_key, kind), hook

        dct = self
        for key in digging:
            if key not in dct: dct[key] = {}
            dct = dct[key]
        dct[final_key] = self.get_path_for(kind, data)


    def dump(self):
        ordered_flow = { k:v for k,v in sorted(self['flow'].items()) }
        self['flow'] = ordered_flow
        flow_str = json.dumps(self, indent=2)
        self.file.touch(exist_ok=True)
        self.file.write_text(flow_str, encoding='utf8')


    @classmethod
    def to_test_data(cls, source:Path=None):
        """ Rebuild the original SOURCE_DATA structure for the tests """
        flow = Flow(source or Path("tests/test_mkdocsaddresses/data_sets/full_flow.json"))
        data = { flow_key: {
                kind: eval(data, {'flow':flow}) if isinstance(data,str)
                    else {hook: eval(path, {'flow':flow}) for hook,path in data.items()}
                for kind,data in data_dct.items()
            }
            for flow_key,data_dct in flow['flow'].items()
        }
        return data
