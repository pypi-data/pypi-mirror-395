from __future__ import annotations

import logging
import sys

from docnote_extract._module_tree import ConfiguredModuleTreeNode
from docnote_extract._module_tree import SummaryTreeNode
from docnote_extract.crossrefs import GetattrTraversal
from docnote_extract.summaries import ModuleSummary

logger = logging.getLogger(__name__)


def filter_module_summaries(
        summary_tree_node: SummaryTreeNode,
        configured_tree_node: ConfiguredModuleTreeNode,
        *,
        _forced_inclusion: bool | None = None
        ) -> None:
    """Recursively walks the passed module tree, **starting from the
    root node** of both the summary and configured trees, setting the
    ``to_document`` value on all module descriptions within the tree,
    but not any of the modules' members.

    Private modules (modules with a relname beginning with an
    underscore, but not ``__dunders__``) and their children will receive
    ``to_document=False`` unless overwritten by the module's effective
    config's ``include_in_docs`` setting.

    Note that this operates in-place.
    """
    if _forced_inclusion is None:
        effective_config = configured_tree_node.effective_config

        if (
            effective_config.include_in_docs is False
            or (
                _conventionally_private(summary_tree_node.relname)
                and not effective_config.include_in_docs)
        ):
            is_included = False
            inclusion_to_force = False

        else:
            is_included = True
            inclusion_to_force = None

    else:
        inclusion_to_force = _forced_inclusion
        is_included = _forced_inclusion

    if is_included:
        # Doing it this way to bypass the frozen-ness
        object.__setattr__(summary_tree_node, 'to_document', True)
        summary_tree_node.module_summary.metadata.to_document = True
    else:
        # Doing it this way to bypass the frozen-ness
        object.__setattr__(summary_tree_node, 'to_document', False)
        summary_tree_node.module_summary.metadata.to_document = False

    for relname, child in summary_tree_node.children.items():
        filter_module_summaries(
            child,
            configured_tree_node / relname,
            _forced_inclusion=inclusion_to_force)


def filter_canonical_ownership(
        module_summary: ModuleSummary,
        *,
        remove_unknown_origins: bool = True,
        ) -> None:
    """Given a module summary and its associated normalized objs lookup,
    this sets ``disowned=True`` on the metadata for all summaries that
    cannot be attributed to passed module, recursively. Note that only
    toplevel module members can be disowned, and their disownment
    applies recursively to all child objects.

    Note that seeing a config value for ``include_in_docs`` is not
    relevant to this, for two reasons:
    ++  because it might be an unstubbed (tracked) import, it might
        still be defined somewhere else
    ++  **all of the canonical module inference logic is contained
        within normalization!**
    """
    module_name = module_summary.name
    # Modules themselves can, by definition, never be disowned
    module_summary.metadata.disowned = False

    for module_member in module_summary.members:
        name = module_member.name
        canonical_module = module_member.metadata.canonical_module

        # Dunder all must ALWAYS be included!
        if module_summary.in_dunder_all(name):
            _set_canonical_ownership(module_summary, name, disowned=False)

        elif canonical_module is None:
            if remove_unknown_origins:
                _set_canonical_ownership(module_summary, name, disowned=True)
            else:
                _set_canonical_ownership(module_summary, name, disowned=False)

        elif canonical_module == module_name:
            _set_canonical_ownership(module_summary, name, disowned=False)

        else:
            _set_canonical_ownership(module_summary, name, disowned=True)


def _set_canonical_ownership(
        module_summary: ModuleSummary,
        toplevel_name: str,
        disowned: bool
        ) -> None:
    module_member = module_summary / GetattrTraversal(toplevel_name)

    for summary in module_member.flatten():
        summary.metadata.disowned = disowned


def filter_private_summaries(module_summary: ModuleSummary) -> None:
    """Given an existing module summary with initialized metadata (ie,
    ``extracted_inclusion`` has been set), this applies first the
    normal python conventions (single-underscore names are private),
    and then the effective config for the object, resulting in a final
    decision about whether or not the object should be included in docs
    or not. This is then set on the ``to_document`` attribute.

    Note that the module summary itself is skipped, as it gets set
    during ``filter_module_summaries``.
    """
    for summary in module_summary.flatten():
        # We don't want this to be contingent upon the ordering of the
        # flattened summaries, and this isn't super performance sensitive,
        # and ``is`` is very fast. Therefore, just do this every iteration.
        if summary is module_summary:
            continue

        name: str | None = getattr(summary, 'name', None)
        try:
            extracted_inclusion = summary.metadata.extracted_inclusion
            canonical_module = summary.metadata.canonical_module
        except AttributeError:
            logger.error('Summary metadata not fully populated: %s', summary)
            raise

        if extracted_inclusion is False:
            summary.metadata.to_document = False

        elif name is not None:
            # Dunders need special handling, because otherwise they generate a
            # LOT of noise.
            # We want to restrict the returned members to things that were
            # actually defined by the library being documented, not things that
            # are coming directly from the stdlib.
            if _is_dunder(name):
                if (
                    canonical_module is None
                    or canonical_module in sys.stdlib_module_names
                ):
                    summary.metadata.to_document = False
                else:
                    summary.metadata.to_document = True

            elif (
                _conventionally_private(name)
                and not extracted_inclusion
            ):
                summary.metadata.to_document = False
            else:
                summary.metadata.to_document = True

        else:
            summary.metadata.to_document = True


def _is_dunder(name: str) -> bool:
    return name.startswith('__') and name.endswith('__')


def _conventionally_private(name: str) -> bool:
    """Returns True if the passed name is, by python convention, to be
    considered private -- ie, if it starts with an underscore, but isn't
    a dunder.

    Note that this also includes mangled names, since they'll end up
    also starting with an underscore (``Foo.__bar`` is mangled to
    ``Foo._Foo__bar``).
    """
    # Could we do this with regex? Yeah, sure, but then we'd have 3 problems.
    # But more seriously, this is faster to write, faster to read, and -- at
    # least naively -- I would assume it's also a bit faster, since we're not
    # dealing with an entire regex engine.
    return name.startswith('_') and not _is_dunder(name)
