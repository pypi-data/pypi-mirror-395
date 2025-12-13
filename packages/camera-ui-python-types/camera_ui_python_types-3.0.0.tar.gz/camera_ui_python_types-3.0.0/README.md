# camera-ui-python-types

Python type definitions for camera.ui ecosystem including camera devices, plugins, detection interfaces, and configuration schemas.

## Installation

```bash
pip install camera-ui-python-types
```

## Purpose

This package provides comprehensive Python type definitions for:

- **Camera Device Management** - Protocol definitions for camera devices and sources
- **Plugin Development** - Type-safe plugin interfaces and abstract base classes
- **Detection Systems** - Motion, object, and audio detection type definitions
- **Configuration Schemas** - JSON schema types for dynamic UI generation  
- **State Management** - Camera state and event type definitions
- **Streaming & Media** - Audio/video codec and streaming type definitions
- **RxPY Integration** - Hybrid observables combining sync/async patterns

## Usage Context

### For Plugin Developers
Provides type safety when developing Python-based camera.ui plugins, ensuring proper implementation of detection algorithms and device integration.

### For Type Checking
Enables static type checking with mypy, pylint, and other Python type checkers for camera.ui related code.

### For IDE Support
Provides full IntelliSense and auto-completion for camera.ui APIs in Python development environments.

## Integration Points

These types are used throughout the Python camera.ui ecosystem:

- **camera-ui-python-common** - Shared utility implementations
- **Python Plugins** - Type-safe plugin development
- **Detection Services** - Motion/object/audio detection implementations
- **Configuration Systems** - Dynamic UI schema generation

## Requirements

- Python 3.10+
- typing-extensions for advanced type features
- RxPY for reactive programming support
- PIL (Pillow) for image type definitions
- Compatible with camera.ui ecosystem packages

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests to our repository.

## License

MIT

---

*Part of the camera.ui ecosystem - A comprehensive camera management solution.*