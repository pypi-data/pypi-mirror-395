from functools import wraps
from typing import Any, Callable, Optional
import asyncio

from moss import Subject, Envelope
from moss.errors import KeyNotFound


def _get_or_create_subject(subject_id: str) -> Subject:
    """Load existing subject or create new one."""
    try:
        return Subject.load(subject_id)
    except KeyNotFound:
        return Subject.create(subject_id)


def _state_to_payload(state: Any) -> dict:
    """Convert state to signable payload, excluding moss_envelope."""
    if isinstance(state, dict):
        return {k: v for k, v in state.items() if k != "moss_envelope"}
    elif hasattr(state, "dict"):
        d = state.dict()
        d.pop("moss_envelope", None)
        return d
    elif hasattr(state, "__dict__"):
        d = dict(state.__dict__)
        d.pop("moss_envelope", None)
        return d
    else:
        return {"output": str(state)}


def _attach_envelope(state: Any, envelope: Envelope) -> Any:
    """Attach envelope to state."""
    if isinstance(state, dict):
        state["moss_envelope"] = envelope
    elif hasattr(state, "__setattr__"):
        state.moss_envelope = envelope
    return state


def signed_node(fn: Callable, subject_id: str) -> Callable:
    """
    Wrap a LangGraph node function with MOSS signing.
    
    Args:
        fn: A LangGraph node function that takes state and returns state
        subject_id: MOSS subject identifier (e.g., "moss:flow:step")
    
    Returns:
        A wrapped function that signs node outputs.
        After execution, state["moss_envelope"] contains the signature.
    
    Example:
        from langgraph.graph import StateGraph
        from moss_langgraph import signed_node
        
        def my_node(state):
            state["result"] = "computed"
            return state
        
        graph = StateGraph(dict)
        graph.add_node("step", signed_node(my_node, "moss:flow:step"))
        
        # After node executes, state["moss_envelope"] is populated
    """
    subject = _get_or_create_subject(subject_id)
    
    if asyncio.iscoroutinefunction(fn):
        @wraps(fn)
        async def async_wrapped(state: Any, *args, **kwargs) -> Any:
            result = await fn(state, *args, **kwargs)
            
            if result is not None:
                payload = _state_to_payload(result)
                envelope = subject.sign(payload)
                result = _attach_envelope(result, envelope)
            
            return result
        
        return async_wrapped
    else:
        @wraps(fn)
        def sync_wrapped(state: Any, *args, **kwargs) -> Any:
            result = fn(state, *args, **kwargs)
            
            if result is not None:
                payload = _state_to_payload(result)
                envelope = subject.sign(payload)
                result = _attach_envelope(result, envelope)
            
            return result
        
        return sync_wrapped


class SignedNodeFactory:
    """
    Factory for creating signed nodes with the same subject.
    
    Example:
        factory = SignedNodeFactory("moss:flow:pipeline")
        
        graph.add_node("step1", factory.wrap(step1_fn))
        graph.add_node("step2", factory.wrap(step2_fn))
    """
    
    def __init__(self, subject_id: str):
        self.subject_id = subject_id
        self._subject: Optional[Subject] = None
    
    @property
    def subject(self) -> Subject:
        if self._subject is None:
            self._subject = _get_or_create_subject(self.subject_id)
        return self._subject
    
    def wrap(self, fn: Callable) -> Callable:
        """Wrap a node function with signing using this factory's subject."""
        return signed_node(fn, self.subject_id)
