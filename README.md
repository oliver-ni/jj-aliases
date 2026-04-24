# jj-aliases

Programmatically generated shell aliases for [jj](https://github.com/jj-vcs/jj) (Jujutsu), inspired by [kubectl-aliases](https://github.com/ahmetb/kubectl-aliases).

This repository contains [a script](generate_aliases.py) to generate convenient shell aliases for `jj`, so you no longer need to spell out every single command and flag over and over again.

An example alias:

```
alias jlgr='jj log --git -r'
```

Confused? Read on.

### Examples

Some of the 81 generated aliases:

```sh
jdem 'fix typo'       # jj describe -m 'fix typo'
jcm 'add feature'     # jj commit -m 'add feature'
jdst                  # jj diff --stat
jwg                   # jj show --git
jlsr '::@'            # jj log --summary -r '::@'
jgf                   # jj git fetch
jgpc @                # jj git push -c @
jrboma                # jj rebase -o main
jgfnma                # jj git fetch && jj new main
jgfrboma              # jj git fetch && jj rebase -o main
```

See the full list in [`.jj_aliases`](.jj_aliases).

### Installation

You can directly download the [`.jj_aliases`](.jj_aliases) file for bash/zsh or the [`.jj_aliases.fish`](.jj_aliases.fish) file for fish and save it to your home directory.

#### Bash/Zsh

Add the following to your `.bashrc`/`.zshrc`:

```sh
[ -f ~/.jj_aliases ] && source ~/.jj_aliases
```

#### Fish

Add the following to your `~/.config/fish/config.fish`:

```fish
test -f ~/.jj_aliases.fish && source ~/.jj_aliases.fish
```

This uses fish [abbreviations](https://fishshell.com/docs/current/cmds/abbr.html) instead of aliases, so pressing space shows the full command before execution.

### Syntax explanation

- **`j`**: `jj`
- commands:
  - **`a`**: `abandon`
  - **`ab`**: `absorb`
  - **`c`**: `commit`
  - **`d`**: `diff`
  - **`de`**: `describe`
  - **`du`**: `duplicate`
  - **`e`**: `edit`
  - **`l`**: `log`
  - **`n`**: `new`
  - **`x`**: `next`
  - **`p`**: `prev`
  - **`rb`**: `rebase`
  - **`rs`**: `restore`
  - **`rv`**: `resolve`
  - **`w`**: `show`
  - **`sp`**: `split`
  - **`sq`**: `squash`
  - **`s`**: `status`
  - **`un`**: `undo`
  - **`rd`**: `redo`
  - **`el`**: `evolog`
- git subcommands:
  - **`gc`**: `git clone`
  - **`gf`**: `git fetch`
  - **`gi`**: `git init`
  - **`gp`**: `git push`
- bookmark subcommands:
  - **`bc`**: `bookmark create`
  - **`bd`**: `bookmark delete`
  - **`bf`**: `bookmark forget`
  - **`bl`**: `bookmark list`
  - **`bm`**: `bookmark move`
  - **`br`**: `bookmark rename`
  - **`bs`**: `bookmark set`
  - **`bt`**: `bookmark track`
  - **`bu`**: `bookmark untrack`
- op subcommands:
  - **`ol`**: `op log`
  - **`or`**: `op restore`
- flags:
  - **`s`**: `--summary`
  - **`st`**: `--stat` (when used as a flag after a command like `d`, `l`, `w`)
  - **`p`**: `--patch`
  - **`g`**: `--git` (for `d`, `l`, `w`)
  - **`a`**: `--all-remotes` (for `bl`, `gf`) / `--all` (for `gp`)
  - **`i`**: `--interactive`
- value flags (at the end, take an argument):
  - **`r`**: `-r` (revision)
  - **`m`**: `-m` (message)
  - **`c`**: `-c` (change, for `gp`)
  - **`o`**: `-o` (onto, for `rb`)
- multi-command combos and shortcuts:
  - **`ma`** suffix: hardcodes `main` as the target
  - **`jnma`**: `jj new main`
  - **`jrboma`**: `jj rebase -o main`
  - **`jgfn`**: `jj git fetch && jj new`
  - **`jgfnma`**: `jj git fetch && jj new main`
  - **`jgfrbo`**: `jj git fetch && jj rebase -o`
  - **`jgfrboma`**: `jj git fetch && jj rebase -o main`

### How it works

Aliases are built by concatenating parts in order: **base** + **command** + **flags** + **value flag**.

For example, `jlgr` is built from:
- `j` = `jj`
- `l` = `log`
- `g` = `--git`
- `r` = `-r` (takes a value, so it goes last)

Value flags like `-r` and `-m` are placed at the end because they accept an argument. You provide the value after the alias:

```sh
jlr '::@'         # jj log -r '::@'
jcm 'fix bug'     # jj commit -m 'fix bug'
jdem 'refactor'   # jj describe -m 'refactor'
jbsr main         # jj bookmark set -r main
jgpc @            # jj git push -c @
jrbo @-           # jj rebase -o @-
```

### Running the generator

```bash
# Generate aliases for bash/zsh (default)
python3 generate_aliases.py > .jj_aliases

# Generate abbreviations for fish
python3 generate_aliases.py fish > .jj_aliases.fish
```

### Customization

The generator is designed to be forked and customized. Edit the `ops`, `flags`, and `value_flags` lists in `generate_aliases.py` to add or remove commands and flags.

### FAQ

**Doesn't this slow down my shell start up?** Sourcing 81 aliases takes negligible time (under 10ms).

**What about `s` being both `status` and `--summary`?** These never conflict because `--summary` requires a preceding command like `d`, `l`, or `w`. So `js` is always `jj status`, while `jds` is `jj diff --summary`. Similarly, `p` is both `prev` and `--patch`, but `--patch` only applies after `l`, so `jp` is `jj prev` and `jlp` is `jj log --patch`.

**Can I add more commands?** Fork this repo and edit `generate_aliases.py`. The combinatorial generator handles the rest.

### License

[MIT](LICENSE)
