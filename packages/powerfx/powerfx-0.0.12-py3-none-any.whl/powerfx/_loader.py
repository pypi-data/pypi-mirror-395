import sys
from importlib import resources
from pathlib import Path

_loaded_key = "_powerfx_loaded"

# fix_clr_loader.py
"""
Patches clr_loader to support .NET 10+ (double-digit major versions).

This must be imported BEFORE any imports that trigger pythonnet/clr_loader,
such as `from powerfx import Engine` or `from agent_framework.declarative import AgentFactory`.

Bug reference: https://github.com/pythonnet/clr-loader/blob/main/clr_loader/util/runtime_spec.py
"""


def apply_patch():
    """
    Patches DotnetCoreRuntimeSpec.floor_version to correctly parse
    versions like "10.0.0" instead of producing "10..0".
    """
    print("Applying patch called")
    try:
        from clr_loader.util.runtime_spec import DotnetCoreRuntimeSpec  # type: ignore
    except ImportError:
        print("Warning: clr_loader not installed, skipping patch")
        return False

    # Store original for reference (optional, useful for debugging)
    _original_floor_version = DotnetCoreRuntimeSpec.floor_version.fget

    def _fixed_floor_version(self) -> str:
        """
        Returns the floor version (major.minor) for runtime config.
        Original implementation used string slicing [:3] which breaks
        for double-digit major versions like "10.0.0".
        Examples:
            "8.0.0"  -> "8.0"
            "9.0.0"  -> "9.0"
            "10.0.0" -> "10.0"
            "10.0.4" -> "10.0"
        """
        print(f"Inside Applying patch for version: {self.version}")
        parts = self.version.split(".")
        if len(parts) >= 2:
            return f"{parts[0]}.{parts[1]}"
        # Fallback to original behavior for unexpected formats
        return _original_floor_version(self)

    # Replace the property with our fixed version
    DotnetCoreRuntimeSpec.floor_version = property(_fixed_floor_version)
    return True


# Auto-apply when imported
_patched = apply_patch()

if _patched:
    print("✓ Applied clr_loader patch for .NET 10+ compatibility")


def load() -> None:
    """
    Ensure Microsoft.PowerFx assemblies are loadable via pythonnet (CoreCLR).

    Precedence for dll_dir:
    - explicit arg
    - env var POWERFX_DLL_DIR
    - <pkg>/runtime (optional fallback)
    """
    if getattr(sys.modules[__name__], _loaded_key, False):
        return

    base = _bundled_dir()
    if not base.is_dir():
        raise RuntimeError(f"Power Fx DLL directory '{base}' does not exist.")

    # Select CoreCLR BEFORE any clr import
    import pythonnet  # type: ignore

    pythonnet.load("coreclr")

    import clr  # type: ignore

    # Make sure PowerFx DLL folder is in probing paths
    if base not in sys.path:
        sys.path.append(str(base))

    # Load ONLY the PowerFx assemblies you ship; let CoreCLR resolve System.* deps.
    for name in ("Microsoft.PowerFx.Core", "Microsoft.PowerFx.Interpreter", "Microsoft.PowerFx.Transport.Attributes"):
        try:
            clr.AddReference(name)
        except Exception as ex:
            # Fallback to explicit path if name load fails
            print(f"Failed to load '{name}' by name, trying explicit path. Exception: {ex}")
            raise

    setattr(sys.modules[__name__], _loaded_key, True)


def _bundled_dir() -> Path:
    """
    Return the path to the bundled PowerFx assemblies inside this package.
    """
    return Path(str(resources.files("powerfx") / "_bundled")).resolve()
