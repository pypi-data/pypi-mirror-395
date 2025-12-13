from functools import wraps
from typing import Any, Callable, Optional, Union, Dict, List

from moss import Subject, Envelope
from moss.errors import KeyNotFound


def _get_or_create_subject(subject_id: str) -> Subject:
    """Load existing subject or create new one."""
    try:
        return Subject.load(subject_id)
    except KeyNotFound:
        return Subject.create(subject_id)


def _result_to_payload(result: Any) -> dict:
    """Convert agent output to signable payload."""
    if isinstance(result, dict):
        return result
    elif isinstance(result, str):
        return {"content": result}
    elif isinstance(result, (list, tuple)):
        return {"messages": [_result_to_payload(r) for r in result]}
    elif hasattr(result, "dict"):
        return result.dict()
    elif hasattr(result, "__dict__"):
        return {"content": str(result), "type": type(result).__name__}
    else:
        return {"content": str(result)}


def _wrap_method(method: Callable, subject: Subject, agent: Any) -> Callable:
    """Wrap a sync method to sign its output."""
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


def _wrap_generate_reply(original_method: Callable, subject: Subject, agent: Any) -> Callable:
    """Wrap generate_reply specifically for AutoGen's signature."""
    @wraps(original_method)
    def wrapped(
        messages: Optional[List[Dict]] = None,
        sender: Optional[Any] = None,
        **kwargs
    ) -> Union[str, Dict, None]:
        result = original_method(messages=messages, sender=sender, **kwargs)
        
        if result is not None:
            payload = _result_to_payload(result)
            envelope = subject.sign(payload)
            agent.moss_envelope = envelope
        
        return result
    
    return wrapped


def _wrap_async_generate_reply(original_method: Callable, subject: Subject, agent: Any) -> Callable:
    """Wrap async generate_reply for AutoGen's signature."""
    @wraps(original_method)
    async def wrapped(
        messages: Optional[List[Dict]] = None,
        sender: Optional[Any] = None,
        **kwargs
    ) -> Union[str, Dict, None]:
        result = await original_method(messages=messages, sender=sender, **kwargs)
        
        if result is not None:
            payload = _result_to_payload(result)
            envelope = subject.sign(payload)
            agent.moss_envelope = envelope
        
        return result
    
    return wrapped


def signed_agent(agent: Any, subject_id: str) -> Any:
    """
    Wrap an AutoGen agent with MOSS signing.
    
    Args:
        agent: An AutoGen agent instance (ConversableAgent, AssistantAgent, etc.)
        subject_id: MOSS subject identifier (e.g., "moss:lab:analyst")
    
    Returns:
        The same agent with wrapped methods that sign outputs.
        After each reply, agent.moss_envelope contains the signature.
    
    Example:
        from autogen import AssistantAgent
        from moss_autogen import signed_agent
        
        agent = AssistantAgent(name="analyst", ...)
        agent = signed_agent(agent, "moss:lab:analyst")
        
        # After agent replies, check:
        # agent.moss_envelope  # Contains MOSS Envelope
    """
    subject = _get_or_create_subject(subject_id)
    
    agent.moss_envelope: Optional[Envelope] = None
    agent._moss_subject = subject
    
    import asyncio
    
    methods_to_wrap = [
        ("generate_reply", _wrap_generate_reply, _wrap_async_generate_reply),
        ("a_generate_reply", None, _wrap_async_generate_reply),
    ]
    
    for method_name, sync_wrapper, async_wrapper in methods_to_wrap:
        if hasattr(agent, method_name):
            original = getattr(agent, method_name)
            if callable(original):
                if asyncio.iscoroutinefunction(original):
                    if async_wrapper:
                        wrapped = async_wrapper(original, subject, agent)
                        setattr(agent, method_name, wrapped)
                else:
                    if sync_wrapper:
                        wrapped = sync_wrapper(original, subject, agent)
                        setattr(agent, method_name, wrapped)
    
    generic_methods = ["receive", "send", "run", "execute"]
    
    for method_name in generic_methods:
        if hasattr(agent, method_name):
            original = getattr(agent, method_name)
            if callable(original):
                if asyncio.iscoroutinefunction(original):
                    wrapped = _wrap_async_method(original, subject, agent)
                else:
                    wrapped = _wrap_method(original, subject, agent)
                setattr(agent, method_name, wrapped)
    
    return agent
