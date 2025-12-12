"""Schema diff utilities for comparing PithSchema objects."""

from __future__ import annotations

from dataclasses import dataclass, field

from pith.core import PithSchema


@dataclass
class SchemaDiff:
    """Command-level diff between two schemas."""

    added: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    modified: list[str] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        """Return True if there are any differences."""
        return bool(self.added or self.removed or self.modified)

    def summary(self) -> str:
        """Return a human-readable summary of changes."""
        if not self.has_changes:
            return "No changes detected."

        lines: list[str] = []
        if self.added:
            lines.append(f"Added commands ({len(self.added)}):")
            for cmd in self.added:
                lines.append(f"  + {cmd}")
        if self.removed:
            lines.append(f"Removed commands ({len(self.removed)}):")
            for cmd in self.removed:
                lines.append(f"  - {cmd}")
        if self.modified:
            lines.append(f"Modified commands ({len(self.modified)}):")
            for cmd in self.modified:
                lines.append(f"  ~ {cmd}")
        return "\n".join(lines)


def compare_schemas(old: PithSchema, new: PithSchema) -> SchemaDiff:
    """Compare two schemas and return command-level differences.

    Args:
        old: The existing/previous schema
        new: The new/updated schema

    Returns:
        SchemaDiff with added, removed, and modified command lists
    """
    old_cmds = set(old.commands.keys())
    new_cmds = set(new.commands.keys())

    added = sorted(new_cmds - old_cmds)
    removed = sorted(old_cmds - new_cmds)

    # Check for modifications in common commands
    common = old_cmds & new_cmds
    modified: list[str] = []

    for name in sorted(common):
        if _command_differs(old.commands[name], new.commands[name]):
            modified.append(name)

    return SchemaDiff(added=added, removed=removed, modified=modified)


def _command_differs(old_cmd: object, new_cmd: object) -> bool:
    """Check if two commands differ (command-level comparison).

    Compares pith, tier1 summary, tier2 arguments/options count,
    and tier3 examples/related count.
    """
    from pith.core import Command

    if not isinstance(old_cmd, Command) or not isinstance(new_cmd, Command):
        return old_cmd != new_cmd

    # Compare pith description
    if old_cmd.pith != new_cmd.pith:
        return True

    # Compare tier1 summary
    if old_cmd.tier1.summary != new_cmd.tier1.summary:
        return True

    # Compare tier2 (arguments and options)
    old_tier2 = old_cmd.tier2
    new_tier2 = new_cmd.tier2

    if (old_tier2 is None) != (new_tier2 is None):
        return True

    if old_tier2 and new_tier2:
        # Compare argument count and names
        old_args = {a.name for a in old_tier2.arguments}
        new_args = {a.name for a in new_tier2.arguments}
        if old_args != new_args:
            return True

        # Compare option count and names
        old_opts = {o.name for o in old_tier2.options}
        new_opts = {o.name for o in new_tier2.options}
        if old_opts != new_opts:
            return True

    # Compare tier3 (examples and related)
    old_tier3 = old_cmd.tier3
    new_tier3 = new_cmd.tier3

    if (old_tier3 is None) != (new_tier3 is None):
        return True

    if old_tier3 and new_tier3:
        if set(old_tier3.examples) != set(new_tier3.examples):
            return True
        if set(old_tier3.related) != set(new_tier3.related):
            return True

    # Compare intents
    return set(old_cmd.intents) != set(new_cmd.intents)
