from dataclasses import dataclass, field, is_dataclass, fields
from typing import Any

def summarize_config(config: Any, prefix: str = "") -> dict[str, Any]:
    result = {}
    if is_dataclass(config):
        for f in fields(config):
            value = getattr(config, f.name)
            key = f"{prefix}.{f.name}" if prefix else f.name
            if is_dataclass(value):
                result.update(summarize_config(value, prefix=key))
            else:
                result[key] = value
    else:
        result[prefix] = config
    return result

@dataclass(kw_only=True)
class AddressConfig:
    PrefixLocation: str = "+"
    PrefixProduct: str = "+"
    PrefixInterface: str = "."
    PrefixPin: str = ":"
    EnableLogging: bool = False


@dataclass(frozen=True)
class LoggingConfig:
    DefaultLevel: str = "DEBUG"
    Format: str = "{time} | {level} | {name}:{function}:{line} | {message}"
    DateFormat: str = "%Y-%m-%d %H:%M:%S"
    Filename: str = "module.log"

@dataclass
class FileLoggingLevelsConfig:
    Address: str = "INFO"
    BWAnalysis: str = "DEBUG"

@dataclass
class ConsoleLoggingLevelsConfig:
    Address: str = "DEBUG"
    BWAnalysis: str = "INFO"

@dataclass
class InterfaceConfig:
    """If false, non standard interfaces will generate an error"""
    AllowNonStandardInterfaceNames: bool = False
    """Toggle whether non-standard interface names are logged or not."""
    LogNonStandardInterfaceNames: bool = True
    """Cause interface names to be validated against a standard naming convention."""
    ValidateInterfaceName: bool = True
    """Raised when trying to access a non-existent interface."""
    ErrorOnNonExistentInterface: bool = True
    """Raised when trying to add a duplicate interface."""
    ErrorOnDuplicateInterface: bool = True


@dataclass
class ModuleConfig:
    Address: AddressConfig = field(default_factory=AddressConfig)
    LoggingConfiguration: LoggingConfig = field(default_factory=LoggingConfig)
    FileLoggingLevels: FileLoggingLevelsConfig = field(default_factory=FileLoggingLevelsConfig)
    ConsoleLoggingLevels: ConsoleLoggingLevelsConfig = field(default_factory=ConsoleLoggingLevelsConfig)
    Interface: InterfaceConfig = field(default_factory=InterfaceConfig)

    def summarize(self, do_print=False) -> dict[str, Any]:
        result = summarize_config(self)
        if do_print:
            print(result)
        return result

# Singleton instance for global access
config = ModuleConfig()


if __name__ == "__main__":
    config.summarize(do_print=True)  # Print the configuration summary at module load