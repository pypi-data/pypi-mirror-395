from typing import Optional

class OAuth2AuthorizeResponse(dict):
    @property
    def url(self) -> str:
        return self.get("authorization_url")

class UserResponse(dict):
    @property
    def id(self) -> str:
        return self.get("id")

    @property
    def email(self) -> str:
        return self.get("email")

    @property
    def avatar(self) -> Optional[str]:
        return self.get("avatar")

    @property
    def full_name(self) -> Optional[str]:
        return self.get("full_name")

    @property
    def role(self) -> Optional[str]:
        return self.get("role")

    @property
    def user_id(self) -> Optional[str]:
        return self.get("user_id")

class CallbackResponse(dict):
    @property
    def token(self) -> str:
        return self.get("access_token")

    @property
    def token_type(self) -> str:
        return self.get("token_type")

    @property
    def user_name(self) -> str:
        return self.get("user_name")

    @property
    def email(self) -> str:
        return self.get("email")

    @property
    def avatar(self) -> str:
        return self.get("avatar")