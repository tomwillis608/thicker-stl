# Use Protocol-Based Abstract Interface Definitions

## Status

Accepted

## Context

The `MeshReader` and `MeshWriter` interfaces are crucial components of the application, allowing the system to abstract
the reading and writing of mesh files from their specific implementations. To adhere to the principles of dependency
inversion and clean architecture, these interfaces need to:

1. Enable flexibility to replace or extend mesh file formats.
2. Simplify testing by allowing mocks or stubs to stand in for concrete implementations.
3. Prevent direct dependencies on file formats (e.g., STL) within the domain and use case layers.

Initially, there was a consideration to combine the reading and writing logic into a single "MeshIO" class. However,
this approach would have resulted in unnecessary coupling between reading and writing responsibilities and potentially
violated the Single Responsibility Principle (SRP).

## Decision

The `MeshReader` and `MeshWriter` will remain distinct protocol-based interfaces, defined as separate components under
the `adapters` folder. Further, this patter will be used as needed for other abstract interfaces that emerge in the
project. These abstract interfaces will:

- Be defined as `typing.Protocol` types.
- Clearly specify the required methods for reading and writing operations.
- Serve as contracts that concrete implementations (e.g., `STLMeshReader`, `STLMeshWriter`) must fulfill.

## Implications

### Architectural Alignment

- **Dependency Inversion:** The `MeshReader` and `MeshWriter` interfaces are injected into use cases, ensuring the
domain and use case layers are agnostic of file format details.
- **Testability:** Mock or stub implementations can easily replace the concrete adapters during testing, enabling
isolated and faster tests.
- **Flexibility:** Future extensions for new file formats (e.g., OBJ, PLY) only require creating new adapter
implementations without modifying the core logic.

### Folder Placement

The protocol definitions are located in `adapters/mesh_reader_writer.py`, separate from their concrete implementations
(e.g., `STLMeshReader` and `STLMeshWriter`), which reside in `adapters/stl_mesh_reader.py`
and `adapters/stl_mesh_writer.py`.

## Consequences

### Advantages

1. **Single Responsibility:** Separate reader and writer protocols maintain clear and independent responsibilities.
1. **Extensibility:** Adding support for new formats (e.g., OBJ) requires minimal changes to the system.
1. **Alignment with Clean Architecture:** The interfaces respect the Dependency Rule, keeping outer layers dependent on
abstractions rather than implementations.

### Potential Drawbacks

1. **Increased Boilerplate:** Defining and maintaining separate protocols adds slight overhead.
1. **Potential Misuse:** Developers may inadvertently create implementations that couple reader and writer logic unless
carefully documented and enforced.

## Alternatives Considered

- **Combining `MeshReader` and `MeshWriter` into a single `MeshIO` interface:**
  - Rejected to avoid violating SRP and increasing coupling.
- **Direct dependency on concrete implementations:**
  - Rejected to maintain testability and flexibility.

## Examples

### Protocol Definition Example

```python
from typing import Protocol

class MeshReader(Protocol):
    def read(self, file_path: str) -> object:
        """Reads a mesh from a file and returns a domain object."""
        ...

class MeshWriter(Protocol):
    def write(self, mesh: object, file_path: str) -> None:
        """Writes a domain object to a mesh file."""
        ...
```

### Concrete Implementation Example

```python
from .mesh_reader_writer import MeshReader, MeshWriter

class STLMeshReader:
    def read(self, file_path: str) -> object:
        # Implementation for reading STL files
        pass

class STLMeshWriter:
    def write(self, mesh: object, file_path: str) -> None:
        # Implementation for writing STL files
        pass
```

## Decision Owner

Tom Willis

## Date

2024-12-20
