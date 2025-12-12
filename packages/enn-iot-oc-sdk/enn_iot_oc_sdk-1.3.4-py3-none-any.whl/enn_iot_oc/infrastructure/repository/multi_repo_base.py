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
        优化版本：优先从SDK包内加载，避免递归搜索
        """
        # 根据model_code推断可能的源文件名
        possible_file_names = [
            f"{self.model_code}.json",
        ]

        # 如果model_code包含下划线，也尝试驼峰命名
        if '_' in self.model_code:
            camel_case = ''.join(word.capitalize() for word in self.model_code.split('_'))
            possible_file_names.extend([
                f"{camel_case}.json",
                f"{camel_case.lower()}.json"
            ])

        # 尝试多个数据源路径（按优先级排序）
        possible_paths = []

        # 1. 最优先：尝试从SDK包内的数据目录加载
        try:
            import ioc_data_sdk
            sdk_data_dir = os.path.join(os.path.dirname(ioc_data_sdk.__file__), 'data', 'source')
            if os.path.exists(sdk_data_dir):
                for file_name in possible_file_names:
                    sdk_file = os.path.join(sdk_data_dir, file_name)
                    if os.path.exists(sdk_file):
                        possible_paths.append(sdk_file)
        except ImportError:
            pass

        # 2. 其次：尝试当前工作目录下的特定路径（不使用递归搜索）
        specific_paths = [
            f"data/demo/source/{self.model_code}.json",
            f"data/source/{self.model_code}.json",
            f"source/{self.model_code}.json",
            f"ioc_data_sdk/data/source/{self.model_code}.json",
        ]

        for file_name in possible_file_names:
            for base_path in specific_paths:
                path = base_path.replace(f"{self.model_code}.json", file_name)
                if os.path.exists(path):
                    possible_paths.append(path)

        # 3. 作为最后手段：限制深度的搜索（最多搜索3层，避免性能问题）
        # 只在前两种方法都失败时使用
        if not possible_paths:
            import glob
            # 限制搜索深度和范围
            limited_patterns = [
                "data/*/source/*.json",  # 只搜索 data/*/source 目录
                "*/data/source/*.json",  # 只搜索 */data/source 目录
            ]

            for pattern in limited_patterns:
                try:
                    for found_file in glob.glob(pattern, recursive=False):
                        if self.model_code in os.path.basename(found_file).lower():
                            if os.path.exists(found_file):
                                possible_paths.append(found_file)
                except Exception:
                    continue

        # 去重并尝试加载
        for source_file in list(set(possible_paths)):
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