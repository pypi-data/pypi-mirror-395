from __future__ import annotations

from typing import Dict, List, Optional, Type

from dioritorm.core.entity import Entity
from dioritorm.core.event import Event


_sync_models: Dict[str, Type[Entity]] = {}
_sync_events: List[Type[Event]] = []
_sync_node_cls: Optional[Type[Entity]] = None
_sync_entity_cls: Optional[Type[Entity]] = None


def register_sync_model(name: str, model_cls: Type[Entity]) -> None:
    _sync_models[name] = model_cls


def get_sync_models() -> Dict[str, Type[Entity]]:
    return dict(_sync_models)


def register_sync_event(event_cls: Type[Event]) -> None:
    if event_cls not in _sync_events:
        _sync_events.append(event_cls)


def get_sync_events() -> List[Type[Event]]:
    return list(_sync_events)


def register_sync_node(node_cls: Type[Entity]) -> None:
    global _sync_node_cls
    _sync_node_cls = node_cls


def get_sync_node() -> Optional[Type[Entity]]:
    return _sync_node_cls


def register_sync_entity(entity_cls: Type[Entity]) -> None:
    global _sync_entity_cls
    _sync_entity_cls = entity_cls


def get_sync_entity() -> Optional[Type[Entity]]:
    return _sync_entity_cls
