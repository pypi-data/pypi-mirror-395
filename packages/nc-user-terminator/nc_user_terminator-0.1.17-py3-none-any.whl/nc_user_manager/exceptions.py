class OAuthError(Exception):
    """统一封装 OAuth 调用错误"""

    def __init__(self, message: str, status_code: int = None, response: str = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(f"[{status_code}] {message}" if status_code else message)
