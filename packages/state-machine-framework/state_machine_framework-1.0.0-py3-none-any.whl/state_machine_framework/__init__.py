"""
State Machine Framework

A flexible, production-ready state machine framework for Python with:
- Clean state definitions with minimal boilerplate
- Validator and hook decorators for validation and side effects
- Multiple ORM support (Django, SQLAlchemy, etc.)
- Workflow context with type safety and validation
- External hook registration for modularity
- Comprehensive error handling

Usage:
    from state_machine_framework import (
        State, StateMachine, validator, hook, transition,
        WorkflowContext, ORMAdapter
    )
"""

__version__ = "1.0.0"
__author__ = "State Machine Framework Team"

from state_machine_framework.core.state import State, StateMeta
from state_machine_framework.core.state_machine import StateMachine, StateMachineMeta
from state_machine_framework.core.exceptions import (
    StateMachineError,
    StateValidityError,
    ObjectNotFound,
    TransitionError,
    ContextValidationError
)

from state_machine_framework.decorators.hooks import (
    pre_transition,
    validator,
    hook,
    transition,
    HookRegistry
)

from state_machine_framework.orm.base import ORMAdapter
from state_machine_framework.workflow.context import WorkflowContext, StateTransitionResult
from state_machine_framework.workflow.requirements import (
    ContextRequirement,
    ModelRequirement,
    DictRequirement
)

__all__ = [
    # Core classes
    'State',
    'StateMeta',
    'StateMachine',
    'StateMachineMeta',
    
    # Exceptions
    'StateMachineError',
    'StateValidityError',
    'ObjectNotFound',
    'TransitionError',
    'ContextValidationError',
    
    # Decorators
    'pre_transition',
    'validator',
    'hook',
    'transition',
    'HookRegistry',
    
    # ORM
    'ORMAdapter',
    
    # Workflow
    'WorkflowContext',
    'StateTransitionResult',
    'ContextRequirement',
    'ModelRequirement',
    'DictRequirement',
]


