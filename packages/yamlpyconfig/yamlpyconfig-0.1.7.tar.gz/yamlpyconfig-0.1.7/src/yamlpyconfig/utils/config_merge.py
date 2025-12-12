from typing import Dict, Any


class ConfigMerge:

    @staticmethod
    def deep_merge(base: Dict[str, Any], override: Dict[str, Any], list_merge: bool = False):
        """
        Deep merge two dictionaries.

        Args:
            base: Base dictionary (will be modified)
            override: Override dictionary
            list_merge: merge list info
        """
        for key, value in override.items():
            if key in base:
                if isinstance(base[key], dict) and isinstance(value, dict):
                    # Both are dicts, merge recursively
                    ConfigMerge.deep_merge(base[key], value, list_merge)
                elif isinstance(base[key], list) and isinstance(value, list) and list_merge:
                    # Both are lists, merge them
                    base[key] += value
                else:
                    # Override with new value
                    base[key] = value
            else:
                # New key, add it
                base[key] = value