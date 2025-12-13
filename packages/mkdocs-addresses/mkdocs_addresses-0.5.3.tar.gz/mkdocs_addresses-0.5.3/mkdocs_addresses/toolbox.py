import re
import math

from .exceptions import AddresserError







def fatal_if(truthy, msg:str, exc=AddresserError):
    if truthy:
        raise exc(msg)



def plugin_dump_padder(k:str, pad=25):
    return k.ljust(pad * math.ceil( len(k) / pad ))



def extract_external_links_refs_in_md(markdown:str):
    """ Extract all the identifiers of externals links in the given markdown code:
                [...][identifier]
    """
    return re.findall(r'\[[^\]]*\]\[([^\]\n]+)\]', markdown)
