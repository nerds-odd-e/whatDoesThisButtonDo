# whatDoesThisButtonDo

An open-source AI-powered exploratory testing assistant that helps automate and enhance software testing processes.

## Description

This project leverages AI capabilities to perform exploratory testing on software applications, helping testers and developers identify potential issues and edge cases more efficiently.

## Prerequisites

- [Nix package manager](https://nixos.org/download.html)
- Git

## Getting Started

1. Start a nix-shell:

```bash
nix develop
```

2. Run tests:

```bash
make
# or
make test
```

This will run the AI-powered exploratory testing on the `test` folder.

## Development

### Code Style

We use `ruff` for code linting and formatting. To check your code:

```bash
ruff check .
```

To automatically fix issues:

```bash
ruff check --fix .
```

Note: `ruff check --fix .` will:
- Automatically fix issues that can be fixed
- Return a non-zero exit code if there are remaining issues
- Display any issues that need manual fixing
