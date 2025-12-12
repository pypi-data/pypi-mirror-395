import inspect
from typing import Dict, Type, TypedDict, cast

from marvel_schedule_maker.models import ActionFieldModel

from marvel_schedule_maker.utils.sequencer import Sequencer

class AttributeDict(TypedDict):
    type: str
    category: str
    description: str
    position: int
    display_name: str
    duration: str
    validators: dict[str, Type[ActionFieldModel.BaseModel]]
    timeline_name: str
    
ActionsDict = Dict[str, AttributeDict]


def getActionRegistry() -> ActionsDict:
    actions: ActionsDict = {}
    for name, func in inspect.getmembers(Sequencer, predicate=inspect.isfunction):
        if getattr(func, "__is_action_method__", False):
            # Get all attributes of the function except built-ins
            attributes = cast(AttributeDict, {k: v for k, v in func.__dict__.items() if not k.startswith('__')})
            actions[attributes['type']] = attributes
    return actions


ACTION_REGISTRY = getActionRegistry()
ACTION_DURATIONS = {action['type']: action['duration'] for action in ACTION_REGISTRY.values()}
