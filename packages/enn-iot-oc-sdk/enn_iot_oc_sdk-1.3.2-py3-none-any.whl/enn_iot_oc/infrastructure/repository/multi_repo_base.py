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
            except Exception:
                pass

        return None

    def list(self) -> List[T]:
        """
        Mock implementation of list() method
        Returns all entities, empty list if table is empty
        """
  
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
            except Exception:
                pass

        # If no mock data, try to initialize from source data
        try:
            source_data = self._load_from_source()
            if source_data and len(source_data) > 0:
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
        except Exception:
            pass

        # Return empty list if no data found
        return []

    def save(self, entity: T) -> None:
        """
        Mock implementation of save() method
        Saves a single entity
        """
    
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
        except Exception as e:
            raise RuntimeError(f"Failed to save entity: {e}")

    def save_all(self, entities: List[T]) -> None:
        """
        Mock implementation of save_all() method
        Saves multiple entities
        """
      
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
        except Exception as e:
            raise RuntimeError(f"Failed to save entities: {e}")

    def _load_from_source(self):
        """
        Load data from source JSON file
        自动发现并加载实体数据，无需硬编码实体列表
        """
        import importlib.resources
        import glob

        # 根据model_code推断可能的源文件名
        possible_file_names = [
            f"{self.model_code}.json",
            f"{self.model_code}.json"
        ]

        # 如果model_code包含下划线，也尝试驼峰命名
        if '_' in self.model_code:
            camel_case = ''.join(word.capitalize() for word in self.model_code.split('_'))
            possible_file_names.extend([
                f"{camel_case}.json",
                f"{camel_case.lower()}.json"
            ])

        # 尝试多个数据源路径
        possible_paths = []

        # 1. 优先尝试当前工作目录下的demo数据路径
        current_dir = os.getcwd()
        base_patterns = [
            f"data/demo/source/{self.model_code}.json",  # 最可能的路径
            f"data/demo/source/{self.model_code}.json",
            f"data/source/{self.model_code}.json",
            f"source/{self.model_code}.json"
        ]

        for file_name in possible_file_names:
            patterns = [pattern.replace(self.model_code + '.json', file_name) for pattern in base_patterns]
            possible_paths.extend(patterns)

        # 2. 使用通配符搜索所有可能的数据文件
        search_patterns = [
            "**/source/*.json",
            "data/**/*.json",
            "**/*.json"
        ]

        for pattern in search_patterns:
            for found_file in glob.glob(pattern, recursive=True):
                if self.model_code in os.path.basename(found_file).lower():
                    possible_paths.append(found_file)

        # 3. 尝试SDK包内的数据
        try:
            import ioc_data_sdk
            sdk_data_dir = os.path.join(os.path.dirname(ioc_data_sdk.__file__), 'data', 'source')
            sdk_files = glob.glob(os.path.join(sdk_data_dir, "*.json"))
            for sdk_file in sdk_files:
                if self.model_code in os.path.basename(sdk_file).lower():
                    possible_paths.append(sdk_file)
        except ImportError:
            pass

        # 4. 按优先级排序路径（demo路径优先，然后是其他路径）
        prioritized_paths = []
        # 先添加data/demo/source路径的文件
        demo_paths = [p for p in possible_paths if "data/demo/source" in p]
        # 再添加其他路径
        other_paths = [p for p in possible_paths if "data/demo/source" not in p]
        prioritized_paths = list(set(demo_paths)) + list(set(other_paths))

        for source_file in prioritized_paths:
            if source_file and os.path.exists(source_file):
                try:
                    with open(source_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    return data
                except Exception:
                    continue

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
        严格匹配主键字段，不支持非主键字段查询
        """
        # If id_field is specified, use only that field
        if self.id_field and self.id_field in item:
            return str(item[self.id_field]) == str(pk)

        # Try common primary key fields (按优先级顺序)
        id_fields = ['id', 'pk', 'primary_key', 'uuid', 'ID', 'Id']

        for field in id_fields:
            if field in item and str(item[field]) == str(pk):
                return True

        # 如果没有找到匹配的主键字段，则不匹配（不支持非主键字段查询）
        return False