import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any

try:
    from vectorwave.search.execution_search import search_executions
except ImportError:
    search_executions = None


class BaseSource(ABC):
    @abstractmethod
    def fetch_data(self, func_name: str, limit: int) -> List[Dict[str, Any]]:
        pass


class DBReplaySource(BaseSource):
    def fetch_data(self, func_name: str, limit: int) -> List[Dict[str, Any]]:
        if not search_executions:
            raise RuntimeError("VectorWave library not found. Cannot use DB source.")

        return search_executions(
            filters={"function_name": func_name.split('.')[-1], "status": "SUCCESS"},
            limit=limit,
            sort_by="timestamp_utc",
            sort_ascending=False
        )


class FileReplaySource(BaseSource):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def fetch_data(self, func_name: str, limit: int) -> List[Dict[str, Any]]:
        data = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if len(data) >= limit: break
                    record = json.loads(line)
                    data.append(record)
        except FileNotFoundError:
            raise FileNotFoundError(f"Snapshot file not found: {self.file_path}")
        return data


class DataSourceFactory:
    @staticmethod
    def get_source(source_type: str, path: str = None) -> BaseSource:
        if source_type == "file":
            return FileReplaySource(path)
        return DBReplaySource()
