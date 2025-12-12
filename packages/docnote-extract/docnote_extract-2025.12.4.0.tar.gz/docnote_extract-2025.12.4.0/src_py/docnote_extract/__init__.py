# ruff: noqa: E402
from docnote import MarkupLang

__all__ = [
    'KNOWN_MARKUP_LANGS',
    'Docnotes',
    'SummaryMetadata',
    'SummaryTreeNode',
    'gather',
]

KNOWN_MARKUP_LANGS: set[str | MarkupLang] = set(MarkupLang)

# Note that all other imports need to come after that, in order to avoid
# circular dependencies. These are all re-exports!
from docnote_extract._gathering import Docnotes
from docnote_extract._gathering import gather
from docnote_extract._module_tree import SummaryTreeNode
from docnote_extract._summarization import SummaryMetadata
