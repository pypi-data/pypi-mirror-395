import asyncio
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, TypeVar

from classiq.interface.exceptions import (
    ClassiqAuthenticationError,
    ClassiqExpiredTokenError,
)

from classiq._internals.async_utils import poll_for
from classiq._internals.authentication.auth0 import Tokens
from classiq._internals.authentication.authorization_flow import AuthorizationFlow

T = TypeVar("T")


@dataclass
class DeviceData:
    user_code: str
    device_code: str
    interval: float
    expires_in: float
    verification_uri: str
    verification_uri_complete: str


class DeviceCodeFlow(AuthorizationFlow):
    _TIMEOUT_ERROR = (
        "Device registration timed out. Please re-initiate the flow and "
        "authorize the device within the timeout."
    )
    _TIMEOUT_SEC: float = timedelta(minutes=15).total_seconds()

    async def get_device_data(self) -> DeviceData:
        device_data: dict[str, Any] = await self.auth0_client.get_device_data(
            require_refresh_token=self.require_refresh_token
        )
        return DeviceData(**device_data)

    async def poll_tokens(self, device_data: DeviceData) -> Tokens:
        interval = device_data.interval
        timeout = min(device_data.expires_in, self._TIMEOUT_SEC)
        return await self._poll_tokens(
            device_code=device_data.device_code,
            interval=interval,
            timeout=timeout,
        )

    async def _poll_tokens(
        self,
        device_code: str,
        interval: float,
        timeout: float,
    ) -> Tokens:
        async def poller() -> dict[str, Any]:
            nonlocal device_code
            return await self.auth0_client.poll_tokens(device_code=device_code)

        def interval_coro() -> Iterable[float]:
            nonlocal interval
            while True:
                yield interval

        await asyncio.sleep(interval)
        async for data in poll_for(
            poller=poller, timeout_sec=timeout, interval_sec=interval_coro()
        ):
            error_code: str | None = data.get("error")
            if error_code is None:
                return self.handle_ready_data(data)
            elif error_code == "authorization_pending":
                pass
            elif error_code == "slow_down":
                # This value is used by poll_for via interval_coro
                interval *= 2
            elif error_code == "expired_token":
                raise ClassiqExpiredTokenError(self._TIMEOUT_ERROR)
            elif error_code == "access_denied":
                error_description = data.get("error_description")
                if error_description is None:
                    raise ClassiqAuthenticationError(
                        "Failed authenticating to Classiq, missing error description"
                    )

                raise ClassiqAuthenticationError(error_description)
            else:
                raise ClassiqAuthenticationError(
                    f"Device registration failed with an unknown error: {error_code}."
                )
        else:
            raise ClassiqAuthenticationError(self._TIMEOUT_ERROR)
