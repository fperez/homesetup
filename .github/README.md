# Scaffolding setup for a git-controlled HOME directory

This repository aims to make it very easy to setup a home directory on a new system according to my preferences.  It uses the same pattern of working off a bare git repo as my [related dotfiles repo](https://github.com/fperez/dotfiles). As such, it does _not_ contain any top-level non-hidden files like README.md or LICENSE to ensure that it can be cloned as a bare repo in your home directory to track all your desired config, without cluttering your home directory with extraneous files.

## Start using this repo

First, **fork this repository to your personal github account**.

You should review the resulting fork and remove any code you don't want or neeed. This repo contains _my_ `$HOME` setup, and you are welcome to use it as a starting point, but you are likely to prefer something else.

Note that you can conveniently use GitHub's web editor, accessed via the `.` (dot/period) key, to edit the repo on the web before you make a local clone.  Alternatively, first make a local clone in a throw-away location, do your preferred cleanup there, and then proceed with the next section where you'll make a bare repo clone for actual usage.

### Clone your fork as a `bare` repository

The main advantage of this setup is that you can directly clone its contents into your `$HOME` directory, without having a top-level `.git/` folder that would be detected by any recursive git operation, making every folder in your system behave as if it was under version control. For that to work, you need to do something sligthly unusual: to clone the repo as a _bare_ repo and set your working directory to be `$HOME`:

> :warning: In the below, replace **`<username>`** with your github handle (this assumes you forked the repository as indicated above)

```bash
git clone --bare https://github.com/<username>/homesetup.git $HOME/.homesetup
````

Bare repositories do not have a working tree in their normal directory, instead they only contain the raw data, and we'll be using as our working tree `$HOME` itself. For this to work, whenever operating on this repo, your `git` call must _always_ include these two flags:

- `--work-tree` - this can be your home directory, i.e., `$HOME` or `~`.
- `--git-dir` - where the repository is cloned - `$HOME/.homesetup`.

For convenience, we will alias this in our `.bashrc`  file as:

```bash
alias ghome='git --git-dir=$HOME/.homesetup --work-tree=$HOME'
```

From now on, **instead of typing `git` you will type `ghome` to operate on this special repo**.

### Once cloned, check out the main branch into `$HOME`

You can now checkout the main branch into `$HOME`, to get the working copy of your files 

```bash
ghome switch main
```

or if you didn't add the `ghome` alias as above, using the long form:

```bash
git --git-dir=$HOME/.homesetup --work-tree=$HOME switch main
```

> :warning: The command `ghome status` will show all the untracked files, which in your home directory is likely a lot. To disable this behavior, use:
>
> ```bash 
> # remove untracked files and directories from git status listings
> ghome config --local status.showUntrackedFiles no 
> ```

That's it, enjoy git-managed `$HOME` scaffolding!
