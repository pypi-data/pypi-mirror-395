from mkdocs.exceptions import PluginError

# pylint: disable=too-many-ancestors


class AddresserError(PluginError):
    """ Generic mkdocs-addresses exception. """



#------------------------------------------------



class AbortError(AddresserError):
    """ Thrown at the face of mkdocs logger... :p
        (see addresses_auto_log final try/except block)
    """



# class InclusionError(AddresserError):
#     """ A file will result in a code snippet using the same prefix than a previous one """



class DumpOnlyException(AddresserError):
    """ Generic mkdocs-addresses exception. """


class NoStaticHandlerError(AddresserError):
    """ No StaticHandler instance declared yet (internal) """



class AddresserConfigError(AddresserError):
    """ Plugin config related error """


class InvalidOperationError(AddresserConfigError):
    """ Don't to that... (ConfigDescriptor specific => internal) """



#------------------------------------------------



class AbstractAddressError(AddresserError):
    """ Path/address related errors, that cover errors found when an address/path is
        found in a `<a href >` or `<img src >` tag.
    """


class MarkdownLinkError(AbstractAddressError):
    """ Addresses should never be written using the path of the md file, when using the plugin.
        Identifiers should be used instead.
    """

class NonAbsoluteAddressError(AbstractAddressError):
    """ Address should be absolute """

class NonRelativeAddressError(AbstractAddressError):
    """ Address is not considered relative (no leading dot). If this error occur on something
        that should be an absolute/external link, this means you probably should
        [mark it as ignored](--mkdocs_addresses_config_plugin_PluginOptions_ignored_identifiers_or_addresses) it.
    """

class LeadingSlashAddressError(AbstractAddressError):
    """ Address with leading slash are not allowed """

class TrailingSlashAddressError(AbstractAddressError):
    """ Address with trailing slash """

class NotAnImageAddressError(AbstractAddressError):
    """ The address isn't considered the one of an image. """

class NotAFileAddressError(AbstractAddressError):
    """ The corresponding file does not exist.

        (note: not using FileNotFoundError, so that all the errors are inheriting from the
        root class `AddresserError`)
    """

class NoMoveUpDirOnNonIndexPageUrlsAsDirAddressError(AbstractAddressError):
    """ When `use_directory_urls=true`, the address has to start with a "../" when defined in any
        markdown document that is not a `index.md` file (Except if the address is a bare anchor
        defined in the same page).
    """





class AnchorAddressError(AbstractAddressError):
    """ Invalid anchor found in an Address """


class ImageWithAnchorError(AnchorAddressError):
    """ Images src attribute should never contain an anchor """

class TooManyAnchorsError(AnchorAddressError):
    """ More than one `#` in the address """

class AnchorUnknownError(AnchorAddressError):
    """ Anchor not defined anywhere """

class AnchorNotInPageError(AnchorAddressError):
    """ The address is a bare anchor, but it is not found in the current page """

class EmptyAnchorError(AnchorAddressError):
    """ Address with a trailing anchor, but without identifier after it.
    <br>This is found with this kind of typo in the markdown document: `{: # wrong }`,
    which results in addresses like `".../#"`.
    """



#------------------------------------------------



class IdentifierError(AddresserError):
    """ Generic error related to identifiers: covers identifiers definitions and usages. """



class InvalidIdentifierError(IdentifierError):
    """ A reference identifier is invalid """

class DuplicateIdentifierError(IdentifierError):
    """ An identifier has already been registered """

class UnknownIdentifierError(IdentifierError):
    """ Unknown identifier """

class UnknownExternalLinkIdentifierError(IdentifierError):
    """ External link syntax that with an identifier which is not found in the
        [external_links_file](--mkdocs_addresses_config_plugin_PluginOptions_external_links_file)
    """



class OutdatedReferenceError(IdentifierError):
    """ Identifier used in some document, but that isn't defined anywhere anymore. """



#-------------------------------------------------

class ConcurrentPluginError(Exception):
    """ Using only for testing purpose, ensuring that pytest doesn't run in // """
