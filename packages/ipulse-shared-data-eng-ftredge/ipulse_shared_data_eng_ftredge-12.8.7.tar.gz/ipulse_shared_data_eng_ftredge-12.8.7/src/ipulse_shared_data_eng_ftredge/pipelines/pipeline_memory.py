from typing import Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class PipelineMemory:
    """Class for managing pipeline memory and state.
    A flexible store that can hold any type of data organized by sections and subjects."""

    _data: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def add_section(self, section_name: str) -> None:
        """Create a new section in memory"""
        if section_name not in self._data:
            self._data[section_name] = {}
            
    def set(self, section: str, key: str, value: Any) -> None:
        """Set value in a section"""
        if section not in self._data:
            self.add_section(section)
        self._data[section][key] = value

    def get(self, section: str, key: str) -> Any:
        """Get value from a section"""
        return self._data.get(section, {}).get(key)

    def update(self, section: str, data: Dict[str, Any], merge_nested: bool = True) -> None:
        """Update multiple values in a section.
        
        Args:
            section: Section name to update
            data: Dictionary of data to update
            merge_nested: If True, recursively merge nested dictionaries instead of replacing them
        """
        if section not in self._data:
            self.add_section(section)
            
        if merge_nested:
            self._deep_update(self._data[section], data)
        else:
            self._data[section].update(data)
            
    def _deep_update(self, original: Dict, update: Dict) -> None:
        """Recursively update nested dictionaries"""
        for key, value in update.items():
            if key in original and isinstance(original[key], dict) and isinstance(value, dict):
                self._deep_update(original[key], value)
            else:
                original[key] = value

    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire section"""
        return self._data.get(section, {})

    def clear_section(self, section: str) -> None:
        """Clear a section"""
        if section in self._data:
            self._data[section].clear()

    def remove_section(self, section: str) -> None:
        """Remove a section entirely"""
        if section in self._data:
            del self._data[section]

    def clear_all(self) -> None:
        """Clear all data"""
        self._data.clear()

    # Convenience methods for common operations
    def add_schema(self, schema_name: str, schema: Any) -> None:
        """Add a schema to schemas section"""
        self.set('schemas', schema_name, schema)
        
    def add_schemas_cerberus(self, schema_name: str, schema: Any) -> None:
        """Add a Cerberus schema to schemas_cerberus section"""
        self.set('schemas_cerberus', schema_name, schema)

    def add_secret(self, secret_name: str, value: str) -> None:
        """Add a secret to secrets section"""
        self.set('secrets', secret_name, value)

    def get_schema(self, schema_name: str) -> Any:
        """Get a schema"""
        return self.get('schemas', schema_name)

    def get_schemas_cerberus(self, schema_name: str) -> Any:
        """Get a Cerberus schema"""
        return self.get('schemas_cerberus', schema_name)

    def get_secret(self, secret_name: str) -> Optional[str]:
        """Get a secret"""
        return self.get('secrets', secret_name)