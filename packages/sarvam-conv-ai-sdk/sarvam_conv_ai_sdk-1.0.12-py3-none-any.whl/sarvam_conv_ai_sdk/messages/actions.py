"""Action messages (client and server)."""

import time
from typing import Literal

from .base import ClientMsgBase
from .config import CustomAppOverrides, InteractionConfig
from .types import ClientMsgType


class ClientInteractionStartMsg(ClientMsgBase, CustomAppOverrides):
    """Initialize interaction message from client.

    This is both the configuration object AND
    the message sent to start an interaction.
    """

    type: Literal[ClientMsgType.INTERACTION_START] = ClientMsgType.INTERACTION_START

    @classmethod
    def create_message_from_config(
        cls,
        config: InteractionConfig,
    ) -> "ClientInteractionStartMsg":
        """Create an interaction start message from ``InteractionConfig``.

        The ``timestamp`` is set at creation time.
        """

        return cls(
            agent_variables=config.agent_variables,
            initial_language_name=config.initial_language_name,
            initial_bot_message=config.initial_bot_message,
            initial_state_name=config.initial_state_name,
            timestamp=time.time(),
        )


class ClientInteractionEndMsg(ClientMsgBase):
    """Client requesting interaction end."""

    type: Literal[ClientMsgType.INTERACTION_END] = ClientMsgType.INTERACTION_END
