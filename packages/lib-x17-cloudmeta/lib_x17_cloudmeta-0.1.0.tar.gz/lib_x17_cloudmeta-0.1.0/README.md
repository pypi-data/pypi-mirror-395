# lib-x17-cloudmeta

Cloud centre module for x17 ecosystem - A Python library for managing cloud infrastructure metadata and configuration hierarchies.

## Overview

`lib-x17-cloudmeta` provides a structured approach to organizing and managing cloud infrastructure metadata across platforms, environments, packages, and services. It implements a hierarchical configuration system with support for metadata merging, reference resolution, and flexible namespace management.

## Installation

```bash
pip install lib-x17-cloudmeta
```

For development:

```bash
pip install lib-x17-cloudmeta[dev]
```

## Key Features

- **Hierarchical Module System**: Organize infrastructure into Platform → Environ → Package → Service hierarchies
- **Metadata Management**: Parse and manage TOML-based metadata files
- **Configuration Overlay**: Merge configurations across hierarchy levels with reference resolution
- **Namespace Access**: Intuitive dot-notation access to nested configuration values
- **Type-Safe Module Kinds**: Enum-based module type system with case-insensitive matching

## Architecture

### Base Components

#### `File` and `Folder`
Base classes for file system path management with automatic path resolution and validation.

```python
from xcloudmeta.base.file import File
from xcloudmeta.base.folder import Folder

file = File("~/config.toml")
folder = Folder("/path/to/directory")
```

#### `ModuleKind`
Enum for module types: `PLATFORM`, `ENVIRON`, `PACKAGE`, `SERVICE`, `UNDEFINED`

```python
from xcloudmeta.base.modulekind import ModuleKind

kind = ModuleKind.from_str("platform")  # Case-insensitive
assert kind == ModuleKind.PLATFORM
assert kind == "platform"  # String comparison supported
```

### Component Layer

#### `MetaFile`
Manages TOML metadata files with automatic parsing and module kind association.

```python
from xcloudmeta.component.metafile import MetaFile

meta = MetaFile(
    path="pyproject.toml",
    kind="package"
)
data = meta.data  # Parsed TOML content
```

#### `MakeFile`
Represents makefile references within modules.

### Module Layer

#### `Module`
Base class for all infrastructure modules with metadata and makefile support.

```python
from xcloudmeta.module.module import Module

module = Module(
    path="/path/to/module",
    kind="package",
    metafile="package.toml",
    makefile="makefile"
)
```

#### Specialized Modules
- `Platform`: Top-level platform configurations
- `Environ`: Environment-specific configurations
- `Package`: Package/library definitions
- `Service`: Service/application configurations

```python
from xcloudmeta.module.platform import Platform
from xcloudmeta.module.environ import Environ
from xcloudmeta.module.package import Package
from xcloudmeta.module.service import Service

platform = Platform("/path/to/platform", metafile="platform.toml")
environ = Environ("/path/to/environ", metafile="environ.toml")
service = Service("/path/to/service", metafile="service.toml")
```

### Centre Layer

#### `Namespace`
Enhanced SimpleNamespace with dot-notation access, serialization, and nested path support.

```python
from xcloudmeta.centre.namespace import Namespace

# Create from dict
ns = Namespace.from_obj({
    "database": {
        "host": "localhost",
        "port": 5432
    }
})

# Access with dot notation
host = ns.get("database.host")  # "localhost"
port = ns.get("database.port", default=3306)

# Set nested values
ns.set("database.user", "admin")

# Serialize
dict_data = ns.to_dict()
json_str = str(ns)  # JSON formatted
```

#### `Layout`
Manages the file system layout for organizing modules.

```python
from xcloudmeta.centre.layout import Layout

layout = Layout(root="/project/root")

# List all modules
platforms = layout.list_platforms()
environs = layout.list_environs()
packages = layout.list_packages()
services = layout.list_services()
```

Default directory structure:
```
root/
├── platform/
│   ├── plat1/
│   └── plat2/
├── environ/
│   ├── dev/
│   └── prod/
├── package/
│   └── pkg1/
└── service/
    ├── svc1/
    └── svc2/
```

#### `Overlay`
Merges metadata from multiple modules with reference resolution.

```python
from xcloudmeta.centre.overlay import Overlay

overlay = Overlay(
    platform=platform,
    environ=environ,
    service=service
)

# Access merged configuration
compose = overlay.get_compose()
namespace = overlay.get_namespace()

# Get values with dot notation
value = overlay.get("service.name")
overlay.set("custom.key", "value")
```

**Reference Resolution**: Use `{{ ref(path.to.value) }}` in TOML files:

```toml
[platform]
region = "us-west-2"

[environ]
name = "prod"
bucket = "{{ ref(platform.region) }}-{{ ref(environ.name) }}-data"
# Result: "us-west-2-prod-data"
```

#### `Centre`
Main entry point for managing the entire infrastructure hierarchy.

```python
from xcloudmeta.centre.centre import Centre

# Initialize with project root
centre = Centre(root="/project/root")

# Access modules
platform = centre.get_platform("aws")
environ = centre.get_environ("production")
service = centre.get_service("api-gateway")

# Create overlay
overlay = centre.overlay(
    platform="aws",
    environ="production",
    service="api-gateway"
)

# Get merged configuration
config = overlay.get_namespace()
api_url = config.get("service.api.url")
```

## Usage Examples

### Basic Module Setup

```python
from xcloudmeta.module.platform import Platform
from xcloudmeta.module.environ import Environ
from xcloudmeta.module.service import Service

# Define modules
platform = Platform("./platform/aws", metafile="platform.toml")
environ = Environ("./environ/prod", metafile="environ.toml")
service = Service("./service/api", metafile="service.toml")

print(platform.meta)  # Parsed TOML data
print(environ.describe())  # Module description
```

### Configuration Overlay

```python
from xcloudmeta.centre.overlay import Overlay

# Merge configurations
overlay = Overlay(
    platform=platform,
    environ=environ,
    service=service
)

# Access merged config
config = overlay.get_namespace()
db_host = config.get("database.host")
db_port = config.get("database.port")
```

### Full Centre Management

```python
from xcloudmeta.centre.centre import Centre

# Initialize centre
centre = Centre(root="./infrastructure")

# List available modules
print(f"Platforms: {[p.name for p in centre.platforms]}")
print(f"Environs: {[e.name for e in centre.environs]}")
print(f"Services: {[s.name for s in centre.services]}")

# Create overlay
overlay = centre.overlay(
    platform="aws",
    environ="production",
    service="api-gateway"
)

# Access configuration
ns = overlay.get_namespace()
print(ns.to_dict())
```

## Metadata File Format

Metadata files use TOML format:

**platform/aws/platform.toml**:
```toml
[platform]
name = "aws"
region = "us-west-2"
account_id = "123456789012"
```

**environ/prod/environ.toml**:
```toml
[environ]
name = "production"
domain = "{{ ref(platform.name) }}.example.com"

[database]
instance_type = "db.r5.large"
```

**service/api/service.toml**:
```toml
[service]
name = "api-gateway"
port = 8080

[resources]
cpu = "2"
memory = "4Gi"
```

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
ruff check .
ruff format .
```

## Requirements

- Python >= 3.11
- No external runtime dependencies (stdlib only)

## License

MIT License - See LICENSE file for details

## Author

Xing Xing (x.xing.work@gmail.com)

## Project Structure

```
lib-x17-cloudmeta/
├── xcloudmeta/
│   ├── base/           # Base classes (File, Folder, ModuleKind)
│   ├── component/      # Component layer (MetaFile, MakeFile)
│   ├── module/         # Module layer (Platform, Environ, Package, Service)
│   └── centre/         # Centre layer (Centre, Overlay, Layout, Namespace)
├── pyproject.toml
├── README.md
└── environment.yml
```
