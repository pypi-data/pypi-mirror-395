"""
DeepSeek-safe LLM wrapper for CrewAI.

This module provides a wrapper around CrewAI's LLM class that sanitizes message
histories to prevent the "Invalid consecutive assistant/user message" error that
DeepSeek's API returns when consecutive messages have the same role.

The wrapper ensures messages alternate between user and assistant roles by:
1. Merging consecutive messages of the same role into a single message
2. Ensuring the first message is always from the user
3. Preserving all semantic content while maintaining API compatibility

Usage:
    from traia_tools import DeepSeekSafeLLM
    
    llm = DeepSeekSafeLLM(
        model="deepseek/deepseek-reasoner",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=1.0
    )
"""

import logging
from typing import Any, Dict, List

from crewai import LLM


class DeepSeekSafeLLM(LLM):
    """
    A wrapper around CrewAI's LLM that sanitizes message histories for DeepSeek.
    
    DeepSeek's API does not support consecutive messages from the same role
    (e.g., two assistant messages in a row). This wrapper automatically handles
    message sanitization to prevent API errors while preserving conversation context.
    
    Attributes:
        merge_consecutive_messages: If True, merges consecutive same-role messages.
                                   If False, only keeps the last message of each
                                   consecutive block.
    """
    
    def __init__(
        self,
        *args,
        merge_consecutive_messages: bool = True,
        **kwargs
    ):
        """
        Initialize DeepSeekSafeLLM with message sanitization enabled.
        
        Args:
            *args: Positional arguments passed to parent LLM class
            merge_consecutive_messages: Whether to merge consecutive messages (True)
                                       or keep only the last one (False)
            **kwargs: Keyword arguments passed to parent LLM class
        """
        super().__init__(*args, **kwargs)
        self.merge_consecutive_messages = merge_consecutive_messages
        
        logging.info(
            f"Initialized DeepSeekSafeLLM with model={self.model}, "
            f"merge_consecutive_messages={merge_consecutive_messages}"
        )
    
    def sanitize_messages(
        self,
        messages: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Sanitize message list to ensure no consecutive messages have the same role.
        
        This method:
        1. Ensures the first message is from 'user' (DeepSeek requirement)
        2. Merges or filters consecutive messages of the same role
        3. Preserves all message content and context
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            
        Returns:
            Sanitized list of messages with alternating roles
        """
        if not messages:
            logging.warning("sanitize_messages called with empty message list")
            return messages
        
        # Log input for debugging
        logging.debug(
            f"Sanitizing {len(messages)} messages. "
            f"First role: {messages[0].get('role')}, "
            f"Last role: {messages[-1].get('role')}"
        )
        
        sanitized = []
        assistant_buffer = []
        user_buffer = []
        prev_role = None
        
        def flush_assistant_buffer():
            """Merge buffered assistant messages into one message."""
            if assistant_buffer:
                if self.merge_consecutive_messages:
                    # Merge all assistant messages with clear separation
                    combined = "\n\n---\n\n".join(assistant_buffer)
                    sanitized.append({"role": "assistant", "content": combined})
                    logging.debug(
                        f"Merged {len(assistant_buffer)} assistant messages "
                        f"into one ({len(combined)} chars)"
                    )
                else:
                    # Keep only the last assistant message
                    sanitized.append({
                        "role": "assistant",
                        "content": assistant_buffer[-1]
                    })
                    logging.debug(
                        f"Kept last of {len(assistant_buffer)} assistant messages"
                    )
                assistant_buffer.clear()
        
        def flush_user_buffer():
            """Merge buffered user messages into one message."""
            if user_buffer:
                if self.merge_consecutive_messages:
                    # Merge all user messages with clear separation
                    combined = "\n\n---\n\n".join(user_buffer)
                    sanitized.append({"role": "user", "content": combined})
                    logging.debug(
                        f"Merged {len(user_buffer)} user messages "
                        f"into one ({len(combined)} chars)"
                    )
                else:
                    # Keep only the last user message
                    sanitized.append({"role": "user", "content": user_buffer[-1]})
                    logging.debug(
                        f"Kept last of {len(user_buffer)} user messages"
                    )
                user_buffer.clear()
        
        # Ensure first message is from user (DeepSeek requirement)
        # If first message is system or assistant, convert to user
        first_message = messages[0].copy()
        if first_message.get("role") not in ["user"]:
            logging.info(
                f"Converting first message from '{first_message.get('role')}' "
                f"to 'user' (DeepSeek requirement)"
            )
            first_message["role"] = "user"
        
        # Process all messages
        for i, msg in enumerate([first_message] + messages[1:]):
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            # Handle system messages by converting to user
            if role == "system":
                role = "user"
                logging.debug(
                    f"Converted system message at index {i} to user message"
                )
            
            # Skip empty content messages
            if not content or (isinstance(content, str) and not content.strip()):
                logging.debug(
                    f"Skipping empty message at index {i} with role '{role}'"
                )
                continue
            
            # Convert content to string if it's a list (some models use list format)
            if isinstance(content, list):
                # Extract text from content list
                text_parts = []
                for item in content:
                    if isinstance(item, dict) and "text" in item:
                        text_parts.append(item["text"])
                    elif isinstance(item, str):
                        text_parts.append(item)
                content = " ".join(text_parts)
                logging.debug(f"Converted list content to string at index {i}")
            
            # Buffer messages by role
            if role == "assistant":
                # Flush user buffer if switching from user to assistant
                if prev_role == "user":
                    flush_user_buffer()
                assistant_buffer.append(content)
            elif role == "user":
                # Flush assistant buffer if switching from assistant to user
                if prev_role == "assistant":
                    flush_assistant_buffer()
                user_buffer.append(content)
            else:
                # Handle any other roles as user messages
                logging.warning(
                    f"Unknown role '{role}' at index {i}, treating as user message"
                )
                if prev_role == "assistant":
                    flush_assistant_buffer()
                user_buffer.append(content)
                role = "user"
            
            prev_role = role
        
        # Flush remaining buffers
        flush_assistant_buffer()
        flush_user_buffer()
        
        # Ensure we have at least one message
        if not sanitized:
            logging.warning(
                "Sanitization resulted in empty message list, "
                "adding default user message"
            )
            sanitized.append({"role": "user", "content": "Please provide a response."})
        
        # Log output for debugging
        logging.debug(
            f"Sanitization complete: {len(messages)} -> {len(sanitized)} messages. "
            f"First role: {sanitized[0].get('role')}, "
            f"Last role: {sanitized[-1].get('role')}"
        )
        
        # Verify no consecutive same-role messages remain
        for i in range(len(sanitized) - 1):
            if sanitized[i]["role"] == sanitized[i + 1]["role"]:
                logging.error(
                    f"SANITIZATION FAILED: Consecutive {sanitized[i]['role']} "
                    f"messages at indices {i} and {i+1}"
                )
        
        return sanitized
    
    def call(
        self,
        messages: str | List[Dict[str, str]],
        tools: List[Dict] | None = None,
        callbacks: List[Any] | None = None,
        available_functions: Dict[str, Any] | None = None,
        from_task: Any | None = None,
        from_agent: Any | None = None,
    ) -> str | Any:
        """
        Override CrewAI's LLM.call() to sanitize messages before calling DeepSeek.
        
        This method intercepts the call, sanitizes the message list to prevent
        consecutive same-role messages, and then calls the parent LLM implementation.
        
        Args:
            messages: Input messages (string or list of message dicts)
            tools: Optional tool schemas for function calling
            callbacks: Optional callback functions
            available_functions: Optional dict of callable functions
            from_task: Optional Task that invoked the LLM
            from_agent: Optional Agent that invoked the LLM
            
        Returns:
            Response from the LLM (string or function call result)
        """
        # Convert string messages to list format
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        
        # Log pre-sanitization state
        logging.debug(
            f"DeepSeekSafeLLM.call() invoked with {len(messages)} messages, "
            f"{len(tools) if tools else 0} tools"
        )
        
        # Sanitize messages to prevent consecutive same-role messages
        safe_messages = self.sanitize_messages(messages)
        
        # Log post-sanitization state
        logging.debug(
            f"Calling parent LLM with {len(safe_messages)} sanitized messages"
        )
        
        # Call parent LLM implementation with sanitized messages
        try:
            response = super().call(
                messages=safe_messages,
                tools=tools,
                callbacks=callbacks,
                available_functions=available_functions,
                from_task=from_task,
                from_agent=from_agent
            )
            logging.debug(
                f"LLM call successful, response length: {len(str(response))}"
            )
            return response
        except Exception as e:
            logging.error(
                f"LLM call failed after sanitization: {str(e)}. "
                f"Message count: {len(safe_messages)}"
            )
            raise

