class InvalidConfig(Exception):
    """Raised when ``DocnoteConfig`` validation fails. Currently, this
    only applies if ``enforce_known_lang`` was set to True, but the
    declared ``markup_lang`` was unknown.
    """


class NotFirstpartyPackage(LookupError):
    """Raised if you attempt to resolve a crossref on a ``Docnotes``
    instance with a package wholly unknown to the instance (ie, one that
    was not passed as a firstparty package to ``gather``).
    """


class UnknownCrossrefTarget(LookupError):
    """Raised if you attempt to resolve a crossref on a ``Docnotes``
    instance with a correct firstparty package, but where the actual
    target of the crossref is unknown.
    """
