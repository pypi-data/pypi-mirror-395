"""
Centralize all the elements needed to improve the overall performances, using a global
cache to:
    - Register all the references definitions ("!!img_png", "--header-link", ...) and
      where they are defined (file).
    - Register all the usages of each references (in what file they are used, and what
      file is the target).
    - Keep track of what files got deleted/modified since last build (relative to one
      "mkdocs serve" command).
With all this, the plugin will check the minimal number of files necessary on a build.
"""

from .tracker_addresses_usage_pool import AddressesUsagePool
from .tracker_references import References
from .static_handler import StaticHandler