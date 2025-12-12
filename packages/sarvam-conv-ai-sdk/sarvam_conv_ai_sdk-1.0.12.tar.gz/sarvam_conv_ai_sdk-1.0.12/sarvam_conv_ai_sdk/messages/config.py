from typing import Any, Optional

from pydantic import BaseModel, Field

from ..tool import SarvamToolLanguageName
from .audio import SampleRate
from .types import InteractionType, UserIdentifierType


class CustomAppOverrides(BaseModel):
    """Custom app overrides."""

    agent_variables: Optional[dict[str, Any]] = Field(default=None)
    initial_language_name: Optional[SarvamToolLanguageName] = Field(default=None)
    initial_bot_message: Optional[str] = Field(default=None)
    initial_state_name: Optional[str] = Field(default=None)


class InteractionConfig(CustomAppOverrides):
    """Configuration used to start an interaction.

    This config is used to build the actual start message
    (``ClientInteractionStartMsg``) that is sent on connect.
    """

    user_identifier_type: UserIdentifierType
    user_identifier: str
    org_id: str
    workspace_id: str
    app_id: str
    version: Optional[int] = Field(default=None)
    interaction_type: InteractionType
    sample_rate: SampleRate
