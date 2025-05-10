# Pre-commit Hooks

## Purpose

Pre-commit hooks are automated scripts that run before each commit to ensure code quality and consistency. They act as a first line
of defense against common issues, helping maintain code standards and preventing problematic code from being committed to the
repository.

## Background

Pre-commit hooks are part of Git's hook system, which allows you to trigger custom scripts at key points in your Git workflow.
The [pre-commit framework](https://pre-commit.com/) makes it easy to manage and share these hooks across projects.

Key benefits of using pre-commit hooks:

- Catch issues early in the development process
- Enforce consistent coding standards
- Prevent common mistakes
- Reduce code review burden
- Automate routine checks

## Current Implementation

Our project uses the following pre-commit hooks:

### 1. nbstripout

- **Purpose**: Removes output cells from Jupyter notebooks
- **Why**: Prevents accidental commit of large data outputs or sensitive information in notebooks
- **Documentation**: [nbstripout](https://github.com/kynan/nbstripout)

### 2. ruff

- **Purpose**: Fast Python linter and formatter
- **Implementation**: We use two hooks:
  - `ruff-format`: Formats Python code
  - `ruff`: Performs linting checks
- **Why**: Maintains consistent code style and catches common issues
- **Note**: Our `pyproject.toml` configuration is intentionally permissive to support rapid development
- **Documentation**: [ruff](https://docs.astral.sh/ruff/)

### 3. detect-secrets

- **Purpose**: Scans for secrets and credentials in code
- **Why**: Prevents accidental commit of sensitive information
- **Configuration**: Uses `.secrets.baseline` for known false positives
- **Documentation**: [detect-secrets](https://github.com/Yelp/detect-secrets)

### 4. markdownlint

- **Purpose**: Lints and enforces consistent markdown formatting
- **Why**: Maintains readable documentation with consistent line lengths and formatting
- **Configuration**: Uses [`markdownlint-cli`](https://github.com/igorshubovych/markdownlint-cli) (v0.44.0)
with `.markdownlint.json` and the following rules:
  - `MD013`: Enforces a maximum line length of 132 characters, matching our Python code style
  - `MD024`: Disabled to allow multiple headings with the same text (useful for documentation structure)
  - `MD033`: Disabled to allow inline HTML when needed (e.g., for specific formatting)
  - `MD041`: Disabled to allow content before the first heading (useful for README files)
- **Auto-fixing**: Some issues can be fixed automatically using the `--fix` flag. First install the package:

  ```bash
  npm install -g markdownlint-cli2
  ```

  Then run (targeting only project root and docs directory):

  ```bash
  markdownlint-cli2 "*.md" "docs/**/*.md" --config .markdownlint.json --fix
  ```

  Not all issues (e.g., line length) can be auto-fixed; manual editing may be required for those.
- **Documentation**: [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli)

## Development-Friendly Approach

While we maintain pre-commit hooks for code quality, we've configured them to be development-friendly:

1. **Permissive Ruff Settings**: Our `pyproject.toml` configuration is intentionally lenient, focusing on critical issues while
allowing flexibility during development.
2. **Fast Execution**: All hooks are chosen for their speed to minimize development friction.
3. **Focused Scope**: We only implement hooks that provide clear value without being overly restrictive.
4. **Consistent Line Lengths**: Both Python and Markdown files use a 132-character line length limit for consistency.

## Security Focus

A key aspect of our pre-commit setup is preventing secret leakage:

1. **Notebook Protection**: `nbstripout` removes outputs that might contain sensitive data
2. **Secret Detection**: `detect-secrets` scans for API keys, passwords, and other credentials
3. **Baseline Management**: We maintain a `.secrets.baseline` file to track known false positives

## Potential Additional Hooks

For this modest project, we've kept the hooks minimal but focused. Here are some additional hooks that could be considered
if needed:

1. **isort**: For import sorting (though ruff can handle this)
2. **mypy**: For static type checking (if type hints become more prevalent)
3. **black**: For code formatting (though ruff-format is sufficient)
4. **bandit**: For security linting (if security becomes a bigger concern)
5. **check-added-large-files**: To prevent accidental commit of large files
6. **check-json**: To validate JSON files
7. **check-yaml**: To validate YAML files

## Usage

To use pre-commit hooks:

1. Install pre-commit:

   ```bash
   pip install pre-commit
   ```

2. Install the hooks:

   ```bash
   pre-commit install
   ```

3. Run manually (if needed):

   ```bash
   pre-commit run --all-files
   ```

## References

- [pre-commit Documentation](https://pre-commit.com/)
- [Git Hooks Documentation](https://git-scm.com/docs/githooks)
- [ruff Documentation](https://docs.astral.sh/ruff/)
- [detect-secrets Documentation](https://github.com/Yelp/detect-secrets)
- [nbstripout Documentation](https://github.com/kynan/nbstripout)
- [markdownlint Documentation](https://github.com/igorshubovych/markdownlint-cli)
