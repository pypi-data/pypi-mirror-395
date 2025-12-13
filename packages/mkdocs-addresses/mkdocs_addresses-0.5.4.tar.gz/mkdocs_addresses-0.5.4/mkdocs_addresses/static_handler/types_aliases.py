from typing import Union
from pathlib import Path
from mkdocs.structure.pages import Page



Ref = SnipDescription = str

UriPath = str
""" String representing an uri path. May be rooted at cwd or docs_dir, depending on the
    "logic" it refers to.
"""

UriDocsPathStr = str
""" String representing an uri path, rooted at the docs_dir """

UriCwdPathStr = str
""" String representing an uri path, rooted at the cwd """

SourceUsedRef = Union[Page, UriDocsPathStr]
""" Union[ Page, UriDocsPath ] """

#----------------------

PathCwd = Path
""" Path instance, rooted at the cwd """

PathDocs = Path
""" Path instance, rooted at the docs_dir """

SourceRef = Union[ Page, PathCwd ]
""" Union[ Page, PathCwd ] """
