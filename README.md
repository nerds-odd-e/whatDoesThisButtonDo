# whatDoesThisButtonDo

"WhatDoesThisButtonDo" is a general purpose automated exploratory testing tool using AI assistant.


## Project Goals and Vision**

• This is an open-source project to create a **general-purpose exploratory testing tool augmented by an AI assistant**.

• The primary goals of the tool are:

1\. **Identifying Missing Requirements:** Using exploratory testing to uncover gaps in the application based on provided requirements or test oracles.

2\. **Bug Identification:** Helping users find defects or issues during the testing process.

3\. **Regression Test Discovery:** Identifying test paths that should be repeated later to ensure the stability of the application.

4\. **Efficient Testing:** Supporting a **breadth-first approach** to exploratory testing, prioritizing areas based on time and relevance.


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
