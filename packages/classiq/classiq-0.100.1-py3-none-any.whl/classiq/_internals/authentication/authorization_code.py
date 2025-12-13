from classiq._internals.authentication.authorization_flow import AuthorizationFlow


class AuthorizationCodeFlow(AuthorizationFlow):
    async def authorize(self, redirect_uri: str) -> None:
        auth_url = self.auth0_client.get_authorize_url(
            redirect_uri, self.require_refresh_token
        )
        self.open_url(auth_url)
