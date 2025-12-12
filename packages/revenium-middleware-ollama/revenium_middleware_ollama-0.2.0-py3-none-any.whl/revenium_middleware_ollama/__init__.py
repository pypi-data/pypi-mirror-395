"""
When you install and import this library, it will automatically hook
ollama.chat using wrapt, and log token usage after
each request. You can customize or extend this logging logic later
to add user or organization metadata for metering purposes.
"""
from .middleware import chat_wrapper,generate_wrapper