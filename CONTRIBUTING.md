# Contributing to the Project

Thank you for considering contributing to this project! This document outlines the architecture, folder structure,
development practices, and best practices that govern this project. Following these guidelines ensures consistency,
maintainability, and high-quality contributions.

---

## Architecture Overview

This project follows a **Screaming Architecture** approach, inspired by Clean Architecture principles. The goal is for
the architecture to clearly communicate the intent and purpose of the system through its structure.

### Screaming Architecture

The project is organized around domain concepts, emphasizing:

- **Use Cases**: The application's primary business rules.
- **Domain Objects**: Core entities that represent the problem domain.
- **Connectors**: Interfaces that connect the application to external systems or I/O.

### Dependency Inversion Principle

High-level modules (use cases, domain logic) do not depend on low-level modules (frameworks, connectors).
Instead, both depend on abstractions (protocols/interfaces).

---

## Folder Structure

### **src/**

The `thicker/` directory contains the core implementation.

- **domain/**
  - Holds the fundamental business entities and logic, independent of I/O and frameworks.
  - Example: `domain/thickening.py` contains the domain logic for mesh transformations.

- **use_cases/**
  - Contains application-specific use cases and orchestrates interactions between the domain and connectors.
  - Example: `use_cases/process_thickening.py` implements the workflow for thickening a mesh.

- **adapters/**
  - Implements concrete adapters to interact with external systems like file I/O or databases.
  - Example: `adapters/stl_mesh_reader.py` handles reading STL mesh files.

- **interfaces/**
  - Implements abstract adapters though Protocols bridge between concrete adapters and use cases
to support dependency inversion.
  - Example: `adapters/mesh_reader.py` provided an interface for reading mesh files.

- **cli/**
  - Implements a concrete connector to the command line interface to run use cases, preserving separation of concerns
and dependency inversion.
  - Example: `cli/cli.py` handles reading STL mesh files.

### **tests/**

The `tests/` directory contains all tests, organized to mirror the `thicker/` source structure. Each test module should
comprehensively test its corresponding code. There is also a `tests/utils` folder for utilities and a `fixures` folder
for data fixtures.

### **docs/adrs/**

- **Architectural Decision Records (ADRs)**
  - Each ADR documents a significant architectural decision, including its context, decision, and consequences.
  - ADRs are lightweight and version-controlled.
  - Example: `docs/adrs/0001-choose-screaming-architecture.md`.

---

## Development Practices

### Test-Driven Development (TDD)

We practice TDD to ensure high-quality, maintainable code. Every feature must start with a test:

1. Write a failing test.
2. Write the simplest code to make the test pass.
3. Refactor the code to improve clarity and efficiency.

Tests ensure:

- High code coverage.
- Each feature works as intended.

### Definition of Done

A task is complete when:

- All acceptance criteria are met.
- 100% test coverage is achieved.
- Code adheres to the Screaming Architecture.
- Linting (via `ruff`) and formatting checks pass.
- Code has been reviewed by peers.
- Pre-commit hooks are verified.
- Documentation is updated.
- ADRs are created or updated as necessary.

### Pre-Commit Hooks

Pre-commit hooks automatically validate the codebase before commits. They check for:

- Linting errors.
- Formatting issues.
- Test coverage.

To install pre-commit hooks:

```bash
pre-commit install
```

### Lightweight ADR Practice

When making an architectural decision, document it as an ADR in `docs/adrs/`. Use a consistent format:

- **Title**: `0002-explain-decision.md`
- **Context**: Why was the decision needed?
- **Decision**: What was decided?
- **Consequences**: Implications of the decision.

### Testing Practices

- **Test First**: Write tests before implementing features.
- **Unit Tests**: Test small, isolated pieces of logic.
- **Integration Tests**: Test interactions between components.
- **End-to-End Tests**: Verify that the application works as a whole.
- **Protocol Tests**: Ensure that interfaces comply with their contracts.

### Code Quality

- Follow Python's typing conventions (e.g., `List[Tuple[float, float, float]]`).
- Avoid introducing external libraries into the domain layer.
- Maintain separation of concerns: domain, use cases, and connectors must not bleed responsibilities.
- Write docstrings for all modules, classes, and methods.

### Version Control

- Use feature branches for development.
- Ensure commits are atomic and descriptive.
- Don't squash commits before merging into `main`.

---

## How to Contribute

1. **Work on an Issue**: Make sure there is an Issue for the story or bug or chore you are going to work on.
1. **Fork the Repository**: Create your own fork to work on.
1. **Create a Branch**: Use a descriptive name like `story/10/add-thickening-option` or `bug/20/fix-utf-8`.
1. **Write Tests**: Start by writing tests for the story or bug fix.
1. **Implement Code**: Follow TDD to implement the story.
1. **Run Pre-Commit Hooks**: Validate your code locally before committing.
1. **Submit a Pull Request**: Ensure your PR is linked to an issue (if applicable) and includes a
description of changes.

---

By following these guidelines, you ensure your contributions align with the project's standards and make a meaningful
impact. Thank you for contributing!
