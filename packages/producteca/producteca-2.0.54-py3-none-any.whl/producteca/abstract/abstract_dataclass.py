from abc import ABC
from ..config.config import ConfigProducteca
from ..utils import clean_model_dump
from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class BaseService(ABC):
    config: ConfigProducteca
    endpoint: str
    _record: Optional[Any] = None
    
    def __repr__(self):
        return repr(self._record)

    def to_dict(self):
        return clean_model_dump(self._record)

    def to_json(self):
        import json
        return json.dumps(clean_model_dump(self._record))

    def __getattr__(self, key):
        return getattr(self._record, key)
