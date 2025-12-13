from classiq._internals.authentication.auth0 import Tokens
from classiq._internals.authentication.authorization_code import AuthorizationCodeFlow
from classiq._internals.authentication.authorization_flow import AuthorizationFlow
from classiq._internals.authentication.device import DeviceCodeFlow


class HybridFlow(AuthorizationFlow):
    def __init__(
        self, require_refresh_token: bool = True, text_only: bool = False
    ) -> None:
        super().__init__(require_refresh_token, text_only)
        self.device_flow = DeviceCodeFlow(require_refresh_token, text_only)
        self.auth_code_flow = AuthorizationCodeFlow(require_refresh_token, text_only)

    async def get_tokens(self) -> Tokens:
        device_data = await self.device_flow.get_device_data()
        await self.auth_code_flow.authorize(device_data.verification_uri_complete)
        print(f"Your user code: {device_data.user_code}")  # noqa: T201
        return await self.device_flow.poll_tokens(device_data)
