import os
from typing import Dict, Any, Optional, Union, TypedDict
import json
from ...messages.client import MessagesClient, AsyncMessagesClient
from ...errors.unauthorized_error import UnauthorizedError
from ...errors.bad_request_error import BadRequestError
from ...types.error import Error
from ...types.user_event import UserEvent
from ...types.message_event import MessageEvent
from ...core.client_wrapper import SyncClientWrapper, AsyncClientWrapper
from ...core.pydantic_utilities import parse_obj_as


class PinnacleRequest(TypedDict):
    headers: Dict[str, Any]
    body: Union[str, bytes]


def _validate_webhook_secret(
    req: PinnacleRequest, secret: Optional[str] = None
) -> None:
    """Validate webhook signature for both sync and async clients."""
    header_secret = (
        req["headers"].get("PINNACLE-SIGNING-SECRET")
        or req["headers"].get("pinnacle-signing-secret")
        or req["headers"].get("Pinnacle-Signing-Secret")
    )

    env_secret = secret or os.environ.get("PINNACLE_SIGNING_SECRET")
    if header_secret is None:
        raise UnauthorizedError(
            body=Error(
                error="Failed to get the PINNACLE-SIGNING-SECRET header from request"
            )
        )
    if env_secret is None:
        raise UnauthorizedError(
            body=Error(
                error="Make sure to set the PINNACLE_SIGNING_SECRET environment variable or pass the secret as an argument to the process method"
            )
        )
    if header_secret != env_secret:
        raise UnauthorizedError(body=Error(error="Invalid webhook signature"))


class EnhancedMessages(MessagesClient):
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    def process(
        self, req: PinnacleRequest, secret: Optional[str] = None
    ) -> Union[MessageEvent, UserEvent]:
        """Process incoming webhook request from any supported framework.

        Args:
            request: Dictionary containing the headers and body (as a string) of the request
            secret: Optional webhook secret. Uses PINNACLE_SIGNING_SECRET env var if not provided.

        Returns:
            MessageEvent: The validated and parsed message event

        Raises:
            UnauthorizedError: If webhook signature is invalid or missing
            BadRequestError: If request cannot be parsed or is invalid
        """

        _validate_webhook_secret(req, secret)

        try:
            body = json.loads(req["body"])
            if body["type"] == "USER.TYPING":
                return parse_obj_as(UserEvent, body)
            else:
                return parse_obj_as(MessageEvent, body)
        except Exception as e:
            raise BadRequestError(body=f"Invalid message event format: {str(e)}")


class AsyncEnhancedMessages(AsyncMessagesClient):
    """Async version of MessageProcessor"""

    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    async def process(
        self, req: PinnacleRequest, secret: Optional[str] = None
    ) -> Union[MessageEvent, UserEvent]:
        """Process incoming webhook request from any supported async framework.

        Args:
            request: Dictionary containing the headers and body (as a string) of the request
            secret: Optional webhook secret. Uses PINNACLE_SIGNING_SECRET env var if not provided.

        Returns:
            MessageEvent: The validated and parsed message event

        Raises:
            UnauthorizedError: If webhook signature is invalid or missing
            BadRequestError: If request cannot be parsed or is invalid
        """

        _validate_webhook_secret(req, secret)

        try:
            body = json.loads(req["body"])
            if body["type"] == "USER.TYPING":
                return parse_obj_as(UserEvent, body)
            else:
                return parse_obj_as(MessageEvent, body)
        except Exception as e:
            raise BadRequestError(body=f"Invalid message event format: {str(e)}")
