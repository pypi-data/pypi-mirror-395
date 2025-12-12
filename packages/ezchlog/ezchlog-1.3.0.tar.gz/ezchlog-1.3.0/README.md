Easy Changelog
==============

Allow to create and merge *part log* files to avoid git conflits or problems with a global **changelog** file.

This is a **command line** (`ezchlog`) tool.

It is available, at your convenance, as a python or rust binary.

You can include it in your CI: see this project as example.

## Installation

### Python version

Install this repository from Pypi:
```sh
pip install ezchlog
```
Or any other means (`pipx`, `uvx` or a package manager).

Python 3.10+ required.

### Rust version

Download a pre-compiled version from [releases](https://gitlab.com/snake_coders/ezchlog/-/releases).

Don’t forget to download the checksum file and check for corruption.  
You should rename the binary to `ezchlog` and place it on your PATH.

You can also compile the `ezchlog` rust binary from source (you should have `rustc` and `cargo` available):
```sh
make release
```

After installation
------------------

Then you’ll have a command to handle your logs:
```sh
ezchlog --help
```

Add a changelog
---------------

```sh
$ ezchlog add "New url for example API"
Changed            new_url_for_example_api
$ ezchlog add -p "Fix example API" Fixed 142
_CHANGELOGS/Fixed/142-fix_example_api.md
```

The file is automatically added to git index unless `--no-git` is used.

Create a git branch
-------------------

If you use `git`, you can automatically create a git branch along the part log file.

For that use the `-b` or `--branch` parameter for the `add` commmand.

```sh
[master] $ ezchlog add -b "Fix example API" Fixed 142
Fixed            142-fix_example_api
[142_fix_example_api] $ 
```

You can configure the branch name using the `branch_format`, `branch_separator` and `branch_lowercase_for` config parameters.

List changelogs
---------------

```sh
$ ezchlog list
Fixed              142-fix_example_api
Changed            new_url_for_example_api
```

```sh
$ ezchlog list -p
_CHANGELOGS/Fixed/142-fix_example_api.md
_CHANGELOGS/Changed/new_url_for_example_api.md
```

Commit with git
---------------

If you use `git`, you can automatically create a git commit with its message using part log files.

By default it will use the only part log file in the **git index** as base for the git commit summary message.

If you have **multiple files** in the index, specify which one is the **main one**, i.e. which one will be use as the summary message.

All part log files in the index will be used in the full git message.

```sh
$ ezchlog commit
[master (root-commit) c0cc282] 142: Fix example API
 2 files changed, 3 insertions(+)
 create mode 100644 _CHANGELOGS/Fixed/142-fix_example_api.md
 create mode 100644 example/api_doc.md
```

The summary message format is `{Ref}: {Title}` if there is a reference, or simply `{Title}`.

- `Title` is the part log first line, without the reference and without any markdown list prefix.
- `Ref` is what is between brackets on the part log first line, with `Ref ` added upfront if the reference start with a sharp `#` (because it’s a comment for git)

Merge changelogs
----------------

```sh
$ ezchlog merge 1.2.3
$ cat CHANGELOG.md
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 1.2.3

### 🔧 Fixed
- Fix example API (142)

### 📝 Changed
- New url for example API
```

Files are automatically updated in the git index unless `--no-git` is used.

You can also add more configuration:

```sh
$ ezchlog merge \
  --with-date \
  --link=https://gitlab.com/snake_coders/ezchlog/-/compare/v1.0.2...v1.1.0 \
  --subtitle "[![](https://gitlab.com/snake_coders/ezchlog/badges/master/coverage.svg)](https://gitlab.com/snake_coders/ezchlog/-/commits/master)" \
  1.1.0
$ cat CHANGELOG.md
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [1.1.0] – 2025-11-07
[1.1.0]: https://gitlab.com/snake_coders/ezchlog/-/compare/v1.0.2...v1.1.0
[![](https://gitlab.com/snake_coders/ezchlog/badges/master/coverage.svg)](https://gitlab.com/snake_coders/ezchlog/-/commits/master)

### 🔧 Fixed
- Fix example API (142)

### 📝 Changed
- New url for example API
```

Configuration
-------------

The following configuration parameters could be specified as environment variables or in a `.ezchlog.toml` file (or `pyproject.toml` file for the python version).

- `EZCHLOG_EDITOR` default to `EDITOR` or `vim`
- `EZCHLOG_LOG_DIR` default to `_CHANGELOGS`
- `EZCHLOG_LOG_FILE` default to `CHANGELOG.md`
- `EZCHLOG_CATEGORY_LIST` default to `Breaking:💣,Security:🛡️,Fixed:🔧,Changed:📝,Added:➕,Removed:➖,Deprecated:⚠️`.
  Use `name:icon` to specify an icon for the category. You can also use it with plain `name` without any icon.
- `EZCHLOG_CATEGORY_DEFAULT` default to `Changed`
- `EZCHLOG_DEFAULT_CHANGELOG` default to  
```
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).
```
- `EZCHLOG_WITH_DATE` default to `False`
- `EZCHLOG_NO_GIT` default to `False`
- `EZCHLOG_BRANCH_FORMAT` default to `%{ref}%{sep}%{name}`, allowed variables: `ref`, `cat`, `name`, `sep`
- `EZCHLOG_BRANCH_SEPARATOR` default to `_`
- `EZCHLOG_BRANCH_LOWERCASE_FOR` default to `cat,name`, allowed variables: `ref`, `cat`, `name`

For `.ezchlog.toml` or `pyproject.toml` config key, use the environment variable name in lowercase without the `EZCHLOG` prefix, for instance `log_dir` or `category_list` keys.

For `pyproject.toml`, the config resides in the `tool.ezchlog` table.
