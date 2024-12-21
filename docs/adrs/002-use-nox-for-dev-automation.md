# Architectural Decision Record:  Use Nox for Developer Automation

## Status

Accepted

## Context

In this project, we need to manage both production and development dependencies separately. We want to ensure that:

Production dependencies are separated from development dependencies.
Developers can easily update and generate requirements.txt and requirements-dev.txt files.
The process for generating the requirements files should be automated to minimize human error.

## Decision

We will use Nox to automate the process of generating requirements.txt and requirements-dev.txt files from the .in
files. The pip-tools package will be used within Nox sessions to compile these files.

- requirements.in will include production dependencies.
- requirements-dev.in will include both production dependencies (via -r requirements.in) and development dependencies.
- Nox will handle the generation of both requirements.txt and requirements-dev.txt files using the pip-compile command.

We will also use Nox to automate the other developer build processes

- ## Consequences

Developers must use the Nox sessions to generate or update the requirements files.
Dependencies will be version-locked using pip-tools, ensuring that the environment is reproducible.
The process for updating and installing dependencies is centralized and automated, reducing the risk of mismatched or
forgotten dependencies.
