
import re
from typing import Generator, Set, NamedTuple, TYPE_CHECKING

from bs4 import BeautifulSoup
from bs4.element import Tag

from mkdocs_addresses.toolbox import extract_external_links_refs_in_md


from .addresses_checker import AddressKind
from .auto_completion_handler import RefKind


if TYPE_CHECKING:
    from mkdocs_addresses.addresses_plugin import AddressAddressesPlugin



class SoupTag(NamedTuple):
    tag: Tag
    attr: str
    kind: RefKind
    identifier: str



TR_FR_TABLE = str.maketrans(
    "àâäéèêëîïôöùûüç",
    "aaaeeeeiioouuuc"
)

def kebabize_fr(msg:str):
    ke     = msg.lower().translate(TR_FR_TABLE)
    purged = re.sub(r'&(amp|lt|gt);|[^a-z0-9_ -]+', '', ke)
    bab    = re.findall(r'\w+', purged)
    return '-'.join(bab)



class PluginSoupExcludingCodes(BeautifulSoup):
    """ Personalized version of the BeautifulSoup parser, it will ignore the tags that are
        contained in <code> tags.

        Takes the plugin as argument in the constructor so that it can extract the configuration
        data from it.
    """

    __codes: Set[Tag]
    __plugin: 'AddressAddressesPlugin'


    def __init__(self, html:str, plugin:'AddressAddressesPlugin'):
        super().__init__(html, features="html.parser")
        self.__codes = [*super().find_all('code')]
        self.__plugin = plugin



    def decompose_header_to_kebab(self, header:Tag):
        """ Takes an header tag (<h...>) and converts it to its string content, by removing
            all the unwanted children.

            WARNING: THIS IS MUTATING THE TREE!
        """
        for child in header:
            if isinstance(child,Tag) and "headerlink" in child.get('class',''):
                child.decompose()

        stripped   = header.get_text()
        keb_header = kebabize_fr(stripped)
        return keb_header



    def find_all(self,*a,**kw) -> Set[Tag] :
        candidates = super().find_all(*a,**kw)
        exclusions = { tag for code in self.__codes
                           for tag in code.find_all(*a,**kw) }

        # Filter output as list, and not using sets, to keep the iteration order consistent
        # in other parts of the program:
        return [ cnd for cnd in candidates if cnd not in exclusions ]



    def get_tags_with_ids(self):
        """ Extract all the tags in the html content that:
                - Contain an id attribute (potentially defined on the fly by mkdocs: headers!)
                - Are not in a <code> tag
                - Compliant with the current plugin configuration (ignored ids and classes, ...)
        """
        return [tag for tag in self.find_all(id=True) if self.is_not_restricted_tag(tag) ]


    def gen_targeted_addresses_data(self) -> Generator[SoupTag,None,None]:
        """ Explore an html content, searching for links href and images src addresses,
            and yield the corresponding tag with some other informations.
            Note: anchors definitions are skipped.
        """
        # Enforce the needed attribute to be present (href and src): this avoids errors when
        # parsing manually written wrong tags, like "<a>no href!</a>"
        links = self.find_all('a', href=True)
        imgs  = self.find_all('img', src=True)

        targeted_tags = (
            (links, 'href', AddressKind.HREF),
            (imgs,  'src',  AddressKind.SRC),
        )
        for tags,attr,kind in targeted_tags:
            for tag in tags:
                if self.is_not_restricted_tag(tag, attr):
                    identifier = tag[attr]
                    yield SoupTag(tag, attr, kind, identifier)


    def is_not_restricted_tag(self, tag:Tag, attr:str=None):
        """ Check that the given tag:
                - either doesn't have any class, or has no ignored class
                - either doesn't have any id, or has no ignored id (not private, not white listed in any way)
                - it's attribute of interest
        """
        ignored_classes    = self.__plugin.ignored_classes
        black_list         = self.__plugin.ignored_identifiers_or_addresses
        black_list_matcher = self.__plugin.black_list_pattern.match

        class_ok = (
            not tag.has_attr('class')
            or not ignored_classes
            or not set(tag['class']) & ignored_classes
        )
        id_ok = class_ok and (
            not tag.has_attr('id')
            or not (
                ( tag_id := tag['id'] ).startswith('__')
                or tag_id in black_list
                or black_list_matcher(tag_id)
            )
        )
        if not id_ok:
            return False

        if not attr:
            return True

        addr = tag[attr]
        return not (addr in black_list or black_list_matcher(addr))


    def destroy_codes(self):
        """ Mutate the current instance, removing all the <code> tags """
        for code in self.__codes:
            code.decompose()


    def get_external_refs_in_codes(self):
        """ Generate all the external references that are in code tags (hence, have not been
            modified in the html)
        """
        return (
            id_ for code in self.__codes
                for id_ in extract_external_links_refs_in_md(code.get_text())
        )
