"""
Mock Single Repository Base Class
Implements SingleRepository interface for single-row entities
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, Dict, Any
import os
import json

T = TypeVar('T')

class SingleRepoBase(Generic[T], ABC):
    """
    Mock base class for single-row repositories
    Provides find() and save() methods as specified in the reference SDK
    """

    def __init__(self, model_code: str, eo_id: str = "", instance_id: str = ""):
        """
        Initialize repository with model code and context
        """
        self.model_code = model_code
        self.eo_id = eo_id
        self.instance_id = instance_id
        self._data_file = f"mock_data_{model_code}.json"

    @abstractmethod
    def to_domain(self, row: Dict[str, Any]) -> T:
        """Convert database row to domain model"""
        pass

    @abstractmethod
    def from_domain(self, entity: T) -> Dict[str, Any]:
        """Convert domain model to database row"""
        pass

    @abstractmethod
    def empty_object(self) -> T:
        """Create empty domain object"""
        pass

    def find(self) -> Optional[T]:
        """
        Mock implementation of find() method
        Returns the single-row entity or None if not found
        """
        print(f"[MOCK] Finding single row for model: {self.model_code}")

        # Try to load mock data first
        if os.path.exists(self._data_file):
            try:
                with open(self._data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data:
                        return self.to_domain(data)
            except Exception as e:
                print(f"[MOCK] Error loading mock data: {e}")

        # If no mock data, try to initialize from source data
        try:
            source_data = self._load_from_source()
            if source_data:
                print(f"[MOCK] Loaded {len(source_data)} records from source data")
                # For single entity, take the first record
                if len(source_data) > 0:
                    entity = self.to_domain(self._convert_field_names(source_data[0]))
                    # Auto-save for future queries
                    self.save(entity)
                    return entity
        except Exception as e:
            print(f"[MOCK] Error loading source data: {e}")

        # Return empty object if no data found
        print(f"[MOCK] No data found for {self.model_code}, returning None")
        return None

    def _load_from_source(self):
        """
        Load data from source JSON file
        """
        import importlib.resources

        # Map model code to source file
        source_files = {
            "biogas_project_information": "biogas_project_information.json",
            "mechanism_cloud_algorithm": "mechanism_cloud_algorithm.json",
            "mechanism_task_planning": "mechanism_task_planning.json"
        }

        # 尝试多个数据源路径
        possible_paths = []

        # 1. 首先尝试当前目录下的原始路径
        current_dir_paths = {
            "biogas_project_information": "data/demo/source/biogas_project_information.json",
            "mechanism_cloud_algorithm": "data/demo/source/mechanism_cloud_algorithm.json",
            "mechanism_task_planning": "data/demo/source/mechanism_task_planning.json"
        }

        # 2. 尝试SDK包内的数据
        try:
            import ioc_data_sdk
            sdk_data_dir = os.path.join(os.path.dirname(ioc_data_sdk.__file__), 'data', 'source')
            sdk_paths = {
                "biogas_project_information": os.path.join(sdk_data_dir, "biogas_project_information.json"),
                "mechanism_cloud_algorithm": os.path.join(sdk_data_dir, "mechanism_cloud_algorithm.json"),
                "mechanism_task_planning": os.path.join(sdk_data_dir, "mechanism_task_planning.json")
            }
            possible_paths.extend([sdk_paths.get(self.model_code)])
        except ImportError:
            pass

        # 3. 尝试使用importlib.resources
        try:
            with importlib.resources.path("ioc_data_sdk.data.source", source_files.get(self.model_code, "")) as p:
                if p.exists():
                    possible_paths.append(str(p))
        except (ImportError, FileNotFoundError):
            pass

        # 4. 最后尝试当前目录下的路径
        possible_paths.append(current_dir_paths.get(self.model_code))

        # 尝试所有可能的路径
        for source_file in possible_paths:
            if source_file and os.path.exists(source_file):
                try:
                    with open(source_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    print(f"[MOCK] Loaded source data from {source_file}")
                    return data
                except Exception as e:
                    print(f"[MOCK] Error loading source file {source_file}: {e}")
                    continue

        print(f"[MOCK] Source file not found for {self.model_code}")
        return None

    def _convert_field_names(self, record):
        """
        Convert field names from source format to storage format
        """
        # This handles camelCase to snake_case conversion
        converted = {}
        for key, value in record.items():
            # Simple conversion: insert underscore before capital letters
            snake_key = ''.join(['_' + c.lower() if c.isupper() else c for c in key]).lstrip('_')
            converted[snake_key] = value
        return converted

    def save(self, entity: T) -> None:
        """
        Mock implementation of save() method
        Saves the single-row entity
        """
        print(f"[MOCK] Saving entity for model: {self.model_code}")

        # Convert to dict and save
        data = self.from_domain(entity)
        try:
            with open(self._data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[MOCK] Successfully saved entity to {self._data_file}")
        except Exception as e:
            print(f"[MOCK] Error saving data: {e}")
            raise RuntimeError(f"Failed to save entity: {e}")