#!/usr/bin/env python3
#
# Copyright 2025 Oliver Ni
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function

import itertools
import sys


def main():
    # Each entry is: (alias, expansion, allow_when_oneof, incompatible_with)
    #
    #   alias:              the characters appended to build the alias name
    #   expansion:          the text appended to build the full command
    #   allow_when_oneof:   if set, at least one of these alias parts must
    #                       already be present in the command for this entry
    #                       to be included (i.e. prerequisites)
    #   incompatible_with:  if set, none of these alias parts may be present
    #                       in the command (i.e. mutual exclusion)

    cmds = [("j", "jj", None, None)]

    # ── top-level commands ────────────────────────────────────────────────
    ops = [
        ("a", "abandon", None, None),
        ("ab", "absorb", None, None),
        ("c", "commit", None, None),
        ("d", "diff", None, None),
        ("de", "describe", None, None),
        ("du", "duplicate", None, None),
        ("e", "edit", None, None),
        ("l", "log", None, None),
        ("n", "new", None, None),
        ("x", "next", None, None),
        ("p", "prev", None, None),
        ("rb", "rebase", None, None),
        ("rs", "restore", None, None),
        ("rv", "resolve", None, None),
        ("w", "show", None, None),
        ("sp", "split", None, None),
        ("sq", "squash", None, None),
        ("s", "status", None, None),
        ("un", "undo", None, None),
        ("rd", "redo", None, None),
        ("el", "evolog", None, None),
        # ── git subcommands ───────────────────────────────────────────────
        ("gc", "git clone", None, None),
        ("gf", "git fetch", None, None),
        ("gi", "git init", None, None),
        ("gp", "git push", None, None),
        # ── bookmark subcommands ──────────────────────────────────────────
        ("bc", "bookmark create", None, None),
        ("bd", "bookmark delete", None, None),
        ("bf", "bookmark forget", None, None),
        ("bl", "bookmark list", None, None),
        ("bm", "bookmark move", None, None),
        ("br", "bookmark rename", None, None),
        ("bs", "bookmark set", None, None),
        ("bt", "bookmark track", None, None),
        ("bu", "bookmark untrack", None, None),
        # ── op subcommands ────────────────────────────────────────────────
        ("ol", "op log", None, None),
        ("or", "op restore", None, None),
    ]

    # ── non-value flags (can be combined freely, order doesn't matter) ───
    flags = [
        ("s", "--summary", ["d", "l", "w"], ["st", "p"]),
        ("st", "--stat", ["d", "l", "w"], ["s", "p"]),
        ("p", "--patch", ["l"], ["s", "st", "g"]),
        ("g", "--git", ["d", "l", "w"], ["s", "st", "p"]),
        ("a", "--all-remotes", ["bl", "gf"], None),
        ("a", "--all", ["gp"], ["r", "c"]),
        ("i", "--interactive", ["c", "sq"], None),
    ]

    # ── value flags (take an argument → must be last, mutually exclusive) ─
    value_flags = [
        ("r", "-r", ["d", "l", "sq", "bs", "bl", "gp"], None),
        ("m", "-m", ["c", "de", "n", "sq"], None),
        ("c", "-c", ["gp"], None),
        ("o", "-o", ["rb"], None),
    ]

    # [(items, optional, take_exactly_one)]
    parts = [
        (cmds, False, True),  # always exactly one base command
        (ops, True, True),  # zero or one operation
        (flags, True, False),  # zero or more flags (permuted)
        (value_flags, True, True),  # zero or one value flag at the end
    ]

    shell_formatting = {
        "bash": "alias {0}='{1}'",
        "zsh": "alias {0}='{1}'",
        "fish": "abbr --add {0} \"{1}\"",
    }

    shell = sys.argv[1] if len(sys.argv) > 1 else "bash"
    if shell not in shell_formatting:
        raise SystemExit(
            'Shell "{}" not supported. Options: {}'.format(
                shell, list(shell_formatting.keys())
            )
        )

    # ── multi-command combos (hand-curated, not combinatorial) ─────────
    combos = [
        ("jnma", "jj new main"),
        ("jrboma", "jj rebase -o main"),
        ("jgfn", "jj git fetch && jj new"),
        ("jgfnma", "jj git fetch && jj new main"),
        ("jgfrbo", "jj git fetch && jj rebase -o"),
        ("jgfrboma", "jj git fetch && jj rebase -o main"),
    ]

    out = gen(parts)

    seen_aliases = set()
    for cmd in out:
        alias = "".join([a[0] for a in cmd])
        command = " ".join([a[1] for a in cmd])
        if alias in seen_aliases:
            print("WARNING: alias conflict: {}".format(alias), file=sys.stderr)
        seen_aliases.add(alias)
        print(shell_formatting[shell].format(alias, command))

    for alias, command in combos:
        if alias in seen_aliases:
            print("WARNING: alias conflict: {}".format(alias), file=sys.stderr)
        seen_aliases.add(alias)
        print(shell_formatting[shell].format(alias, command))


# ── combinatorial generator ──────────────────────────────────────────────


def gen(parts):
    out = [()]
    for items, optional, take_exactly_one in parts:
        orig = list(out)
        if take_exactly_one:
            combos = combinations(items, 1, include_0=optional)
        else:
            combos = combinations(items, len(items), include_0=optional)

        # for optional groups, generate all orderings so that e.g. both
        # "sp" and "ps" are valid aliases (flags are not positional)
        if optional:
            new_combos = []
            for c in combos:
                new_combos += list(itertools.permutations(c))
            combos = new_combos

        new_out = []
        for segment in combos:
            for stuff in orig:
                if is_valid(stuff + segment):
                    new_out.append(stuff + segment)
        out = new_out
    return out


def is_valid(cmd):
    return is_valid_requirements(cmd) and is_valid_incompatibilities(cmd)


def is_valid_requirements(cmd):
    parts = {c[0] for c in cmd}
    for i in range(len(cmd)):
        requirements = cmd[i][2]
        if requirements and not (parts & set(requirements)):
            return False
    return True


def is_valid_incompatibilities(cmd):
    parts = {c[0] for c in cmd}
    for i in range(len(cmd)):
        incompatibilities = cmd[i][3]
        if incompatibilities and (parts & set(incompatibilities)):
            return False
    return True


def combinations(a, n, include_0=True):
    result = []
    for j in range(0, n + 1):
        if not include_0 and j == 0:
            continue
        cs = itertools.combinations(a, j)
        # only check incompatibilities early; requirements are checked later
        # once the full command (ops + flags) is assembled
        cs = [c for c in cs if is_valid_incompatibilities(c)]
        result += list(cs)
    return result


if __name__ == "__main__":
    main()
