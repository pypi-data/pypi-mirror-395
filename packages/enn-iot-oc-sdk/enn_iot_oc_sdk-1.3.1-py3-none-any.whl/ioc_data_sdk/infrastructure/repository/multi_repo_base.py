"""
Mock Multi Repository Base Class
Implements MultiRepository interface for multi-row entities
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Dict, Any
import os
import json

T = TypeVar('T')

class MultiRepoBase(Generic[T], ABC):
    """
    Mock base class for multi-row repositories
    Provides find_by_id(), list(), save(), and save_all() methods as specified in the reference SDK
    """

    def __init__(self, model_code: str, eo_id: str = "", instance_id: str = "", id_field: str = None):
        """
        Initialize repository with model code and context
        """
        self.model_code = model_code
        self.eo_id = eo_id
        self.instance_id = instance_id
        self.id_field = id_field
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

    def find_by_id(self, pk: str) -> Optional[T]:
        """
        Mock implementation of find_by_id() method
        Returns entity with given primary key or None if not found
        """
        print(f"[MOCK] Finding entity by ID '{pk}' for model: {self.model_code}")

        # Try to load mock data
        if os.path.exists(self._data_file):
            try:
                with open(self._data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        # Find by primary key (assuming first string field or 'id')
                        for item in data:
                            if self._matches_id(item, pk):
                                return self.to_domain(item)
                    else:
                        # Single item case
                        if self._matches_id(data, pk):
                            return self.to_domain(data)
            except Exception as e:
                print(f"[MOCK] Error loading data: {e}")

        print(f"[MOCK] No entity found with ID '{pk}'")
        return None

    def list(self) -> List[T]:
        """
        Mock implementation of list() method
        Returns all entities, empty list if table is empty
        """
        print(f"[MOCK] Listing all entities for model: {self.model_code}")

        # Try to load mock data first
        if os.path.exists(self._data_file):
            try:
                with open(self._data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        return [self.to_domain(item) for item in data]
                    elif data:
                        # Single item case, wrap in list
                        return [self.to_domain(data)]
            except Exception as e:
                print(f"[MOCK] Error loading mock data: {e}")

        # If no mock data, try to initialize from source data
        try:
            source_data = self._load_from_source()
            if source_data and len(source_data) > 0:
                print(f"[MOCK] Loaded {len(source_data)} records from source data")
                # Process each record with relationship loading
                entities = []
                for record in source_data:
                    converted_record = self._convert_field_names(record)
                    # Load related data for this record
                    record_with_relations = self._load_related_data(converted_record)
                    entity = self.to_domain(record_with_relations)
                    entities.append(entity)

                # Auto-save for future queries
                self.save_all(entities)
                return entities
        except Exception as e:
            print(f"[MOCK] Error loading source data: {e}")

        # Return empty list if no data found
        print(f"[MOCK] No data found for {self.model_code}, returning empty list")
        return []

    def save(self, entity: T) -> None:
        """
        Mock implementation of save() method
        Saves a single entity
        """
        print(f"[MOCK] Saving single entity for model: {self.model_code}")

        data = self.from_domain(entity)
        current_data = []

        # Load existing data
        if os.path.exists(self._data_file):
            try:
                with open(self._data_file, 'r', encoding='utf-8') as f:
                    current_data = json.load(f)
                    if not isinstance(current_data, list):
                        current_data = [current_data] if current_data else []
            except Exception:
                current_data = []

        # Add new entity
        current_data.append(data)

        # Save back
        try:
            with open(self._data_file, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, ensure_ascii=False, indent=2)
            print(f"[MOCK] Successfully saved entity to {self._data_file}")
        except Exception as e:
            print(f"[MOCK] Error saving data: {e}")
            raise RuntimeError(f"Failed to save entity: {e}")

    def save_all(self, entities: List[T]) -> None:
        """
        Mock implementation of save_all() method
        Saves multiple entities
        """
        print(f"[MOCK] Saving {len(entities)} entities for model: {self.model_code}")

        # Convert all entities to dict
        data_list = [self.from_domain(entity) for entity in entities]

        # Load existing data
        current_data = []
        if os.path.exists(self._data_file):
            try:
                with open(self._data_file, 'r', encoding='utf-8') as f:
                    current_data = json.load(f)
                    if not isinstance(current_data, list):
                        current_data = [current_data] if current_data else []
            except Exception:
                current_data = []

        # Append new data
        current_data.extend(data_list)

        # Save back
        try:
            with open(self._data_file, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, ensure_ascii=False, indent=2)
            print(f"[MOCK] Successfully saved {len(entities)} entities to {self._data_file}")
        except Exception as e:
            print(f"[MOCK] Error saving data: {e}")
            raise RuntimeError(f"Failed to save entities: {e}")

    def _load_from_source(self):
        """
        Load data from source JSON file
        """
        # Map model code to source file
        source_files = {
            "biogas_project_information": "data/demo/source/biogas_project_information.json",
            "mechanism_cloud_algorithm": "data/demo/source/mechanism_cloud_algorithm.json",
            "mechanism_task_planning": "data/demo/source/mechanism_task_planning.json"
        }

        source_file = source_files.get(self.model_code)
        if source_file and os.path.exists(source_file):
            try:
                with open(source_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"[MOCK] Loaded source data from {source_file}")
                return data
            except Exception as e:
                print(f"[MOCK] Error loading source file {source_file}: {e}")

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

    def _load_related_data(self, record_data):
        """
        Load related data for entities with relationships
        Override in specific repository implementations as needed
        """
        return record_data

    def _matches_id(self, item: Dict[str, Any], pk: str) -> bool:
        """
        Helper method to check if item matches given primary key
        """
        # If id_field is specified, try that first
        if self.id_field and self.id_field in item:
            return str(item[self.id_field]) == str(pk)

        # Try common primary key fields
        id_fields = ['id', 'pk', 'primary_key', 'uuid']

        for field in id_fields:
            if field in item and str(item[field]) == str(pk):
                return True

        # Try any string field as fallback
        for value in item.values():
            if isinstance(value, str) and value == pk:
                return True

        return False