from __future__ import annotations

import inspect
import typing
from collections.abc import Sequence
from typing import Any
from typing import Literal

from docnote import DOCNOTE_CONFIG_ATTR_FOR_MODULES
from docnote import DocnoteConfig
from docnote import DocnoteConfigParams
from docnote import Note

from docnote_extract import KNOWN_MARKUP_LANGS
from docnote_extract.exceptions import InvalidConfig
from docnote_extract.summaries import DocText

if typing.TYPE_CHECKING:
    from docnote_extract._extraction import ModulePostExtraction


def validate_config(config: DocnoteConfig, hint: Any) -> Literal[True]:
    """Performs any config enforcement (currently, just the
    ``enforce_known_lang`` parameter). Raises ``InvalidConfig`` if
    enforcement fails.
    """
    if config.enforce_known_lang:
        if (
            config.markup_lang is not None
            and config.markup_lang not in KNOWN_MARKUP_LANGS
        ):
            raise InvalidConfig(
                'Unknown markup lang with enforcement enabled!', config, hint)

    return True


def coerce_config(
        module: ModulePostExtraction,
        *,
        parent_stackables: DocnoteConfigParams | None = None
        ) -> DocnoteConfig:
    """Given a module-post-extraction, checks for an explicit config
    defined on the module itself. If found, returns it. If not found,
    creates an empty one.
    """
    explicit_config = getattr(module, DOCNOTE_CONFIG_ATTR_FOR_MODULES, None)
    if parent_stackables is None:
        parent_stackables = {}

    if explicit_config is None:
        return DocnoteConfig(**parent_stackables)

    elif not isinstance(explicit_config, DocnoteConfig):
        raise TypeError(
            f'``<module>.{DOCNOTE_CONFIG_ATTR_FOR_MODULES}`` must always '
            + 'be a ``DocnoteConfig`` instance!', module, explicit_config)

    # Note: the intermediate step is required to OVERWRITE the values. If we
    # just did these directly within ``DocnoteConfig``, python would complain
    # about getting multiple values for the same keyword arg.
    combination: DocnoteConfigParams = {
        **parent_stackables, **explicit_config.as_nontotal_dict()}
    return DocnoteConfig(**combination)


def textify_notes(
        raw_notes: Sequence[Note],
        effective_config: DocnoteConfig
        ) -> tuple[DocText, ...]:
    retval: list[DocText] = []
    for raw_note in raw_notes:
        # Note that the passed effective_config will already have been
        # validated at this point, but not the note's direct config.
        if raw_note.config is not None:
            # Note that we don't want just the stackables here; this is already
            # an effective config for the thing the note is attached to, so
            # we've already applied stacking rules. We want the whole thing.
            combination: DocnoteConfigParams = {
                **effective_config.as_nontotal_dict(),
                **raw_note.config.as_nontotal_dict()}
            effective_config = DocnoteConfig(**combination)
            validate_config(effective_config, f'On-note config for {raw_note}')

        retval.append(DocText(
            value=inspect.cleandoc(raw_note.value),
            markup_lang=effective_config.markup_lang))

    return tuple(retval)


def extract_docstring(
        obj: Any,
        effective_config: DocnoteConfig
        ) -> DocText | None:
    """Gets the DocText version of the docstring, if one is defined.
    Otherwise, returns None.
    """
    # Note that this gets cleaned up internally by ``inspect.cleandoc`` (see
    # stdlib docs) and also normalized to str | None.
    raw_clean_docstring = inspect.getdoc(obj)
    if not raw_clean_docstring or raw_clean_docstring.isspace():
        return None
    else:
        return DocText(
            value=raw_clean_docstring,
            markup_lang=effective_config.markup_lang)
