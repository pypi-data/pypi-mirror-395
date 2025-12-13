import webbrowser
from typing import Any

from classiq.interface.exceptions import ClassiqAuthenticationError

from classiq._internals.authentication.auth0 import Auth0, Tokens


class AuthorizationFlow:
    def __init__(self, require_refresh_token: bool = True, text_only: bool = False):
        self.require_refresh_token = require_refresh_token
        self.text_only = text_only
        self.auth0_client = Auth0()

    async def get_tokens(self) -> Tokens:
        raise NotImplementedError

    def handle_ready_data(self, data: dict[str, Any]) -> Tokens:
        access_token: str | None = data.get("access_token") or None
        # If refresh token was not requested, this would be None
        refresh_token: str | None = data.get("refresh_token") or None

        if access_token is None or (
            self.require_refresh_token is True and refresh_token is None
        ):
            raise ClassiqAuthenticationError(
                "Token generation failed for unknown reason (missing access token or refresh token)."
            )

        return Tokens(access_token=access_token, refresh_token=refresh_token)

    def open_url(self, url: str) -> None:
        if self.text_only:
            print(  # noqa: T201
                f"Please visit this URL from any trusted device to authenticate: {url}"
            )
        else:
            webbrowser.open(url)
            print(  # noqa: T201
                f"If a browser doesn't automatically open, please visit this URL from any trusted device to authenticate: {url}"
            )
