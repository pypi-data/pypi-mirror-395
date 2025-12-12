import json
from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class ChatSuggestion(BaseModel):
    action: Optional[Literal["enable_chat"]] = Field(default=None, description="Custom actions available to be dispatched by the chat interface")
    prompt: str = Field(..., description="Suggestion text to show in UI")
    model_config = {
        "extra": "ignore"
    }

class ChatSuggestions(BaseModel):
    chat_enabled: Optional[bool] = Field(default=True, description="This will let user only answer using the suggestions provided")
    suggestions: List[ChatSuggestion] = Field(..., description="List of suggestions that will be available for the user")

@tool(args_schema=ChatSuggestions)
def send_chat_suggestions(chat_enabled: Optional[bool] = True,
    suggestions: List[ChatSuggestion] = None):
    """
        This tool can be used to provide user predefined prompts and help during the user experience
        Example input:
        {
            "suggestions": [
                {
                    "action": null,
                    "prompt": "Suggestion 1 Prompt"
                },
                {
                    "action": null,
                    "prompt": "Suggestion 2 Prompt"
                },
                {
                    "action": "enable_chat",
                    "prompt": "Other"
                }
            ],
        } 
    """
    # No side-effects needed; return the same payload so it's accessible
    if not suggestions:
        return []
    return {"chat_enabled": chat_enabled, "suggestions": [s.model_dump() for s in suggestions]}
