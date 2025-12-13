# MeshSync Core Common Library - Python

Shared domain models, value objects, and SQLAlchemy schemas for the MeshSync 3D model marketplace platform.

## Overview

This library provides Python implementations of domain models following Domain-Driven Design (DDD) principles. It includes:

- **Value Objects**: Immutable domain concepts
- **Enums**: Enumerated types for domain states
- **SQLAlchemy Schemas**: Database mappings for persistence

## Installation

```bash
pip install mesh-sync-core-common-lib
```

## Usage

### Importing Value Objects

```python
from mesh_sync_common.generated.model import print_estimates_base
from mesh_sync_common.domain.user import user_preferences
```

### Importing Enums

```python
from mesh_sync_common.generated.model import model_status_base
from mesh_sync_common.generated.storage import storage_provider_type_base
```

### Using SQLAlchemy Schemas

```python
from mesh_sync_common.generated.model.infrastructure import model_schema_base
from mesh_sync_common.generated.user.infrastructure import user_schema_base
```

## Domain Organization

The library is organized by domain:

- **storage**: Storage provider configurations and connections
- **user**: User management and preferences
- **model**: 3D model domain with processing metadata
- **marketplace**: Marketplace listings and integrations
- **catalog**: Model catalog and discovery

## Generated Code

This library is auto-generated from YAML schema definitions using the MeshSync schema generator. Do not edit generated files directly - modify the source YAML schemas instead.

## Type Safety

All code is fully typed with mypy strict mode enabled.

## License

MIT
