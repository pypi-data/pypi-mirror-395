from copy import deepcopy
from typing import Dict, List, Optional, Union, Any, ClassVar, Type
import requests
from smolagents import ApiModel, ChatMessage, MessageRole
from smolagents.tools import Tool
from smolagents.models import get_clean_message_list, tool_role_conversions
from openai.types.chat import ChatCompletion
import os
from dotenv import load_dotenv
load_dotenv()

def _request_access_token() -> str:
    """Request an access token from the Flow API"""
    response = requests.post(
        "https://flow.ciandt.com/auth-engine-api/v1/api-key/token",
        headers={"Content-Type": "application/json", "FlowTenant": os.getenv("FLOW_TENANT", "flowteam")},
        json={"clientId": os.getenv("FLOW_CLIENT_ID"), "clientSecret": os.getenv("FLOW_CLIENT_SECRET"), "appToAccess": "llm-api"}
    )

    return response.json().get("access_token")

_access_token = _request_access_token()

class ModelConfig:
    """Configuration for a specific model type"""
    def __init__(
        self,
        api_url: str,
        response_handler: str,
        default_params: Dict[str, Any],
        requires_anthropic_format: bool = False,
        requires_system_message_separation: bool = False,
    ):
        self.api_url = api_url
        self.response_handler = response_handler  # 'claude' or 'openai'
        self.default_params = default_params
        self.requires_anthropic_format = requires_anthropic_format
        self.requires_system_message_separation = requires_system_message_separation


class FlowApiModel(ApiModel):
    """
    A unified API model wrapper for Flow-based models (Claude, GPT, DeepSeek),
    providing a simple interface to interact with different model types.
    """
    # Registry of model-specific configurations
    MODEL_REGISTRY: ClassVar[Dict[str, ModelConfig]] = {
        # Claude models
        "anthropic.claude-37-sonnet": ModelConfig(
            api_url="https://flow.ciandt.com/ai-orchestration-api/v1/bedrock/invoke",
            response_handler="claude",
            default_params={
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 20000,
                "temperature": 0.5,
                "top_p": 0.9,
                "top_k": 250,
            },
            requires_anthropic_format=True,
            requires_system_message_separation=True,
        ),
        
        # DeepSeek models
        "DeepSeek-R1": ModelConfig(
            api_url="https://flow.ciandt.com/ai-orchestration-api/v1/foundry/chat/completions",
            response_handler="openai",
            default_params={
                "max_tokens": 8192,
            },
        ),
        
        # GPT models
        "o3-mini": ModelConfig(
            api_url="https://flow.ciandt.com/ai-orchestration-api/v1/openai/chat/completions",
            response_handler="openai",
            default_params={
                "max_tokens": 8192,
                "top_p": 1.0,
                "reasoning_effort": "medium",
                "presence_penalty": 0,
                "frequency_penalty": 0,
            },
        ),

        "gpt-4o": ModelConfig(
            api_url="https://flow.ciandt.com/ai-orchestration-api/v1/openai/chat/completions",
            response_handler="openai",
            default_params={
                "max_tokens": 8192,
                "temperature": 0.7,
                "top_p": 1.0,
                "presence_penalty": 0,
                "frequency_penalty": 0,
            },
        ),

        "gpt-4.1": ModelConfig(
            api_url="https://flow.ciandt.com/ai-orchestration-api/v1/openai/chat/completions",
            response_handler="openai",
            default_params={
                "max_tokens": 8192,
                "temperature": 0.7,
                "top_p": 1.0,
                "presence_penalty": 0,
                "frequency_penalty": 0,
            },
        ),

        "o1-mini": ModelConfig(
            api_url="https://flow.ciandt.com/ai-orchestration-api/v1/openai/chat/completions",
            response_handler="openai",
            default_params={
                "reasoning_effort": "medium",
                "top_p": 1.0,
                "presence_penalty": 0,
                "frequency_penalty": 0,
            },
        ),
    }

    @classmethod
    def get_model_config(cls, model_id: str) -> ModelConfig:
        """Get configuration for a specific model ID"""
        if model_id not in cls.MODEL_REGISTRY:
            raise ValueError(f"Unsupported model: {model_id}. Available models: {list(cls.MODEL_REGISTRY.keys())}")
        return cls.MODEL_REGISTRY[model_id]

    @classmethod
    def create(cls, model_id: str, **kwargs) -> 'FlowApiModel':
        """Factory method to create the appropriate model instance"""
        return cls(model_id=model_id, **kwargs)

    def __init__(
        self,
        model_id: str,
        api_key: str = _access_token,
        flow_tenant: str = os.getenv("FLOW_TENANT", "flowteam"),
        flow_agent: str = "feature_refinement_agent",
        flow_operation_id: str = "default_operation",
        **kwargs,
    ):
        super().__init__(model_id=model_id, **kwargs)
        
        # Get model-specific configuration
        self.config = self.get_model_config(model_id)
        
        # Common attributes for all models
        self.api_key = api_key
        self.flow_tenant = flow_tenant
        self.flow_agent = flow_agent
        self.flow_operation_id = flow_operation_id
        self.model_name = model_id  # For backward compatibility
        
        # Load model-specific default parameters
        for key, value in self.config.default_params.items():
            setattr(self, key, kwargs.get(key, value))
        
        # Store additional kwargs
        self.kwargs = kwargs
        
        # Use model-specific API URL
        self.api_url = kwargs.get("api_url", self.config.api_url)

    def create_client(self):
        """No additional client setup is required for Flow models."""
        return None

    def _create_headers(self) -> dict:
        """
        Creates the headers for the API request.
        """
        headers = {
            "Content-Type": "application/json",
            "FlowTenant": self.flow_tenant,
            "FlowAgent": self.flow_agent,
            "Authorization": f"Bearer {self.api_key}",
        }
        
        # Only add FlowOperationId if it's required (for Claude and GPT models)
        if hasattr(self, "flow_operation_id"):
            headers["FlowOperationId"] = self.flow_operation_id
            
        return headers

    def _claude_get_tool_json_schema(self, tool: Tool) -> dict:
        """Convert a Tool object to the JSON schema format expected by the API"""
        properties = deepcopy(tool.inputs)
        required = []
        for key, value in properties.items():
            if value["type"] == "any":
                value["type"] = "string"
            if not ("nullable" in value and value["nullable"]):
                required.append(key)
        return {
            "name": tool.name,
            "type": "function",
            "description": tool.description,
            "input_schema": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        }

    def _prepare_payload(
        self,
        messages: List[Dict[str, str]],
        stop_sequences: Optional[List[str]] = None,
        grammar: Optional[str] = None,
        tools_to_call_from: Optional[List[Tool]] = None,
        custom_role_conversions: Optional[Dict[str, str]] = None,
        convert_images_to_image_urls: bool = False,
        **kwargs,
    ) -> Dict[str, Any]:
        """Prepare the payload for the API request based on model type"""
        # Handle system message separately for models that require it
        system_message = None
        if self.config.requires_system_message_separation:
            system_message = next((message for message in messages if message["role"] == "system"), None)
            messages = [message for message in messages if message["role"] != "system"]

        # Prepare completion kwargs with base model params
        completion_kwargs = self._prepare_completion_kwargs(
            messages=messages,
            stop_sequences=stop_sequences,
            grammar=grammar,
            tools_to_call_from=tools_to_call_from,
            custom_role_conversions=custom_role_conversions,
            convert_images_to_image_urls=convert_images_to_image_urls,
            **kwargs,
        )

        # Add model-specific parameters
        model_params = {}
        for key, default_value in self.config.default_params.items():
            model_params[key] = getattr(self, key, default_value)
            
        # Update with model ID and allowed models
        model_params.update({
            "allowedModels": [self.model_id],
        })

        if not self.config.response_handler == "claude":
            model_params.update({
                "model": self.model_id,
            })
        
        # Special handling for o3-mini model
        if self.model_id == "o3-mini" or self.model_id == "o1-mini":
            if "max_tokens" in model_params:
                del model_params["max_tokens"]
        
        # Update the completion kwargs with model params
        completion_kwargs.update(model_params)

        # del completion_kwargs["grammar"]  # Remove grammar from payload if it exists
        
        # Remove tool_choice from payload if it exists
        if "tool_choice" in completion_kwargs:
            del completion_kwargs["tool_choice"]
            
        # Special handling for Claude models - rename stop_sequences to stop
        if self.config.response_handler == "claude" and "stop" in completion_kwargs:
            completion_kwargs.pop("stop", None)

        # Add tools if provided
        if tools_to_call_from and self.config.requires_anthropic_format:
            completion_kwargs["tools"] = [self._claude_get_tool_json_schema(tool) for tool in tools_to_call_from]

        # Add system message if separated
        if system_message and self.config.requires_system_message_separation:
            completion_kwargs["system"] = system_message["content"]

        return completion_kwargs

    def _handle_response(self, response: requests.Response) -> ChatMessage:
        """Handle the API response based on model type"""
        if response.status_code != 200:
            raise ValueError(
                f"API call failed with status code {response.status_code}: {response.text}"
            )
        
        response_data = response.json()
        
        # Update token counts
        usage = response_data.get("usage") or {}
        self._last_input_token_count = usage.get("input_tokens", 0)
        self._last_output_token_count = usage.get("output_tokens", 0)
        
        if self.config.response_handler == "claude":
            # Claude-style response handling
            content_list = response_data.get("content", [])
            if not content_list:
                raise ValueError("API response contains no content.")

            first_message_content = next(
                (item["text"] for item in content_list if item.get("type") == "text"), None
            )

            if first_message_content is None:
                raise ValueError("No valid text content found in the API response.")

            return ChatMessage(
                role=MessageRole.ASSISTANT,
                content=first_message_content,
                raw=response_data,
            )
        else:
            # OpenAI-style response handling
            chatCompletion = ChatCompletion.model_validate(response_data)
            
            return ChatMessage.from_dict(
                chatCompletion.choices[0].message.model_dump(include={"role", "content", "tool_calls"}),
                raw=response_data,
            )

    def generate(
        self,
        messages: List[Dict[str, Union[str, List[Dict]]]],
        stop_sequences: Optional[List[str]] = None,
        grammar: Optional[str] = None,
        tools_to_call_from: Optional[List[Tool]] = None,
        custom_role_conversions: Optional[Dict[str, str]] = None,
        convert_images_to_image_urls: bool = False,
        **kwargs,
    ) -> ChatMessage:
        """Process the input messages and return the model's response.

        Parameters:
            messages (`list[dict[str, str]]`):
                A list of message dictionaries to be processed. Each dictionary should have the structure `{"role": "user/system", "content": "message content"}`.
            stop_sequences (`List[str]`, *optional*):
                A list of strings that will stop the generation if encountered in the model's output.
            grammar (`str`, *optional*):
                The grammar or formatting structure to use in the model's response.
            tools_to_call_from (`List[Tool]`, *optional*):
                A list of tools that the model can use to generate responses.
            custom_role_conversions (`Dict[str, str]`, *optional*):
                A dictionary mapping custom role names to standard role names.
            convert_images_to_image_urls (`bool`, *optional*):
                Whether to convert images in messages to URLs.
            **kwargs:
                Additional keyword arguments to be passed to the underlying model.

        Returns:
            `ChatMessage`: A chat message object containing the model's response.
        """
        # Prepare the payload
        payload = self._prepare_payload(
            messages=messages,
            stop_sequences=stop_sequences,
            grammar=grammar,
            tools_to_call_from=tools_to_call_from,
            custom_role_conversions=custom_role_conversions,
            convert_images_to_image_urls=convert_images_to_image_urls,
            **kwargs,
        )

        # Create headers for the API request
        headers = self._create_headers()
        
        # Send the request to the API
        response = requests.post(self.api_url, headers=headers, json=payload, timeout=300)
        
        # Handle the response
        return self._handle_response(response)
    
    def __call__(
        self,
        messages: List[Dict[str, str]],
        stop_sequences: Optional[List[str]] = None,
        grammar: Optional[str] = None,
        tools_to_call_from: Optional[List[Tool]] = None,
        custom_role_conversions: Optional[Dict[str, str]] = None,
        convert_images_to_image_urls: bool = False,
        **kwargs,
    ) -> ChatMessage:
        """
        Sends a request to the Flow API and returns the response.
        This method is an alias for generate() for backward compatibility.
        """
        return self.generate(
            messages=messages,
            stop_sequences=stop_sequences,
            grammar=grammar,
            tools_to_call_from=tools_to_call_from,
            custom_role_conversions=custom_role_conversions,
            convert_images_to_image_urls=convert_images_to_image_urls,
            **kwargs,
        )