from functools import wraps
from typing import Any, Callable, Optional

from moss import Subject, Envelope
from moss.errors import KeyNotFound


def _get_or_create_subject(subject_id: str) -> Subject:
    """Load existing subject or create new one."""
    try:
        return Subject.load(subject_id)
    except KeyNotFound:
        return Subject.create(subject_id)


def _wrap_method(method: Callable, subject: Subject, agent: Any) -> Callable:
    """Wrap a method to sign its output."""
    @wraps(method)
    def wrapped(*args, **kwargs):
        result = method(*args, **kwargs)
        
        if result is not None:
            payload = _result_to_payload(result)
            envelope = subject.sign(payload)
            agent.moss_envelope = envelope
        
        return result
    
    return wrapped


def _wrap_async_method(method: Callable, subject: Subject, agent: Any) -> Callable:
    """Wrap an async method to sign its output."""
    @wraps(method)
    async def wrapped(*args, **kwargs):
        result = await method(*args, **kwargs)
        
        if result is not None:
            payload = _result_to_payload(result)
            envelope = subject.sign(payload)
            agent.moss_envelope = envelope
        
        return result
    
    return wrapped


def _result_to_payload(result: Any) -> dict:
    """Convert agent output to signable payload."""
    if isinstance(result, dict):
        return result
    elif isinstance(result, str):
        return {"output": result}
    elif hasattr(result, "raw"):
        return {"output": result.raw}
    elif hasattr(result, "dict"):
        return result.dict()
    elif hasattr(result, "__dict__"):
        return {"output": str(result), "type": type(result).__name__}
    else:
        return {"output": str(result)}


def moss_wrap(agent: Any, subject_id: str) -> Any:
    """
    Wrap a CrewAI agent with MOSS signing.
    
    Args:
        agent: A CrewAI Agent instance
        subject_id: MOSS subject identifier (e.g., "moss:team:researcher")
    
    Returns:
        The same agent with wrapped methods that sign outputs.
        After each output, agent.moss_envelope contains the signature.
    
    Example:
        from crewai import Agent
        from moss_crewai import moss_wrap
        
        agent = Agent(role="Researcher", ...)
        agent = moss_wrap(agent, "moss:team:researcher")
        
        # After agent executes, check:
        # agent.moss_envelope  # Contains MOSS Envelope
    """
    subject = _get_or_create_subject(subject_id)
    
    agent.moss_envelope: Optional[Envelope] = None
    agent._moss_subject = subject
    
    methods_to_wrap = ["execute_task", "execute", "run", "invoke"]
    
    for method_name in methods_to_wrap:
        if hasattr(agent, method_name):
            original = getattr(agent, method_name)
            if callable(original):
                import asyncio
                if asyncio.iscoroutinefunction(original):
                    wrapped = _wrap_async_method(original, subject, agent)
                else:
                    wrapped = _wrap_method(original, subject, agent)
                setattr(agent, method_name, wrapped)
    
    return agent
