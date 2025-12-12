import os
import time
import asyncio
from typing import List, Dict, Any, Optional, AsyncGenerator, Callable, Union, Iterator
from dataclasses import dataclass, field
import openai

# Mock OpenAI-compatible response classes for Responses API
@dataclass
class MOpenAIResponseChoice:
    index: int = 0
    finish_reason: str = "stop"
    
    @dataclass
    class Message:
        content: str
        role: str = "assistant"
        tool_calls: Optional[List[Dict[str, Any]]] = None
        
    @dataclass
    class Delta:
        content: Optional[str] = None
        tool_calls: Optional[List[Dict[str, Any]]] = None
        
    message: Message = None
    delta: Delta = None

@dataclass
class MOpenAIResponseUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

@dataclass
class MOpenAIResponseCompletionResponse:
    id: str = f"chatcmpl-{int(time.time())}"
    choices: List[MOpenAIResponseChoice] = field(default_factory=list)
    usage: MOpenAIResponseUsage = field(default_factory=MOpenAIResponseUsage)
    model: str = ""
    object: str = "chat.completion"
    created: int = field(default_factory=lambda: int(time.time()))

# Chat Completions API wrapper for Responses API
class MOpenAIResponseChatCompletions:
    def __init__(self, client):
        self.client = client
        
    def create(
        self,
        messages: List[Dict[str, Any]],
        model: str = "gpt-4o",
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        stop: Optional[Union[str, List[str]]] = None,
        stream: bool = False,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        response_format: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Convert OpenAI Chat Completions API call to Responses API call
        """
        
        # Prepare input for Responses API
        input_data = []
        
        # Convert messages to Responses API format
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                # System messages need to be handled differently in Responses API
                # We can add them as instructions or prepend to first user message
                if isinstance(content, str):
                    input_data.append({
                        "role": "system",
                        "content": [{"type": "input_text", "text": content}]
                    })
                else:
                    input_data.append({
                        "role": "system", 
                        "content": self._convert_content_to_responses_format(content)
                    })
            elif role in ["user", "assistant"]:
                if isinstance(content, str):
                    input_data.append({
                        "role": role,
                        "content": [{"type": "input_text" if role == "user" else "output_text", "text": content}]
                    })
                else:
                    input_data.append({
                        "role": role,
                        "content": self._convert_content_to_responses_format(content)
                    })
            elif role == "tool":
                # Handle tool response messages
                input_data.append({
                    "type": "function_call_output",
                    "call_id": msg.get("tool_call_id", ""),
                    "output": content
                })
        
        # Prepare Responses API parameters
        responses_params = {
            "model": model,
            "input": input_data,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream
        }
        
        # Add max_tokens if specified
        if max_tokens is not None:
            responses_params["max_output_tokens"] = max_tokens
            
        # Add tools if specified
        if tools is not None:
            responses_params["tools"] = self._convert_tools_to_responses_format(tools)
            
        # Add tool_choice if specified
        if tool_choice is not None:
            responses_params["tool_choice"] = tool_choice
            
        # Add response_format if specified
        if response_format is not None:
            responses_params["text"] = {
                "format": response_format
            }
            
        # Add stop sequences if specified
        if stop is not None:
            responses_params["text"] = responses_params.get("text", {})
            responses_params["text"]["stop"] = stop if isinstance(stop, list) else [stop]
        
        # Handle streaming vs non-streaming
        if stream:
            return self._handle_stream_response(responses_params)
        else:
            return self._handle_normal_response(responses_params)
    
    def _convert_content_to_responses_format(self, content):
        """Convert content to Responses API format"""
        if isinstance(content, str):
            return [{"type": "input_text", "text": content}]
            
        result = []
        for item in content:
            if item.get("type") == "text":
                result.append({"type": "input_text", "text": item["text"]})
            elif item.get("type") == "image_url":
                result.append({
                    "type": "input_image",
                    "image_url": item["image_url"]["url"]
                })
            else:
                # Pass through other types as-is
                result.append(item)
        return result
    
    def _convert_tools_to_responses_format(self, tools):
        """Convert tools to Responses API format"""
        converted_tools = []
        for tool in tools:
            if tool.get("type") == "function":
                converted_tools.append({
                    "type": "function",
                    "name": tool["function"]["name"],
                    "description": tool["function"].get("description", ""),
                    "parameters": tool["function"].get("parameters", {})
                })
            else:
                # Pass through other tool types
                converted_tools.append(tool)
        return converted_tools
    
    def _handle_normal_response(self, responses_params):
        """Handle non-streaming response"""
        try:
            # Call the new Responses API
            response = self.client.client.responses.create(**responses_params)
            
            # Convert to Chat Completions format
            content = ""
            tool_calls = None
            finish_reason = "stop"
            
            # Extract content from output
            for output_item in response.output:
                if hasattr(output_item, 'type'):
                    if output_item.type == "message":
                        for content_block in output_item.content:
                            if content_block.type == "output_text":
                                content += content_block.text
                    elif output_item.type == "function_call":
                        # Handle function calls
                        if tool_calls is None:
                            tool_calls = []
                        tool_calls.append({
                            "id": output_item.call_id,
                            "type": "function",
                            "function": {
                                "name": output_item.name,
                                "arguments": output_item.arguments
                            }
                        })
                        finish_reason = "tool_calls"
            
            # Create OpenAI-compatible response
            choice = MOpenAIResponseChoice(
                message=MOpenAIResponseChoice.Message(
                    content=content,
                    role="assistant",
                    tool_calls=tool_calls
                ),
                finish_reason=finish_reason
            )
            
            # Extract usage information
            usage = MOpenAIResponseUsage()
            if hasattr(response, 'usage') and response.usage:
                usage.prompt_tokens = getattr(response.usage, 'input_tokens', 0)
                usage.completion_tokens = getattr(response.usage, 'output_tokens', 0)
                usage.total_tokens = getattr(response.usage, 'total_tokens', usage.prompt_tokens + usage.completion_tokens)
            
            openai_response = MOpenAIResponseCompletionResponse(
                id=response.id,
                choices=[choice],
                usage=usage,
                model=response.model,
            )
            
            return openai_response
            
        except Exception as e:
            # Handle errors
            error_response = MOpenAIResponseCompletionResponse()
            error_response.error = str(e)
            return error_response
    
    def _handle_stream_response(self, responses_params):
        """Handle streaming response"""
        try:
            # Call the new Responses API with streaming
            stream = self.client.client.responses.create(**responses_params)
            
            # Convert streaming response to Chat Completions format
            def stream_generator():
                accumulated_content = ""
                accumulated_tool_calls = []
                
                for event in stream:
                    chunk = MOpenAIResponseCompletionResponse(
                        choices=[MOpenAIResponseChoice(
                            delta=MOpenAIResponseChoice.Delta(),
                            finish_reason=None
                        )]
                    )
                    
                    if event.type == "response.output_text.delta":
                        # Text delta
                        chunk.choices[0].delta.content = event.delta
                        accumulated_content += event.delta
                        yield chunk
                        
                    elif event.type == "response.function_call.delta":
                        # Function call delta
                        if not accumulated_tool_calls:
                            accumulated_tool_calls.append({
                                "id": event.call_id,
                                "type": "function",
                                "function": {
                                    "name": event.name,
                                    "arguments": ""
                                }
                            })
                        
                        # Update arguments
                        if hasattr(event, 'arguments_delta'):
                            accumulated_tool_calls[-1]["function"]["arguments"] += event.arguments_delta
                            chunk.choices[0].delta.tool_calls = [accumulated_tool_calls[-1]]
                            yield chunk
                            
                    elif event.type == "response.done":
                        # Final chunk
                        final_chunk = MOpenAIResponseCompletionResponse(
                            choices=[MOpenAIResponseChoice(
                                delta=MOpenAIResponseChoice.Delta(content=""),
                                finish_reason="stop" if not accumulated_tool_calls else "tool_calls"
                            )]
                        )
                        
                        # Add usage if available
                        if hasattr(event, 'usage'):
                            final_chunk.usage = MOpenAIResponseUsage(
                                prompt_tokens=getattr(event.usage, 'input_tokens', 0),
                                completion_tokens=getattr(event.usage, 'output_tokens', 0),
                                total_tokens=getattr(event.usage, 'total_tokens', 0)
                            )
                        
                        yield final_chunk
            
            return stream_generator()
            
        except Exception as e:
            # Handle errors
            def error_generator():
                error_response = MOpenAIResponseCompletionResponse()
                error_response.error = str(e)
                yield error_response
            return error_generator()

# Main client class that wraps OpenAI Responses API to look like Chat Completions API
class MOpenAIResponseAI:
    def __init__(self, api_key=None, base_url=None, organization=None, **kwargs):
        self.api_key = api_key
        if not self.api_key:
            self.api_key = os.environ.get("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError(
                    "API key must be provided either as an argument or through the OPENAI_API_KEY environment variable")
        
        # Initialize the OpenAI client
        client_kwargs = {
            "api_key": self.api_key
        }
        
        if base_url:
            client_kwargs["base_url"] = base_url
        if organization:
            client_kwargs["organization"] = organization
            
        self.client = openai.OpenAI(**client_kwargs)
        
        # Create API interfaces - make structure match OpenAI's
        self.chat = self._ChatCompletionsInterface(self)
    
    class _ChatCompletionsInterface:
        def __init__(self, client):
            self.client = client
            self.completions = MOpenAIResponseChatCompletions(client)
    
    def close(self):
        # Close the client if necessary
        if hasattr(self.client, "close") and callable(self.client.close):
            self.client.close()

# Async version of the client
class MAsyncOpenAIResponseAI:
    def __init__(self, api_key=None, base_url=None, organization=None, **kwargs):
        self.api_key = api_key
        if not self.api_key:
            self.api_key = os.environ.get("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError(
                    "API key must be provided either as an argument or through the OPENAI_API_KEY environment variable")
        
        # Initialize the AsyncOpenAI client
        client_kwargs = {
            "api_key": self.api_key
        }
        
        if base_url:
            client_kwargs["base_url"] = base_url
        if organization:
            client_kwargs["organization"] = organization
            
        self.client = openai.AsyncOpenAI(**client_kwargs)
        
        # Create API interfaces - make structure match AsyncOpenAI
        self.chat = self._AsyncChatInterface(self)
    
    class _AsyncChatInterface:
        def __init__(self, client):
            self.client = client
            self.completions = client._AsyncChatCompletions(client)
    
    class _AsyncChatCompletions:
        def __init__(self, client):
            self.client = client
        
        async def create(
            self,
            messages: List[Dict[str, Any]],
            model: str = "gpt-4o",
            temperature: float = 1.0,
            max_tokens: Optional[int] = None,
            top_p: float = 1.0,
            frequency_penalty: float = 0.0,
            presence_penalty: float = 0.0,
            stop: Optional[Union[str, List[str]]] = None,
            stream: bool = False,
            tools: Optional[List[Dict[str, Any]]] = None,
            tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
            response_format: Optional[Dict[str, Any]] = None,
            **kwargs
        ):
            """
            Async version of the create method
            """
            # For simplicity, reuse the sync logic
            # In a production implementation, you would implement proper async streaming
            sync_completions = MOpenAIResponseChatCompletions(self.client)
            return sync_completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop,
                stream=stream,
                tools=tools,
                tool_choice=tool_choice,
                response_format=response_format,
                **kwargs
            )
    
    async def close(self):
        # Close the client if necessary
        if hasattr(self.client, "close") and callable(self.client.close):
            await self.client.close() 