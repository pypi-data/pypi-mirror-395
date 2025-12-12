# Contributing to `wriftai-python`

Thank you for your interest in contributing to wriftai-python. This guide will help you get started with the contribution process.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](/CODE_OF_CONDUCT.md) By participating, you are expected to uphold this code.

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/wriftai/wriftai-python/issues

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs.
Anything tagged with "bug" and "help wanted" is open to whoever wants to implement a fix for it.

### Implement Features

Look through the GitHub issues for features.
Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Write Documentation

wriftai-python could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/wriftai/wriftai-python/issues.

If you are proposing a new feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.

## Getting Started

Please note this documentation assumes you already have `python`, [`uv`](https://docs.astral.sh/uv/getting-started/installation/) and `git` installed.

1. Fork the `wriftai-python` repo on GitHub.

2. Clone your fork locally:

```bash
git clone git@github.com:your-username/wriftai-python.git
cd wriftai-python
```

3. Setup environment

```bash
make install
```

4. Run all quality control checks

```bash
make check
```

5. Run unit and integration tests:

```bash
make test
```

More specific recipes can be found in the [Makefile](./Makefile).

## Development Workflow

1. Create a new branch for your changes:
   ```bash
   git checkout -b type/description
   # Example: git checkout -b feat/predictions-async
   ```
2. Make your changes following the code style guidelines
3. Add tests for your changes
4. Run the checks and test suite:
   ```bash
   make check && make test
   ```
5. Commit your changes with a descriptive message following this format:

   ```
   fix: fix incorrect prediction polling

   Issue: <issue url>
   ```

   Commit messages should be well formatted, and to make that "standardized", use Conventional Commits. You can follow the documentation on [their website](https://www.conventionalcommits.org).

7. Push your branch to your fork
8. Open a pull request. In your PR description:
   - Clearly describe what changes you made and why
   - Include any relevant context or background
   - List any breaking changes or deprecations
   - Reference related issues or discussions

## Documentation Guidelines

All documentation files can be found in the [`docs/`](./docs/) directory. Whenever changes are made to the codebase ensure that all relevant documentation is updated accordingly. Each file in this directory must be a valid `.md` or `.mdx` file.

### Front Matter

Each Markdown file must include a front matter block as required by WriftAI's official documentation:

```md
---
title: Models
description: API documentation for Models.
---
```

Front matter is automatically added to all auto-generated files in `docs/references/`.
Other sections of the `docs` folder are written manually — authors must ensure those files include valid front matter with a clear `title` and `description`.


### Python API References

We automatically generate Python API reference documentation that is **used by the official WriftAI documentation**.

#### How It Works

1. **Sphinx + autodoc** generates Markdown files from the Python source code.
2. On every push or pull request to `main`, the CI workflow:

   * Runs `make-docs` to regenerate API reference files.
   * Fails if generated files differ from the committed ones, ensuring that API references are always up to date.


#### Local Commands

```bash
# Generate API reference docs (run before committing)
make docs
```

Run this command whenever you make changes to APIs to keep the generated documentation in sync.

#### Known Issues

While our documentation pipeline is stable, a few formatting and inheritance-related issues exist upstream in Sphinx and its extensions. These are tracked in open GitHub issues and pull requests:

1. **Overload signature rendering issue**
  The `*` used for keyword-only parameters in overloaded functions may be omitted in the rendered documentation.\
  [GitHub issue](https://github.com/liran-funaro/sphinx-markdown-builder/issues/42)

2. **Type hint formatting in docstrings**
  When using **`sphinx.ext.napoleon`** with *Google-style docstrings*, certain complex type hints (for example, `Optional[str]` or `Optional[dict[str, Any]]`) may be rendered incorrectly in the generated Markdown output — appearing as something like:
   ```
   (Optional *[*str])
   ``` 
   in the parameters section.\
  [GitHub issue](https://github.com/liran-funaro/sphinx-markdown-builder/issues/43)\
  *Current workaround:* wrap the type in backticks within the docstring, for example:

   ```markdown
   Args:
      name (`Optional[str]`): The optional name of the user.
   ```
   **Important caveat:**
   * Only wrap types in backticks for standard Python types or external types.
   * Do not add backticks around internal or project-specific types if you want Sphinx to generate proper cross-references. Wrapping internal types in backticks will break the ability to link them in the docs.

3. **Missing docstrings for inherited attributes**
  Attributes inherited from parent classes appear in subclass documentation, but their docstrings are not included.
  This is a known Sphinx autodoc limitation currently under review.\
  [GitHub issue](https://github.com/sphinx-doc/sphinx/issues/9290) . [Related PR](https://github.com/sphinx-doc/sphinx/pull/10806)

4. **Unlinked type aliases in autodoc output**
   Recursively defined type aliases (e.g., `JsonValue`) are rendered in the documentation as their full expanded form—such as `list[JsonValue] | Mapping[str, JsonValue] | str | bool | int | float | None`—rather than simply as `JsonValue`. While quoting the alias (e.g., `"JsonValue"`) allows it to resolve correctly, it does not link to its definition. This issue has been fixed upstream but has not yet been included in a Sphinx release (merged on **August 5, 2025**; last release was in **March 2025**).  \
   [GitHub Issue](https://github.com/sphinx-doc/sphinx/issues/10785) . [Related PR](https://github.com/sphinx-doc/sphinx/pull/13808)

5. **Incorrect base classes for `TypedDict` subclasses on Python < 3.12**
   When generating documentation with Python versions earlier than 3.12, classes that inherit from another class based on `TypedDict` (for example, `PredictionWithIO(Prediction)`) incorrectly display their base as `dict` instead of the actual parent class.
   This occurs because Python 3.12 (via PEP 692) makes TypedDict a proper base class, fixing inheritance display in documentation.\
   [Python 3.12 changelog – PEP 692](https://docs.python.org/3/whatsnew/3.12.html#pep-692-using-typed-dict-as-a-base-class)\
   *Current workaround:* generate documentation using Python 3.12 or later, where `TypedDict` is a proper base class and inheritance is resolved correctly.

## Releases

We use [**Release Please**](https://github.com/googleapis/release-please) to automate versioning and changelog generation. More information [here](https://elixirschool.com/blog/managing-releases-with-release-please).

- **Do not manually bump versions or edit the changelog.**
- When pull requests are merged into `main`, Release Please will:
  - Update the changelog and package version automatically.
  - Create a **release PR** when there are user-facing changes based on the [conventional commit prefix](https://www.conventionalcommits.org). The most important prefixes you should have in mind are:
    - fix: which represents bug fixes, and correlates to a SemVer patch.
    - feat: which represents a new feature, and correlates to a SemVer minor.
    - feat!:, or fix!:, refactor!:, etc., which represent a breaking change (indicated by the !) and will result in a SemVer major.
- Once the release PR is merged, a GitHub Release is created and the package is automatically **published to PYPI** from CI.
